#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 10:34:14 2018

@author: shenwanxiang
"""

from sklearn.decomposition import PCA as skl_pca
import pandas as pd

from utils.pandastool import ParseDFtypes
from utils.modelbase import ModelBase
#import numpy as np
import coloredlogs,logging
coloredlogs.install()



class PCA(ModelBase):

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
        
        n_components: int, default: 3
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
        
        self._id_ = model_id
        self._limitation_ = model_limiation
        self.n_components = n_components
        
        
        
    def get_info(self):
        
        return {'id': self._id, 
                'name': self._name, 
                'description': self._description,
                'limited':self._limitation
                }
        


                
                
    
    def run(self, 
            dfx,
            n_components = 3): 

        
        self.n_components = n_components
        
        msg = {}
        

        
        
        x_numer_cols, x_cate_cols = ParseDFtypes(dfx)
        
        if x_numer_cols ==[]:
            logging.error('All input dfx are no numeric columns, Please check your input dfx data!')
            msg['error'] = 'All input dfx are no numeric columns, Please check your input dfx data!'
            return  {'result':pd.DataFrame(), 'msg':msg}
        
        
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
        
        return {'result':l, 'msg':msg, 'component':ff}


        
        
    
    
    
    
    
    

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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
            
  