#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 20:21:58 2018

@author: shenwanxiang
"""

import numpy as np
import itertools
import math
from scipy.stats import ttest_ind
import pandas as pd

from ..utils.pandastool import ParseDFtypes, isCategory, isSeries
from ..utils.modelbase import ModelBase
import coloredlogs,logging
coloredlogs.install()

ABSTRACT = '''相关分析用于研究定量数据之间的关系情况,包括是否有关系,以及关系紧密程度等.此分析方法通常用于回归分析之前;相关分析与回归分析的逻辑关系为:先有相关关系,才有可能有回归关系。'''

# 误差均方
def MSE(list_groups,list_total):
    sse=SSE(list_groups)
    mse=sse/(len(list_total)-1*len(list_groups))*1.0 
    return mse 

#sum of squares within group error,also know as random error   
def SSE(list_groups): 
    sse=0
    for group in list_groups:
        se=SE(group)
        sse+=se
    return sse

#one within group error,also know as random error
def SE(group):
    se=0
    mean1=np.mean(group)
    for i in group:
        error=i-mean1
        se+=error**2
    return se
     

def Combination(list_groups):
    combination= []
    for i in range(1,len(list_groups)+1):
        iter = itertools.combinations(list_groups,i)
        combination.append(list(iter))
    #需要排除第一个和最后一个
    return combination[1:-1][0]



#LSD(least significant difference)最小显著差异
def LSD(list_groups,list_total,sample1,sample2,a=0.05):
    mean1=np.mean(sample1)
    mean2=np.mean(sample2)
    distance=mean1-mean2
    #print("distance:",distance)
    #t检验的自由度
    #df=len(list_total)-1*len(list_groups)
    mse=MSE(list_groups,list_total)
    #print("MSE:",mse)
    
    
    #t_value=stats.t(df).isf(a/2)
    #p = 1 - stats.t.cdf(t_value, df=df)
    
    t_value,p = ttest_ind(sample1,sample2)
    
    lsd=t_value*math.sqrt(mse*(1.0/len(sample1)+1.0/len(sample2)))
    
    res = [mean1,mean2, distance, lsd, p]
    return pd.DataFrame(res, index=['(I)平均值', '(J)平均值','差值(I-J)','LSD统计量','P值'])





def Multiple_test(list_groups,list_total):
    #print("multiple test----------------------------------------------")
    combination=Combination(list_groups)
    
    a = []
    for pair in combination:
        a.append(LSD(list_groups,list_total,pair[0],pair[1]))
        
    return a
        



class advance_d_PostHocTest(ModelBase):

    """
    事后检验：用于分析定类数据与定量数据之间的关系情况
    例如研究人员想知道三组学生(本科以下,本科,本科以上,tsy)的智商平均值是否有显著差异.
    比如分析显示三组学生智商（tsx）有着明显的差异,那具体是本科以下与本科这两组之间,
    还是本科以下与本科以上两组之间的差异;即具体两两组别之间的差异对比,则称为事后检验; 
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
            返回一个字典，带有‘result’关键字，其值为按照tsy分组的均值、p-值等等系数组成的dataframe

    """
    
    
    
    def __init__(self,
                 model_id=None,
                 model_limiation=None,
                 ):

       self._name_ = '事后检验'
        
        
    def get_info(self):
        
        return {'id': self._id,
                'name': self._name,
                'info': self._description,
                'abstract': ABSTRACT,
                'doc': self._doc,
                'limited': '',
                'args': [{'id': 'x', 'name': '分析项x', 'type': 'dataframe', 'requirement': '每个元素必须包含在df的列中'}, {"id": "y", "name": "分析项y", 'type': 'deries', 'requirement': '每个元素必须包含在df的列中'}],
                'extra_args': []
                }

    
    
    def run(self, 
            df, 
            x,
            y,
            extra_args={}): 


            dfx = df[x]
            tsy = df[y[0]]
            
            msg = {}
            
            tsy = tsy.reset_index(drop=True)
            dfx = dfx.reset_index(drop=True) 
            
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
                    
                    
                    
                    

                    res = []
                    for i in x_numer_cols:

                        tsx = dfx[i]
                        lg = list(tsy.unique())
                        list_groups = [tsx[tsy==i].tolist() for i in lg]
                        list_total = tsx.tolist()
                        a = Multiple_test(list_groups,list_total)   
                        dfr = pd.concat(a,axis=1).T
                        dfr.index = [(i[0]+'(I)', i[1] + '(J)') for i in Combination(lg)]
                        
                        dfr['分析项'] = i
                        
                        dfrr = dfr.reset_index().set_index(['分析项','index'])
                        
                        res.append(dfrr)
                        
                    df_res = pd.concat(res)
                    
                    return {'tables': [{'table_json': df_res.reset_index().to_json(orient='index'),
                                        'table_html': df_res.to_html(),
                                        'table_info': '生成的字段之间的相关系数和p-值表',
                                        'chart': ['heatmap', 'line', 'bar']}],
                            'conf': self.get_info(),
                            'msg': msg}, [{'table_df': df_res, 'label': '生成的字段之间的相关系数和p-值表'}]
        



if __name__ == '__main__':
    
    #读取数据
    from dataset import load_MedExp
    
    
    df =load_MedExp()

    testdata = load_MedExp()
    dfx = df[['med','age','idp']]
    
    tsy = df.health
    #tsy = tsy[tsy.isin(['good', 'excellent'])]
    
    
    #类的初始化
    O = PostHocTest()

    #打印该类描述的信息
    print(O.get_info().get('description'))
    
    #执行运算，传入tsx、tsy参数
    dict_res = O.run(dfx,tsy)
    
    #获取返回的字典
    dict_res.get('result')



