#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 14:04:31 2018

@author: charleshen
"""

import logging
import os

import coloredlogs
import pandas as pd

from ..dataset import load_MedExp
from ..utils.modelbase import ModelBase
from ..utils.pandastool import ParseDFtypes

coloredlogs.install()

ABSTRACT = '''相关分析用于研究定量数据之间的关系情况,包括是否有关系,以及关系紧密程度等.此分析方法通常用于回归分析之前;相关分析与回归分析的逻辑关系为:先有相关关系,才有可能有回归关系。'''

class common_d_GroupByStat(ModelBase):

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
        
        self._name_ = '分类汇总方法'

        
        
    def get_info(self):
        
        return {'id': self._id,
                'name': self._name,

                'info': self._description,
                'abstract': ABSTRACT,
                'doc': self._doc,
                'limited': '如果方法为‘pearson’，需要输入的每列的数据都是数值型数据，不能是字符串或者object',
                'args': [{"id": "x", "name": "分析项x", 'type': 'dataframe', 'requirement': '每个元素必须包含在df的列中'},
                         ],

                'extra_args': [{'id': "method",
                                'default': 'count',
                                'name': "汇总方式",
                                'type': "select",
                                'choice': [{'value': 'count', 'label': '汇总出现的个数'},
                                           {'value': 'mean',
                                               'label': '汇总平均数'},
                                           {'value': 'sum', 'label': '汇总和'},
                                           {'value':'std','label':'汇总标准差'}]
                                }
                               ],
                 'schema': {
                    'type': 'object',
                    'properties': {
                        'method': {'type': 'string'}
                    },
                }
                }

    
    
    def run(self, 
            df, 
            x,
            y,
            extra_args={'method':'count'}): 

        by=x
        numer_cols, cate_cols = ParseDFtypes(df)
        
        msg = {}
        method = extra_args.get('method')
        
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
            
        return {'tables': [{'table_json': result.reset_index().to_json(orient='index'),
                            'table_html': result.to_html(),
                            'table_info': '生成的字段之间的相关系数和p-值表',
                            'chart': ['heatmap', 'line', 'bar']}],
                'conf': self.get_info(),
                'msg': msg}, [{'table_df': result, 'label': '生成的字段之间的相关系数和p-值表'}]
        

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
