import pymysql
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
except:
    from tensorflow.keras import Sequential
    from tensorflow.keras.layers import Dense
    from tensorflow.keras.layers import LSTM
    from tensorflow.keras.layers import Dropout
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