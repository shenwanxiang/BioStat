#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 23:10:09 2018

@author: charleshen
"""


import logging
import os

import coloredlogs
import pandas as pd
from scipy.stats import ttest_1samp

from ..dataset import load_MedExp
from ..utils.modelbase import ModelBase
from ..utils.pandastool import ParseDFtypes

coloredlogs.install()

ABSTRACT = '''相关分析用于研究定量数据之间的关系情况,包括是否有关系,以及关系紧密程度等.此分析方法通常用于回归分析之前;相关分析与回归分析的逻辑关系为:先有相关关系,才有可能有回归关系。'''


class common_i_TTest1Samp(ModelBase):

    """
    单样本T检验: 用于分析定量数据是否与某个数字有着显著的差异性,要求输入一列或多列定量数据dfx，
    和对应的一个参考数字ref_num,默认为0，返回对应列的F，p

    方法
    -------
    get_info : 
        获取该模型的信息， 返回一个字典，包含‘id’和‘name’, 'description','limited'关键字
        含义分别为：模型的id, 模型的名称，模型的描述，模型的适用范围


    run:  
        参数
        ----------
        dfx: pandas DataFrame
            需要每列的数据都是数字型数据，不能是字符串或者object
        
        ref_num: float
             需要一个数字进行对比，默认为0.0
            
            
        返回结果
        ----------        
            返回一个字典，带有‘result’关键字，其值为对应的、t-值、p-值等等系数组成的dataframe

    """
    
    
    
    def __init__(self, 
                 model_id = None, 
                 model_limiation = None,
                 ):
        
        self._name_ = '单样本T检验'


        
        
    def get_info(self):
        
        return {'id': self._id,
                'name': self._name,

                'info': self._description,
                'abstract': ABSTRACT,
                'doc': self._doc,
                'limited': '如果方法为‘pearson’，需要输入的每列的数据都是数值型数据，不能是字符串或者object',
                'args': [{"id": "x", "name": "分析项x", 'type': 'dataframe', 'requirement': '每个元素必须包含在df的列中'}],

                'extra_args': [{ 'id': "ref_num", 
                                'default': 0,
                                'name':"参考数字", 
                                'type': "inputNumber",
                                }],
                'schema': {
                    'type': 'object',
                    'properties': {
                        'ref_num': {'type': 'number'}
                    },
                }
        }

    
    
    def run(self, 
            df,
            x,
            y,
            extra_args={'ref_num':0}): 
            msg = {}
            dfx = df[x]
            ref_num = extra_args.get('ref_num')
            x_numer_cols, x_cate_cols = ParseDFtypes(dfx)
    
            if x_numer_cols ==[]:
                logging.error('All input dfx are no numeric columns, Please check your input dfx data!')
                msg['error'] = '输入的dfx所有的列都不是数值型数据，请检查输入数据'
                return  {'result':'', 'msg':msg},pd.DataFrame()
            
            
            else:
                
                if x_cate_cols != []:
                    logging.warning('input dfx has non-numeric columns: %s, will ignore these columns!' % x_cate_cols)
                    msg['warning'] = '输入的dfx包含了非数值型的列: %s, 将会被自动忽略！' % x_cate_cols
                
                
                rs = []
                for i in x_numer_cols:
                    F,p = ttest_1samp(dfx[i], ref_num)
                    columns = ['t-值', 'p-值']
                    rs.append(pd.DataFrame([F,p],index=columns,columns=[i]).T)

                res = pd.concat(rs)
                
                res['p-值'] = res['p-值'].apply(lambda x:'{:.5f}'.format(x))
                
                dfres = res.round(5)
                return {'tables': [{'table_json': dfres.reset_index().to_json(orient='index'),
                            'table_html': dfres.to_html(),
                            'table_info': '生成的字段之间的相关系数和p-值表',
                            'chart': ['heatmap', 'line', 'bar']}],
                            'conf': self.get_info(),
                            'msg': msg}, [{'table_df': dfres, 'label': '生成的字段之间的相关系数和p-值表'}]
            
        
        
            

if __name__ == '__main__':
    
    
    #读取数据
    #from dataset import load_MedExp
    
    
    df =load_MedExp()

    testdata = load_MedExp()
    dfx = df[['med','age','idp']]
    
    
    
    #类的初始化
    O = TTest1Samp()

    #打印该类描述的信息
    print(O.get_info().get('description'))
    
    #执行运算，传入tsx、tsy参数
    dict_res = O.run(dfx, ref_num=20)
    
    #获取返回的字典
    dict_res.get('result')
