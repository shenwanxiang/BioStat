#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 10:34:14 2018

@author: shenwanxiang
"""

from sklearn.cluster import KMeans
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

import pandas as pd

from utils.pandastool import ParseDFtypes
from utils.modelbase import ModelBase



import coloredlogs,logging
coloredlogs.install()



class Cluster(ModelBase):

    """
    聚类分析: 具体聚类方法为K均值聚类,输入需要事先指定类别的个数，默认n_culsters = 3,
    其次需要输入数字型的dfx。执行完聚类后，系统基于生成的类别进行方差分析，
    返回一个由类别对应的方差分析组成的dataframe在‘result’关键字中, 聚类的类别结果在‘cluster’中；

    
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
        
        n_clusters: int, default: 3
           定义需要聚的类的个数 
        
        返回结果
        ----------        
            返回一个字典，带有‘result’关键字，为返回的聚类结果，带有
            'msg'关键字为字典，log信息包括error,warning, info等
            
    """
    
    
    
    def __init__(self, 
                 model_id = None, 
                 model_limiation = None,
                 n_clusters = 3
                 ):
        
        self._id_ = model_id
        self._limitation_ = model_limiation
        self.n_clusters = n_clusters
        
        
        
    def get_info(self):
        
        return {'id': self._id, 
                'name': self._name, 
                'description': self._description,
                'limited':self._limitation
                }
        


                
                
    
    def run(self, 
            dfx,
            n_clusters = 3): 

        
        self.n_clusters = n_clusters
        
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

        y = KMeans(n_clusters=n_clusters, init='k-means++', random_state=17).fit_predict(dfu)
        
        y = pd.Series(y,index = dfu.index, name='类别')
        
        dfu = dfu.join(y)
        
        
        d = dfu.groupby('类别').size().to_dict()
        
        for k, v in d.items():
            d[k] = '类别%s(N=%s)' %(k,v)        
                
        dfu['类别'] = dfu['类别'].map(d)
        
        
        m = dfu.groupby('类别').mean().T
        s = dfu.groupby('类别').std().T
        
        
        def change(ts):
            v= []
            for i in ts.index:
                r = '%s±%s' % (round(ts.loc[i],2),round(s[ts.name].loc[i],2))
                v.append(r)
            return pd.Series(v,index=ts.index)


        m1 = m.apply(change)
        
        
        rs = []
        for i in x_numer_cols:
            model = ols('%s ~ %s' % (i, '类别') ,dfu).fit()
            anovat = anova_lm(model)
            anovat.columns = ['自由度', '平方和', '均方和', 'F-值', 'p-值']
            rs.append(anovat[['F-值', 'p-值']].round(3).iloc[0].to_frame(name=i).T)

        
        
        res = m1.join(pd.concat(rs))
        
        return {'result':res, 'msg':msg, 'cluster':dfu}


        
        
    
    
    
    
    
    
    
    
    
    

if __name__ == '__main__':
    
    #读取数据
    from dataset import load_MedExp
    
    
    df =load_MedExp()

    
    
    
    #类的初始化
    C = Cluster()

    #打印该类描述的信息
    print(C.get_info().get('description'))
    
    #执行运算，传入tsx、tsy参数
    res = C.run(df,n_clusters=10)
    
    #获取返回的字典
    res.get('result')    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
            
  