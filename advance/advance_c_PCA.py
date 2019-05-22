#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 10:34:14 2018

@author: shenwanxiang
"""

from sklearn.decomposition import PCA as skl_pca
import pandas as pd

from ..utils.pandastool import ParseDFtypes
from ..utils.modelbase import ModelBase
#import numpy as np
import coloredlogs,logging
coloredlogs.install()


ABSTRACT = '''相关分析用于研究定量数据之间的关系情况,包括是否有关系,以及关系紧密程度等.此分析方法通常用于回归分析之前;相关分析与回归分析的逻辑关系为:先有相关关系,才有可能有回归关系。'''

class advance_c_PCA(ModelBase):

    """
    主成分分析用于对数据信息进行浓（降维）:用户可自行设置主成分个数,默认为3；
    返回一个主成分分析结果组成的dataframe在‘result’关键字中，每个成分得分在‘component’中；

    
    方法
    -------
    get_info : 
        获取该模型的信息， 返回一个字典，包含‘id’和‘name’, 'description','limited'关键字
        含义分别为：模型的id, 模型的名称，模型的描述，模型的适用范围

    run:  
        参数
        ----------
        dfx: pandas DataFrame
            X data, 只能是数字型定量数据，不能输入字符串
        
        n_components: int, default: 2
           主成分的个数 
        
        返回结果
        ----------        
            返回一个字典，带有‘result’关键字，为返回的因子分析结果，带有
            'msg'关键字为字典，log信息包括error,warning, info等
            
    """
    
    
    
    def __init__(self, 
                 model_id = None, 
                 model_limiation = None,
                 n_components = 3
                 ):
        
        self._name_ = '主成分分析方法'
        
        
        
    def get_info(self):
        
        return {'id': self._id, 
                'name': self._name, 
                'info': self._description,
                'abstract': ABSTRACT,
                'doc': self._doc,
                'limited':'',
                'args': [{'id': 'x', 'name': '分析项x', 'type': 'dataframe', 'requirement': '每个元素必须包含在df的列中'}],
                'extra_args': [{'id': 'n_components',
                                'default': 2,
                                'name': "计算方法",
                                'type': "inputNumber"
                                },
                               ],
                'schema': {
                    'type': 'object',
                    'properties': {
                        'n_components': {'type': 'number'}
                    },
                }
                }
        


                
                
    
    def run(self, 
            df,
            x,
            y,
            extra_args={'n_components':2}): 

        
        n_components = int(extra_args.get('n_components'))
        dfx = df[x]
        msg = {}
        

        
        
        x_numer_cols, x_cate_cols = ParseDFtypes(dfx)
        
        if x_numer_cols ==[]:
            logging.error('All input dfx are no numeric columns, Please check your input dfx data!')
            msg['error'] = 'All input dfx are no numeric columns, Please check your input dfx data!'
            return  {'result':pd.DataFrame(), 'msg':msg},pd.DataFrame()        
        
        else:
            
            if x_cate_cols != []:
                logging.warning('input dfx has non-numeric columns: %s, will ignore these columns!' % x_cate_cols)
            
                msg['warning'] = 'input dfx has non-numeric columns: %s, will ignore these columns!' % x_cate_cols
            

        
        dfu = dfx[x_numer_cols]




        
        
        clf = skl_pca(n_components=n_components)   
        res = clf.fit_transform(dfu)
        
        l = pd.DataFrame(clf.components_.T, index = dfu.columns)
        l.loc['方差解释率%'] = clf.explained_variance_ratio_
        l.columns=['主成分%s荷载系数' % (i+1) for i in range(n_components)]
        
        
        s = pd.Series(clf.score_samples(dfu),index = dfu.index,name='综合得分')
            
        r = pd.DataFrame(res, index = dfu.index)
        r.columns = ['第%s主成分' % (i+1) for i in range(n_components)]
        
        
        ff = r.join(s)
        df_res = ff
        df_res2 = l

        
        return {'tables': [{'table_json': df_res.reset_index().to_json(orient='index'),
                            'table_html': df_res.to_html(),
                            'table_info': '生成的字段之间的相关系数和p-值表',
                            'chart': ['heatmap', 'line', 'bar']},
                            {'table_json': df_res2.reset_index().to_json(orient='index'),
                            'table_html': df_res2.to_html(),
                            'table_info': '生成的字段之间的相关系数和p-值表',
                            'chart': ['heatmap', 'line', 'bar']}],
                'conf': self.get_info(),
                'msg': msg}, [{'table_df': df_res, 'label': '生成的字段之间的相关系数和p-值表'},
                {'table_df': df_res2, 'label': '生成的字段之间的相关系数和p-值表'}]
 

        
        
    
    
    
    
    
    

if __name__ == '__main__':
    
    #读取数据
    from dataset import load_MedExp
    
    df =load_MedExp()

    #类的初始化
    C = PCA()

    #打印该类描述的信息
    print(C.get_info().get('description'))
    
    #执行运算，传入tsx、tsy参数
    res = C.run(df,n_components=4)
    
    #获取返回的字典
    res.get('result')    
    res.get('msg')
    res.get('component')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
            
  