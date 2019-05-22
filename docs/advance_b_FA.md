#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 10:34:14 2018

@author: shenwanxiang
"""

from factor_analyzer import FactorAnalyzer
import pandas as pd

from utils.pandastool import ParseDFtypes
from utils.modelbase import ModelBase



import coloredlogs,logging
coloredlogs.install()



class FactorAnalysis(ModelBase):

    """
    因子分析:(探索性因子分析)用于探索分析项(定量数据)应该分成几个因子(变量),用户可自行设置因子个数,默认为3；
    实际应用时，可以使用相关性矩阵进行验证变量之间的关系，如果相关系数小于0.3，那么变量间的共性较小，不适合使用因子分析
    返回一个因子分析组成的dataframe在‘result’关键字中，因子得分在‘factor’中；

    
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
        
        n_factors: int, default: 3
           定义需要聚的因子的个数 
        
        返回结果
        ----------        
            返回一个字典，带有‘result’关键字，为返回的因子分析结果，带有
            'msg'关键字为字典，log信息包括error,warning, info等
            
    """
    
    
    
    def __init__(self, 
                 model_id = None, 
                 model_limiation = None,
                 n_factors = 3
                 ):
        
        self._id_ = model_id
        self._limitation_ = model_limiation
        self.n_factors = n_factors
        
        
        
    def get_info(self):
        
        return {'id': self._id, 
                'name': self._name, 
                'description': self._description,
                'limited':self._limitation
                }
        


                
                
    
    def run(self, 
            dfx,
            n_factors = 3): 

        
        self.n_factors = n_factors
        
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




        
        
        fa = FactorAnalyzer()        
        fa.analyze(dfu, n_factors, rotation=None)        
        l = fa.loadings
        c = fa.get_communalities() 
        s = fa.get_scores(dfu)

        l.columns= ['因子%s荷载系数' % (i+1) for i in range(n_factors)]
        c.columns=['共同度']
        s.columns = ['因子%s' % (i+1) for i in range(n_factors)]
        
        
        res = l.join(c)
        
        
        
        return {'result':res, 'msg':msg, 'factor':s}


        
        
    
    
    
    
    
    
    
    
    
    

if __name__ == '__main__':
    
    #读取数据
    from dataset import load_MedExp
    
    
    df =load_MedExp()

    
    
    
    #类的初始化
    C = FactorAnalysis()

    #打印该类描述的信息
    print(C.get_info().get('description'))
    
    #执行运算，传入tsx、tsy参数
    res = C.run(df,n_factors=4)
    
    #获取返回的字典
    res.get('result')    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
            
  