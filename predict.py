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
import tensorflow as tf
import tqdm
import csv
# 调用GPU方法
import os
import tensorflow as tf

config = tf.compat.v1.ConfigProto(gpu_options=tf.compat.v1.GPUOptions(allow_growth=True))
sess = tf.compat.v1.Session(config=config)
# 选择编号为0的GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # 我的笔记本只有一块GPU，编号是0，所以这里调用编号为0的GPU


def time_series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
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
    for i in range(1, n_out + 1):
        time = '(t+%d)' % i
        cols.append(df.shift(-i))
        names += [('%s%s' % (origNames[j], time)) for j in range(n_vars)]
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    if dropnan:
        agg.dropna(inplace=True)
    return agg


# 打开数据库连接
db = pymysql.connect(host='10.236.66.44',
                     user='lx',
                     password='123456',
                     database='stock')

# 使用cursor()方法获取操作游标
cursor = db.cursor()
stock_id_list = []
stock_data = []
sql_stock = "select * from stock_info"
try:
    cursor.execute(sql_stock)
    stock_id_result = cursor.fetchall()
    for x in stock_id_result:
        stock_id_list.append(x[1])
except pymysql.Error as e:
    print("Error: unable to fetch data")
# SQL 查询语句
for x in tqdm.tqdm(stock_id_list):
    sql = "SELECT * FROM stock_hisinfo where  stock_id=" + x
    sql2 = "SELECT * FROM stock_a_lg_indicator where stock_id=" + x
    stock_data_tmp = []
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        cursor.execute(sql2)
        # 获取所有记录列表
        results2 = cursor.fetchall()
        r_dict = dict()
        for i in results2:
            r_dict[i[0]]=i
        # print("result:",results )
        for row in results:
            stockrow = []
            stockrow.append(row[2])
            stockrow.append(row[3])
            stockrow.append(row[4])
            stockrow.append(row[5])
            try:
                stockrow.append(r_dict[row[1]][1])
            except:
                r_dict[row[1]]=[0 for i in range(9)]
                stockrow.append(r_dict[row[1]][1])
            stockrow.append(r_dict[row[1]][2])
            stockrow.append(r_dict[row[1]][3])
            stockrow.append(r_dict[row[1]][4])
            stockrow.append(r_dict[row[1]][5])
            stockrow.append(r_dict[row[1]][6])
            stockrow.append(r_dict[row[1]][7])
            stockrow.append(r_dict[row[1]][8])
            stock_data_tmp.append(stockrow)
            # 打印结果
    except pymysql.Error as e:
        print("Error: unable to fetch data")
    stock_data.append(stock_data_tmp)
# 关闭数据库连接
db.close()
scaler = []
for i in range(len(stock_data)):
    scaler.append(MinMaxScaler(feature_range=(0, 1)))
for i in range(len(stock_data)):
    stock_data[i] = scaler[i].fit_transform(stock_data[i])
# df = pd.DataFrame(scaledData1)
# print(df)
# print(df.shift(1))
# print(scaledData1.shape)
processedData = []
n_steps_in = 50  # 历史时间长度
n_steps_out = 7  # 预测时间长度
for x in tqdm.tqdm(stock_data):
    processedData1 = time_series_to_supervised(x, n_steps_in, n_steps_out)
    # processedData=pd.concat([processedData,processedData1])
    processedData.append(processedData1)
print(processedData)
# print(processedData)
test_input = []
test_label = []
index = 1
input_size=12
rmse=[]
for x in tqdm.tqdm(processedData):
    data_x = x.loc[:, '0(t-' + str(n_steps_in) + ')':'{}(t-1)'.format(input_size-1)]
    data_y = x.loc[:, '0':'3','0(t+1)':'3(t+1)','0(t+2)':'3(t+2)','0(t+3)':'3(t+3)','0(t+4)':'3(t+4)','0(t+5)':'3(t+5)','0(t+6)':'3(t+6)',
    '0(t+7)':'3(t+7)']
    try:
        train_X1, test_X1, train_y, test_y = train_test_split(data_x.values, data_y.values, test_size=0.3, random_state=343)
    except:
        continue
    test_X = test_X1.reshape((test_X1.shape[0], n_steps_in, input_size))
    # reshape input to be 3D [samples, timesteps, features]
    train_X =train_X1.reshape((train_X1.shape[0], n_steps_in, input_size))
    test_input.append(test_X)
    test_label.append(test_y)
# design network
    model = Sequential()
    model.add(LSTM(96, return_sequences=True, input_shape=(train_X.shape[1], train_X.shape[2])))
    model.add(Dropout(0.2))
    model.add(LSTM(64, return_sequences=False))  # returns a sequence of vectors of dimension 32
    model.add(Dropout(0.2))
    model.add(Dense(32))
    model.add(Dropout(0.2))
    model.add(Dense(28))
    model.compile(loss='mse', optimizer='adam')
    print(model.summary())
    # fit network
    # model = load_model('./model_multi_lstm.h5')
    history = model.fit(train_X, train_y, epochs=30, batch_size=128, validation_data=(test_X, test_y), verbose=1,
                        shuffle=False)

    model.save('./pre_model{i}.h5'.format(i=index))

# plot history
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='test')
    plt.legend()
    if(index<5):
        plt.savefig('./history_loss{i}.jpg'.format(i=index))



#  # 预测
    yhat =model.predict(test_X)
    for i in len(test_y):
        rmse.append(sqrt(mean_squared_error(test_y[:, i], yhat[:, i])))
        index=index+1
res=np.array(rmse)
pd.DataFrame(res).to_csv('rmse.csv')

# # 逆转预测值
# # print(yhat[:,2])
# inv_forecast_y = scaler.inverse_transform(yhat)
#     # 逆转实际值
# inv_test_y = scaler.inverse_transform(test_y)
# # 计算均方根误差
# count=0
# for i in range(len(inv_test_y[:,2])):
#         if inv_test_y[:,2][i]-inv_forecast_y[:,2][i]<=0.03 or inv_forecast_y[:,2][i]-inv_test_y[:,2][i]<=0.03:
#             count=count+1
# acu=count/len(inv_test_y[:,2])
# print(acu)
#
# rmse = sqrt(mean_squared_error(inv_test_y[:,2], inv_forecast_y[:,2]))
# print('Test RMSE: %.3f' % rmse)
# # print(n_steps_in)
# #画图
# plt.figure(figsize=(16,8))
# plt.plot(inv_test_y[0:300,2], label='true')
# plt.plot(inv_forecast_y[0:300,2], label='pre')
# plt.legend()
# plt.savefig('./predict.jpg')
# plt.show()