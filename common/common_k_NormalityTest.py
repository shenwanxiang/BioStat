#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 23:29:10 2018

@author: charleshen
"""

#https://stackoverflow.com/questions/7903977/implementing-a-kolmogorov-smirnov-test-in-python-scipy



'''


正态性检验分析结果
名称	样本量	Kolmogorov-Smirnov检验	Shapro-Wilk检验
统计量	p	统计量	p
【系统】网购忠诚度_定量	150	0.204	0.000**	0.900	0.000**
【系统】平台偏好_定类	150	0.348	0.000**	0.736	0.000**


'''





import logging
import os

import coloredlogs
import pandas as pd
from scipy.stats import kstest, shapiro

from ..dataset import load_MedExp
from ..utils.modelbase import ModelBase
from ..utils.pandastool import ParseDFtypes

coloredlogs.install()

ABSTRACT = '''相关分析用于研究定量数据之间的关系情况,包括是否有关系,以及关系紧密程度等.此分析方法通常用于回归分析之前;相关分析与回归分析的逻辑关系为:先有相关关系,才有可能有回归关系。'''



class common_k_NormalityTest(ModelBase):

    """
    正态性检验用于分析数据是否呈现出正态性特质,可以输入一个dataframe dfx,需要为数字型的数据
    返回一个dataframe，在‘result‘关键字中保存了正太检验的结果（Kolmogorov-Smirnov检验和Shapro-Wilk检验）
    
    
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
                   
            
        返回结果
        ----------        
            返回一个字典，带有‘result’关键字，包含统计量w、p-值等等系数组成的dataframe

    """
    
    
    
    def __init__(self, 
                 model_id = None, 
                 model_limiation = None,
                 ):
        
        self._name_ = '正态性检验'


        
        
    def get_info(self):
        
        return {'id': self._id,
                'name': self._name,

                'info': self._description,
                'abstract': ABSTRACT,
                'doc': self._doc,
                'limited': '如果方法为‘pearson’，需要输入的每列的数据都是数值型数据，不能是字符串或者object',
                'args': [{"id": "x", "name": "分析项x", 'type': 'dataframe', 'requirement': '每个元素必须包含在df的列中'}],

                'extra_args': []
                }
    
    
    def run(self,
            df,
            x,
            y,
            extra_args={}): 

        
            dfx = df[x]
            msg = {}
            
            x_numer_cols, x_cate_cols = ParseDFtypes(dfx)


            if x_numer_cols ==[]:
                logging.error('All input dfx are no numeric columns, Please check your input dfx data!')
                msg['error'] = '输入的dfx所有的列都不是数值型数据，请检查输入数据'
                return  {'result':'', 'msg':msg},pd.DataFrame()
            
            
            else:
                
                if x_cate_cols != []:
                    logging.warning('input dfx has non-numeric columns: %s, will ignore these columns!' % x_cate_cols)
                
                    msg['warning'] = '输入的dfx包含了非数值型的列: %s, 将会被自动忽略！' % x_cate_cols       

                 
                rr = []
                for i in x_numer_cols:
                    dfi = dfx[i].dropna()
                    
                    l = len(dfi)
                    
                    ks_w, ks_p  = kstest(dfi,'norm') 
                    ws_w,ws_p = shapiro(dfi)
                    
                    
                    cols = ['样本量', 'KS检验：统计量','KS检验：p值','Shapro-Wilk检验：统计量', 'Shapro-Wilk检验：p-值']	
                            
                    dfr = pd.DataFrame([l, ks_w, ks_p,ws_w,ws_p],index=cols,columns=[i]).T
                    
                    rr.append(dfr)
                res = pd.concat(rr)
                    
                res['KS检验：p值'] = res['KS检验：p值'].apply(lambda x:'{:.5f}'.format(x))
                res['Shapro-Wilk检验：p-值'] = res['Shapro-Wilk检验：p-值'].apply(lambda x:'{:.5f}'.format(x))
                
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
    O = NormalityTest()

    #打印该类描述的信息
    print(O.get_info().get('description'))
    
    #执行运算，传入tsx、tsy参数
    dict_res = O.run(dfx)
    
    #获取返回的字典
    dict_res.get('result')            
