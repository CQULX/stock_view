import pymysql
import joblib
from math import sqrt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
try:
    from keras import Sequential
    from keras.layers import Dense
    from keras.layers import LSTM
    from keras.layers import Dropout
    from keras.models import load_model
except:
    from tensorflow.keras import Sequential
    from tensorflow.keras.layers import Dense
    from tensorflow.keras.layers import LSTM
    from tensorflow.keras.layers import Dropout
    from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import akshare
from sqlalchemy import create_engine
from mysite.settings import DATABASES
#调用GPU方法
import os
import tensorflow as tf
try:
    config = tf.compat.v1.ConfigProto(gpu_options=tf.compat.v1.GPUOptions(allow_growth=True))
    sess = tf.compat.v1.Session(config=config)
    # 选择编号为0的GPU
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"#我的笔记本只有一块GPU，编号是0，所以这里调用编号为0的GPU
except:
    print("GPU Cannot Load!")

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

def pre(stock_id):
    user_name = DATABASES['default']['USER']
    password = DATABASES['default']['PASSWORD']
    ip = DATABASES['default']['HOST']
    port = DATABASES['default']['PORT']
    # 打开数据库连接
    db = pymysql.connect(host=ip,
                        user=user_name,
                        password=password,
                        database='stock')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "SELECT * FROM stock_hisinfo where  stock_id="+stock_id
    sql2 = "SELECT * FROM stock_a_lg_indicator where stock_id=" + stock_id
    con_string = ('mysql+pymysql://{}:{}@{}:{}/stock'.format(user_name,password,ip,port))
    engine=create_engine(con_string) # 可用于to_sql和read_sql
    errInd=[]
    stock_zh_a_hist_df = akshare.stock_a_lg_indicator(stock_id)
    df_id = {'stock_id': [str(stock_id) for k in range(len(stock_zh_a_hist_df))]}
    stock_zh_a_hist_df['stock_id'] = pd.DataFrame(df_id)
    stock_zh_a_hist_df.to_sql('stock_a_lg_indicator', engine, if_exists='append', index=False)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # print("result:",results )
        cursor.execute(sql2)
        # 获取所有记录列表
        results2 = cursor.fetchall()
        r_dict = dict()
        for i in results2:
            r_dict[i[0]] = i
        stock_data=[]
        stock_datay=[]
        for row in results:
            stockrow=[]
            stockrow.append(row[2])
            stockrow.append(row[3])
            stockrow.append(row[4])
            stockrow.append(row[5])
            stock_datay.append(stockrow[:])
            try:
                stockrow.append(r_dict[row[1]][1])
            except:
                r_dict[row[1]] = [0 for i in range(9)]
                stockrow.append(r_dict[row[1]][1])
            stockrow.append(r_dict[row[1]][2])
            stockrow.append(r_dict[row[1]][3])
            stockrow.append(r_dict[row[1]][4])
            stockrow.append(r_dict[row[1]][5])
            stockrow.append(r_dict[row[1]][6])
            stockrow.append(r_dict[row[1]][7])
            stockrow.append(r_dict[row[1]][8])
            stock_data.append(stockrow)
            # 打印结果
    except pymysql.Error as e:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()
    try:    
        model=load_model('./mysite/stock_view/code/model/model{}.h5'.format(stock_id))
        print("存在训练好的模型")
        scaler=joblib.load('./mysite/stock_view/code/scaler/scaler{}'.format(stock_id))
        scalery=joblib.load('./mysite/stock_view/code/scaler/scalery{}'.format(stock_id))
        rmse = None
    except:
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaledData1 = scaler.fit_transform(stock_data)
        scalery = MinMaxScaler(feature_range=(0, 1))
        scalery.fit_transform(stock_datay)

        joblib.dump(scaler,'./mysite/stock_view/code/scaler/scaler{}'.format(stock_id))
        joblib.dump(scalery,'./mysite/stock_view/code/scaler/scalery{}'.format(stock_id))
        # print(scaledData1.shape)
        #缺失数据处理
        for i in range(scaledData1.shape[1]):
            # 获取当前列数据
            temp_col = scaledData1[:, i]
            # 判断当前列的数据中是否含有nan
            nan_num = np.count_nonzero(temp_col != temp_col)
            if nan_num != 0:
                temp_col_not_nan = temp_col[temp_col == temp_col]
                # 将nan替换成这一列的平均值
                try:
                    temp_col[np.isnan(temp_col)] = np.mean(temp_col_not_nan)
                except:
                    temp_col[np.isnan(temp_col)]=0


        n_steps_in =50 #历史时间长度
        n_steps_out=7#预测时间长度
        processedData1 = time_series_to_supervised(scaledData1,n_steps_in,n_steps_out)
        # print(processedData1.head())

        # data_x = processedData1.loc[:,'0(t-'+str(n_steps_in)+')':'3(t-1)']
        # data_y = processedData1.loc[:,'0':'3']

        data_x = processedData1.loc[:, '0(t-' + str(n_steps_in) + ')':'{}(t-1)'.format(12 - 1)]
        data_y = processedData1.loc[:, ['0', '1', '2', '3', '0(t+1)', '1(t+1)', '2(t+1)', '3(t+1)',
                                        '0(t+2)', '1(t+2)', '2(t+2)', '3(t+2)', '0(t+3)', '1(t+3)', '2(t+3)', '3(t+3)',
                                        '0(t+4)', '1(t+4)', '2(t+4)', '3(t+4)', '0(t+5)', '1(t+5)', '2(t+5)', '3(t+5)',
                                        '0(t+6)', '1(t+6)', '2(t+6)', '3(t+6)']]

        train_X1,test_X1, train_y, test_y = train_test_split(data_x.values, data_y.values, test_size=0.3, random_state=343)
        # reshape input to be 3D [samples, timesteps, features]
        train_X = train_X1.reshape((train_X1.shape[0], n_steps_in, scaledData1.shape[1]))
        test_X = test_X1.reshape((test_X1.shape[0], n_steps_in, scaledData1.shape[1]))
        # design network
        model = Sequential()
        model.add(LSTM(96,return_sequences=True, input_shape=(train_X.shape[1], train_X.shape[2])))
        model.add(Dropout(0.2))
        model.add(LSTM(64, return_sequences=False))  # returns a sequence of vectors of dimension 32
        model.add(Dropout(0.2))
        model.add(Dense(32))
        model.add(Dropout(0.2))
        model.add(Dense(train_y.shape[1]))
        model.compile(loss='mse', optimizer='adam')
        # print(model.summary())
        # fit network
        history = model.fit(train_X, train_y, epochs=10, batch_size=64, validation_data=(test_X, test_y), verbose=2,
                            shuffle=False)

        model.save('./mysite/stock_view/code/model/model{}.h5'.format(stock_id))
            # # plot history
        plt.plot(history.history['loss'], label='train')
        plt.plot(history.history['val_loss'], label='test')
        plt.legend()

        plt.savefig('./history.jpg')


        # plt.show()
        # 预测
        yhat = model.predict(test_X)
        # 逆转预测值
        # print(yhat[:,2])
        # scaler=joblib.load('./scaler_all/scaler300812')


        # 计算均方根误差
        rmsetmp=[]
        for i in range(28):
            rmsetmp.append(sqrt(mean_squared_error(test_y[:, i], yhat[:, i])))
        rmse = sum(rmsetmp) / len(rmsetmp)
        print('Test RMSE: %.3f' % rmse)

    test_X=stock_data[-51:-1]
    test_X=scaler.transform(test_X)
    for i in range(test_X.shape[1]):
        #获取当前列数据
        temp_col = test_X[:,i]
        # 判断当前列的数据中是否含有nan
        nan_num = np.count_nonzero(temp_col != temp_col)
        if nan_num != 0:
            temp_col_not_nan = temp_col[temp_col==temp_col]
            # 将nan替换成这一列的平均值
            temp_col[np.isnan(temp_col)] = np.mean(temp_col_not_nan)
    yhat = model.predict(test_X.reshape(1,50,12))
    yhat[0,:4] = scalery.inverse_transform(yhat[0,:4].reshape(1,-1))
    yhat[0,4:8] = scalery.inverse_transform(yhat[0,4:8].reshape(1,-1))
    yhat[0,8:12] = scalery.inverse_transform(yhat[0,8:12].reshape(1,-1))
    yhat[0,12:16] = scalery.inverse_transform(yhat[0,12:16].reshape(1,-1))
    yhat[0,16:20] = scalery.inverse_transform(yhat[0,16:20].reshape(1,-1))
    yhat[0,20:24] = scalery.inverse_transform(yhat[0,20:24].reshape(1,-1))
    yhat[0,24:28] = scalery.inverse_transform(yhat[0,24:28].reshape(1,-1))
    test_X = scaler.inverse_transform(test_X)[:,:4]
    yhat = yhat.reshape(-1,4)
    # print(n_steps_in)
    #画图
    plt.figure(figsize=(16,8))
    plt.plot(range(0,50),test_X[:,0], label='true')
    plt.plot(range(50,57),yhat[:,0], label='pre')
    plt.legend()
    plt.savefig('./predict.jpg')
    result=[]
    result+=list(test_X)
    result+=list(yhat)
    return result,rmse
