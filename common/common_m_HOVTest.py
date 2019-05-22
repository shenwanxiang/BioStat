#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 21:00:36 2018

@author: charleshen
"""





import logging
import os

import coloredlogs
import pandas as pd
from scipy.stats import levene

from ..dataset import load_MedExp
from ..utils.modelbase import ModelBase
from ..utils.pandastool import ParseDFtypes, isCategory, isSeries

coloredlogs.install()


ABSTRACT = '''相关分析用于研究定量数据之间的关系情况,包括是否有关系,以及关系紧密程度等.此分析方法通常用于回归分析之前;相关分析与回归分析的逻辑关系为:先有相关关系,才有可能有回归关系。'''



class common_m_HOVTest(ModelBase):

    """
    方差齐检验,用于分析不同定类数据组别 对定量数据时的波动情况是否一致.也叫F检验，例如想知道三组学生的智商tsy
    身高波动（dfx）情况是否一致（通常情况希望波动一致，即方差齐）。F检验仅可对比多组数据的差异,也即tsy的unqiue元素个数可以大于2，
    返回一个dataframe，在‘result‘关键字中
    
    
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
        
        tsy: pandas Series
             需要一列的数据都是分类型数据
            
            
        返回结果
        ----------        
            返回一个字典，带有‘result’关键字，其值为按照tsy分组的均值和标准差、F-值、p-值等等系数组成的dataframe

    """
    
    
    
    def __init__(self, 
                 model_id = None, 
                 model_limiation = None,
                 ):
        
        self._name_ = '方差齐检验'


        
        
    def get_info(self):
        
        return {'id': self._id,
                'name': self._name,

                'info': self._description,
                'abstract': ABSTRACT,
                'doc': self._doc,
                'limited': '如果方法为‘pearson’，需要输入的每列的数据都是数值型数据，不能是字符串或者object',
                'args': [{"id": "x", "name": "分析项x", 'type': 'dataframe', 'requirement': '每个元素必须包含在df的列中'},
                         {"id": "y", "name": "分析项y", 'type': 'series', 'requirement': '每个元素必须包含在df的列中'}],

                'extra_args': []
                }
    
    
    def run(self, 
            df,
            x,
            y,
            extra_args={}): 

            dfx = df[x]
            tsy = df[y[0]]
            tsy = tsy.reset_index(drop=True)
            dfx = dfx.reset_index(drop=True)            
    
        
            msg = {}
            
            xl = len(dfx)
            yl = len(tsy)
            if  xl != yl:
                logging.error('the length of input X:%s is not equal the length of Y: %s ! ' % (xl,yl))
                msg['error'] = 'the length of input X:%s is not equal the length of Y: %s ! ' % (xl,yl)
                return  {'result':'', 'msg':msg},pd.DataFrame()
                
            
            if not isSeries(tsy) or not isCategory(tsy):
                logging.error('input tsy is not a pandas Series or not a category data!')
                msg['error'] = 'input tsy is not a pandas Series or not a category data!'
                
                return  {'result':'', 'msg':msg},pd.DataFrame()
                
            
            
            else:
                

                x_numer_cols, x_cate_cols = ParseDFtypes(dfx)


                if x_numer_cols ==[]:
                    logging.error('All input dfx are no numeric columns, Please check your input dfx data!')
                    msg['error'] = 'All input dfx are no numeric columns, Please check your input dfx data!'
                    return  {'result':'', 'msg':msg},pd.DataFrame()
                
                
                else:
                    
                    if x_cate_cols != []:
                        logging.warning('input dfx has non-numeric columns: %s, will ignore these columns!' % x_cate_cols)
                    
                        msg['warning'] = 'input dfx has non-numeric columns: %s, will ignore these columns!' % x_cate_cols
                    
                    
                    name = tsy.name
                    
                    dfu = dfx[x_numer_cols].join(tsy)
                    m = dfu.groupby(name).mean().T
                    s = dfu.groupby(name).std().T

                    def change(ts):
                        v= []
                        for i in ts.index:
                            r = '%s±%s' % (round(ts.loc[i],2),round(s[ts.name].loc[i],2))
                            v.append(r)
                        return pd.Series(v,index=ts.index)


                    m1 = m.apply(change)
                    
                    
                    

                    rs = []
                    for i in x_numer_cols:
                        
                        
                        dd = [dfu[dfu[tsy.name] == c][i] for c in tsy.unique()]
                        
                        F, p = levene(*dd)
                        
                        columns = ['F-值', 'p-值']
                        rs.append(pd.DataFrame([F,p],index=columns,columns=[i]).T)

                    
                    
                    res = m1.join(pd.concat(rs))
                    
    
                    dfres = res   
                    return {'tables': [{'table_json': dfres.reset_index().to_json(orient='index'),
                            'table_html': dfres.to_html(),
                            'table_info': '生成的字段之间的相关系数和p-值表',
                            'chart': ['heatmap', 'line', 'bar']}],
                            'conf': self.get_info(),
                            'msg': msg}, [{'table_df': dfres, 'label': '生成的字段之间的相关系数和p-值表'}]
            
        
        
            

if __name__ == '__main__':
    
    #读取数据
    
    
    
    df =load_MedExp()

    testdata = load_MedExp()
    dfx = df[['med','age','idp']]
    
    tsy = df.health
    #tsy = tsy[tsy.isin(['good', 'excellent'])]
    
    
    #类的初始化
    O = HOVTest()

    #打印该类描述的信息
    print(O.get_info().get('description'))
    
    #执行运算，传入tsx、tsy参数
    dict_res = O.run(dfx,tsy)
    
    #获取返回的字典
    dict_res.get('result')
