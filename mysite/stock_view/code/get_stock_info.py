from ipaddress import ip_address
import pandas as pd
import akshare as ak
import requests
import pymysql as mysql
from sqlalchemy import create_engine
import tqdm
import bs4
from mysite.mysite.settings import DATABASES
def update():
    user_name=DATABASES['default']['USER']
    password = DATABASES['default']['PASSWORD']
    ip_address = DATABASES['default']['HOST']
    port = DATABASES['default']['PORT']
    con_string = ('mysql+pymysql://{}:{}@{}:{}/stock'.format(user_name,password,ip_address,port))
    engine=create_engine(con_string) # 可用于to_sql和read_sql

    new_df=ak.stock_zh_a_spot_em()
    new_df['id']=new_df['代码']
    new_df.rename(columns={'序号':'No','代码':'stock_id','名称':'stock_name','最新价':'now_price','涨跌幅':'changepercent',
                           '涨跌额':'changeamount','成交量':'turnover','成交额':'vol','振幅':'swing','最高':'high_price',
                           '最低':'low_price','今开':'open_price','昨收':'close_price_yesterday','量比':'quantity_relative_ratio',
                           '换手率':'turnover_rate','市盈率-动态':'PE','市净率':'PB','总市值':'total_value','流通市值':'traded_market_value',
                           '涨速':'higher_speed','5分钟涨跌':'five_min_up_down','60日涨跌幅':'sixty_day_up_down',
                           '年初至今涨跌幅':'yeartodate_up_down'},inplace=True)
    new_df.dropna(inplace=True)
    new_df.to_sql('stock_info',engine,if_exists='replace',index=False)
# update()
