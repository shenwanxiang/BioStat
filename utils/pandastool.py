#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 19:42:41 2018
@email: shenwanxiang@tinghua.org.cn
@author: charleshen


每一算法类包含若干函数：
get_info()   获取算法说明的JSON结构体，包括算法的名称、使用方法、使用约束等信息，如： 


{id: 'xxx', 
name: 'ooo', 
description: 'xxx', 
limited: {} ... }



run(args)    执行算法，args为输入的数据和参数，比如 {x: xArr, y: yArr, args: {arg1: 1} }，返回计算结果, json里面嵌套dataframe格式
validate(args)   检验算法的数据和参数是否合法，返回{result: True/False, msg: 'xxx'}
输入的数据和输出的数据都用json和pandas的dataframe格式


"""



import pandas as pd
    

def isCategory(ts):
    
    if str(ts.dtypes) in ['object','bool','category']:
        return True
    else:
        return False
    
def isSeries(ts):
    
    if type(ts) == pd.Series:
        return True
    else:
        return False
    
    
    
    
class P(object):
    
    def __init__(self, df):
        self.df = df

    def __sub__(self):
        numeric_cols, category_cols = ParseDFtypes(self.df)
        return numeric_cols
    
    
    
def ParseDFtypes(df):
    
    dtypes = df.dtypes
    bool_cols = dtypes[dtypes == 'bool'].index.tolist()
    cat_cols = dtypes[dtypes == 'category'].index.tolist()
    float_cols= dtypes[dtypes == 'float'].index.tolist()
    int_cols = dtypes[dtypes == 'int'].index.tolist()
    object_cols = dtypes[dtypes == 'object'].index.tolist()
            

    numeric_cols = float_cols + int_cols
    category_cols = bool_cols + cat_cols + object_cols
    
    return numeric_cols, category_cols



    
    
def ConvertNumeric2Category(df_numer,bins=10):
    
    con_ = []
    for s in df_numer.columns:
        con_.append(pd.cut(df_numer[s],bins))
        
    return pd.concat(con_,axis=1)
        




def isEqualLength(dfx,dfy):
    
    if len(dfx) != len(dfy):
        return False
    else:
        return True
    

