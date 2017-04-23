# -*- coding:utf-8 -*-
__author__ = 'maomaochong'
import sys
sys.path.append('E:/Code/Python_ML_Code/JD')
import pandas as pd
import load_data
import time
import numpy as np
"""
# create table inspector_03
# as
# select t1.`user_id`,t1.`sku_id`
# ,MAX(TO_DAYS(t2.TIME)) as max_time
# ,MIN(TO_DAYS(t2.TIME)) as min_time
# ,MAX(TO_DAYS(t2.TIME))-MIN(TO_DAYS(t2.TIME)) AS time_diff
# from inspector_02 t1
# inner join jdata_action_all t2
# on t1.user_id=t2.user_id and t1.sku_id=t2.sku_id
# group by t1.`user_id`,t1.`sku_id`;
"""
raw_data_path = 'E:/Code/Python_ML_Code/JD/raw_data/'

jdata_action_all = load_data.load_from_csv(raw_data_path,['JData_Action_ALL',])
inspector_02 = load_data.load_from_mysql('inspector_02')

print 'reading: ' +  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
result = pd.merge(inspector_02, jdata_action_all[0], how='inner', on=['user_id', 'sku_id'])
print 'done: ' +  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


result01 = result.groupby('user_id','sku_id').agg({'time_y':np.max,'time_y':np.min})

#
# print 'reading: ' +  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# result = pd.merge(jdata_action_all,inspector_02,  how='inner', on=['user_id', 'sku_id'])
# print 'done: ' +  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#

