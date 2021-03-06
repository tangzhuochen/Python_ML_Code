# -*- coding:utf-8 -*-
__author__ = 'maomaochong'
"""
训练woe规则与进行woe转换
"""
import pandas as pd
import woe.config as config
import woe.feature_process as fp
import woe.eval as eval
import pickle
import time
import csv
import numpy as np
from multiprocessing import Pool
import os


######################################################
# import sys
# # make a copy of original stdout route
# stdout_backup = sys.stdout
# # define the log file that receives your log info
# log_file = open(r'E:\ScoreCard\cs_model\cs_m1_pos_model_daily\log\cs_m1_pos_daily_alg02.log', "w")
# # redirect print output to log file
# sys.stdout = log_file
#
# print "Now all print info will be written to message.log"
# # any command line that you will execute
######################################################

# get columns names list
config_path = r'E:\Code\Python_ML_Code\cs_model\config\config_cs_daily_model.csv'
cfg = config.config()
cfg.load_file(config_path)
col_dataset = pd.read_csv(config_path)
col_name_list = col_dataset.var_name

"""
训练WOE规则
"""
def process_train_woe(cfg=None,feature_name=None,target=None):
    print 'run into process_train_woe: \n',feature_name,time.asctime(time.localtime(time.time()))
    feature_path = 'E:\\ScoreCard\\cs_model\\cs_m1_pos_model_daily\\raw_data\\dataset_split_by_cols\\'
    feature_path = feature_path + feature_name + '.csv'
    feature = pd.read_csv(feature_path)
    rst = []
    if feature.columns[0] in list(cfg.bin_var_list):
        feature.loc[feature[feature.columns[0]].isnull()] = -1
        fp.change_feature_dtype(feature, cfg.variable_type)
        dataset = pd.merge(feature.reset_index(),target.reset_index()).drop('index', axis=1)
        var = feature.columns[0]
        del feature
        del target
        riv = fp.proc_woe_continuous(dataset,var,cfg.global_bt,cfg.global_gt,cfg.min_sample,alpha=0.05)
    else: # process woe transformation of discrete variables
        print 'process woe transformation of discrete variables: \n',time.asctime(time.localtime(time.time()))
        feature.loc[feature[feature.columns[0]].isnull()] = 'missing'
        fp.change_feature_dtype(feature, cfg.variable_type)
        dataset = pd.merge(feature.reset_index(),target.reset_index()).drop('index', axis=1)
        var = feature.columns[0]
        del feature
        del target
        riv = fp.proc_woe_discrete(dataset,var,cfg.global_bt,cfg.global_gt,cfg.min_sample,alpha=0.05)

    rst.append(riv)
    feature_detail = eval.eval_feature_detail(rst)

    rst_path = 'E:\\ScoreCard\\cs_model\\cs_m1_pos_model_daily\\gendata\\WOE_Rule\\'
    rst_path = rst_path + feature_name + '.pkl'

    result = (riv,feature_detail)
    output = open(rst_path, 'wb')
    pickle.dump(result,output)
    output.close()

    return result


def single_process(var):
    target_path = r'E:\ScoreCard\cs_model\cs_m1_pos_model_daily\raw_data\dataset_split_by_cols\target.csv'
    target = pd.read_csv(target_path)
    fp.change_feature_dtype(target, cfg.variable_type)
    cfg.global_bt = sum(target.target)
    cfg.global_gt = target.shape[0] - cfg.global_bt
    cfg.min_sample = int(target.shape[0]*0.05)

    return process_train_woe(cfg,feature_name=var,target=target)


# feature_list = list(cfg.bin_var_list)
# feature_list.extend(list(cfg.discrete_var_list))
#
# for i in range(89,feature_list.__len__()):
#     try:
#         result = single_process(feature_list[i])
#     except Exception:
#         print '[error]',feature_list[i]

######################################################
# log_file.close()
# # restore the output to initial pattern
# sys.stdout = stdout_backup
#
# print "Now this will be presented on screen"
######################################################


if __name__ == "__main__":

    feature_list = list(cfg.bin_var_list)
    feature_list.extend(list(cfg.discrete_var_list))
    rst_path = 'E:\\ScoreCard\\cs_model\\cs_m1_pos_model_daily\\gendata\\WOE_Rule\\'
    rst_list = os.listdir(rst_path)
    rst_list = [rst_list[i].split(".")[0] for i in range(rst_list.__len__())]

    feature_list_todo = list(set(feature_list)^set(rst_list))
    # riv_list = []
    # feature_detail_list = []
    # for var in feature_list:
    #     riv,feature_detail = process_train_woe(cfg,feature_name=var,target=target)
    #     riv_list.append(riv)
    #     feature_detail_list.append(feature_detail)

    pool = Pool(processes=1)
    result = pool.map(single_process,feature_list_todo)
    pool.close()
    pool.join()



"""
进行WOE转换
"""
# def process_woe_trans(cfg=None,in_data_path=None,rst_path=None,out_path=None):
#     # config_path = r'E:\Code\Python_ML_Code\cs_model\config\config_cs_daily_model.csv'
#     # data_path = in_data_path
#     # cfg = config.config()
#     # cfg.load_file(config_path, data_path)
#
#     dataset = pd.read_csv(in_data_path)
#     for var in [tmp for tmp in cfg.bin_var_list if tmp in list(dataset.columns)]:
#         # fill null
#         dataset.loc[dataset[var].isnull(), (var)] = -1
#
#     for var in [tmp for tmp in cfg.discrete_var_list if tmp in list(dataset.columns)]:
#         # fill null
#         dataset.loc[dataset[var].isnull(), (var)] = 'missing'
#
#     fp.change_feature_dtype(dataset, cfg.variable_type)
#
#     output = open(rst_path, 'rb')
#     rst = pickle.load(output)
#     output.close()
#
#     # Training dataset Woe Transformation
#     r = rst[0]
#     dataset[r.var_name] = fp.woe_trans(dataset[r.var_name], r)
#     dataset.to_csv(out_path)
#     print('%s\tSUCCESS EXPORT FILE: \n%s' %(time.asctime(time.localtime(time.time())),out_path))
#
#
# def single_process_woe_trans(var):
#     print('%s\tPROC WOE TRANS: \t%s' %(time.asctime(time.localtime(time.time())),var))
#     # target_path = r'E:\ScoreCard\cs_model\cs_m1_pos_model_daily\raw_data\dataset_split_by_cols\target.csv'
#     # target = pd.read_csv(target_path)
#     #
#     # cfg.global_bt = sum(target.target)
#     # cfg.global_gt = target.shape[0] - cfg.global_bt
#     # cfg.min_sample = int(target.shape[0]*0.05)
#
#     in_data_path = 'E:\\ScoreCard\\cs_model\\cs_m1_pos_model_daily\\raw_data\\dataset_split_by_cols\\' + var + '.csv'
#     rst_path = 'E:\\ScoreCard\\cs_model\\cs_m1_pos_model_daily\\gendata\\WOE_Rule\\' + var + '.pkl'
#     out_path = 'E:\\ScoreCard\\cs_model\\cs_m1_pos_model_daily\\gendata\\' + var + '_woe_transed.csv'
#     return process_woe_trans(cfg,in_data_path,rst_path,out_path)
#     # return process_woe_trans(in_data_path,rst_path,out_path)

# if __name__ == "__main__":
#     feature_list = list(cfg.bin_var_list)
#     feature_list.extend(list(cfg.discrete_var_list))
#
#     for i in range(feature_list.__len__()):
#         try:
#             # result = single_process_woe_trans(feature_list[i])
#             result = single_process(feature_list[i])
#         except Exception:
#             print '[error]',feature_list[i]



