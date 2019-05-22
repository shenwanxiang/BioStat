#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 14:04:31 2018

@author: charleshen
"""

from .utils.pandastool import ParseDFtypes
from .utils.modelbase import ModelBase
from .dataset import load_MedExp

import pandas as pd
import coloredlogs,logging
coloredlogs.install()


class GroupByStat(ModelBase):

    """
    数据的分类汇总方法，run函数需要至少输入一个原始数据DataFrame，
    以及需要汇总的列（list，比如['colums1','columns2'])，和汇总的方式，比如‘mean’
    
    
    
    方法
    -------
    get_info : 
        获取该模型的信息， 返回一个字典，包含‘id’和‘name’, 'description','limited'关键字
        含义分别为：模型的id, 模型的名称，模型的描述，模型的适用范围

    run:  
        参数
        ----------
        df: pandas DataFrame
            原始数据
        
        by: list
            需要汇总的列,list每个元素必须是df中包含的列名
            
        method: str
            需要汇总的方式，可选'count'(汇总出现的个数, 默认),'mean'（汇总平均数）,'sum'（汇总和）,'std'（汇总标准差）, 等等
            
            
        返回结果
        ----------        
            返回一个字典，带有‘result’关键字，其值为由汇总结果组成的dataframe
    """
    
    
    
    def __init__(self, 
                 model_id = None, 
                 model_limiation = None,
                 ):
        
        self._id_ = model_id
        self._limitation_ = model_limiation

        
        
    def get_info(self):
        
        return {'id': self._id, 
                'name': self._name, 
                'description': self._description,
                'limited':self._limitation
                }
    
    
    def run(self, 
            df, 
            by,
            method = 'count'): 


        numer_cols, cate_cols = ParseDFtypes(df)
        
        msg = {}
        
        
        if numer_cols == []:
            logging.error('All input DataFrame are no numeric columns, Please check your input data!')
            result = pd.DataFrame()
            msg['error'] = '输入的所有的列都不是数值型数据，请检查输入数据df！'

        else:
            if method != 'count':
                
                s1 = set(by)
                s2 = set(numer_cols)
                if s2.issubset(s1):
                    logging.error('by columns contains all numeric columns, no numeric data to calculate!')
                    msg['error'] ='参数by占用了所有数值型的列， 所以没有额外的数值型列来计算 %s 的结果！' % method
                    
                    result = pd.DataFrame()                    
                else:
                    dfg = df.groupby(by)
                    result = dfg.agg(method)
                    result = result.round(5)

            else:
                result = df.groupby(by).size().to_frame(name= '样本量')
            
        return {'result':result, 'msg':msg}
        
        

if __name__ == '__main__':
    
    

    df = load_MedExp()
    
    
    #类的初始化
    O = GroupByStat()

    #打印该类描述的信息
    print(O.get_info().get('description'))
    
    #执行运算，传入tsx、tsy参数
    res = O.run(df, by = ['sex','health'], method='mean')
    
    #获取返回的字典
    res1 = res.get('result')