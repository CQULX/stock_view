import pymysql
from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
import pandas as pd
# from pandas import read_csv
# from pandas import DataFrame
# from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras import Sequential
from keras.models import load_model
# from keras import models
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

def time_series_to_supervised(data, n_in=1, n_out=1,dropnan=True):
    """
    :param data:作为列表或2D NumPy数组的观察序列。需要。
    :param n_in:作为输入的滞后观察数（X）。值可以在[1..len（数据）]之间可选。默认为1。
    :param n_out:作为输出的观测数量（y）。值可以在[0..len（数据）]之间。可选的。默认为1。
    :param dropnan:Boolean是否删除具有NaN值的行。可选的。默认为True。
    :return:
    """
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    origNames = df.columns
    cols, names = list(), list()
    cols.append(df.shift(0))
    names += [('%s' % origNames[j]) for j in range(n_vars)]
    n_in = max(0, n_in)
    for i in range(n_in, 0, -1):
        time = '(t-%d)' % i
        cols.append(df.shift(i))
        names += [('%s%s' % (origNames[j], time)) for j in range(n_vars)]
    n_out = max(n_out, 0)
    for i in range(1, n_out+1):
        time = '(t+%d)' % i
        cols.append(df.shift(-i))
        names += [('%s%s' % (origNames[j], time)) for j in range(n_vars)]
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    if dropnan:
        agg.dropna(inplace=True)
    return agg


# 打开数据库连接
db = pymysql.connect(host='10.236.66.12',
                     user='lx',
                     password='123456',
                     database='stock')
 
# 使用cursor()方法获取操作游标
cursor = db.cursor()
 
# SQL 查询语句
sql = "SELECT * FROM stock_hisinfo where  stock_id=1"
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    # print("result:",results )
    stock_data=[]
    for row in results:
        stockrow=[]
        stockrow.append(row[2])
        stockrow.append(row[3])
        stockrow.append(row[4])
        stockrow.append(row[5])
        stock_data.append(stockrow)
        # 打印结果
except pymysql.Error as e:
    print("Error: unable to fetch data")
 
# 关闭数据库连接
db.close()
scaler = MinMaxScaler(feature_range=(0, 1))
scaledData1 = scaler.fit_transform(stock_data)
# print(scaledData1.shape)

n_steps_in =50 #历史时间长度
n_steps_out=1#预测时间长度
processedData1 = time_series_to_supervised(scaledData1,n_steps_in,n_steps_out)
# print(processedData1.head())

data_x = processedData1.loc[:,'0(t-'+str(n_steps_in)+')':'3(t-1)']
data_y = processedData1.loc[:,'0':'3']
train_X1,test_X1, train_y, test_y = train_test_split(data_x.values, data_y.values, test_size=0.3, random_state=343)
# reshape input to be 3D [samples, timesteps, features]
train_X = train_X1.reshape((train_X1.shape[0], n_steps_in, scaledData1.shape[1]))
test_X = test_X1.reshape((test_X1.shape[0], n_steps_in, scaledData1.shape[1]))
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

# design network
# model = Sequential()
# model.add(LSTM(96,return_sequences=True, input_shape=(train_X.shape[1], train_X.shape[2])))
# model.add(Dropout(0.2))
# model.add(LSTM(64, return_sequences=False))  # returns a sequence of vectors of dimension 32
# model.add(Dropout(0.2))
# model.add(Dense(32))
# model.add(Dropout(0.2))
# model.add(Dense(train_y.shape[1]))
# model.compile(loss='mse', optimizer='adam')
# print(model.summary())
# fit network
model=load_model('./model_multi_lstm.h5')
# history = model.fit(train_X, train_y, epochs=30, batch_size=64, validation_data=(test_X, test_y), verbose=2,
#                     shuffle=False)

# model.save('./model_multi_lstm.h5')

# # plot history
# plt.plot(history.history['loss'], label='train')
# plt.plot(history.history['val_loss'], label='test')
# plt.legend()

# plt.savefig('./history.jpg')

# plt.show()

 # 预测
yhat = model.predict(test_X)
# 逆转预测值
# print(yhat[:,2])
inv_forecast_y = scaler.inverse_transform(yhat)
    # 逆转实际值
inv_test_y = scaler.inverse_transform(test_y)
# 计算均方根误差
count=0
for i in range(len(inv_test_y[:,2])):
        if inv_test_y[:,2][i]-inv_forecast_y[:,2][i]<=0.03 or inv_forecast_y[:,2][i]-inv_test_y[:,2][i]<=0.03:
            count=count+1
acu=count/len(inv_test_y[:,2])
print(acu)

rmse = sqrt(mean_squared_error(inv_test_y[:,2], inv_forecast_y[:,2]))
print('Test RMSE: %.3f' % rmse)
# print(n_steps_in)
#画图
plt.figure(figsize=(16,8))
plt.plot(inv_test_y[0:300,2], label='true')
plt.plot(inv_forecast_y[0:300,2], label='pre')
plt.legend()
plt.savefig('./predict.jpg')
plt.show()