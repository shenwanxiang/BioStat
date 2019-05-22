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

from ..utils.pandastool import ParseDFtypes
from ..utils.modelbase import ModelBase



import coloredlogs,logging
coloredlogs.install()

ABSTRACT = '''相关分析用于研究定量数据之间的关系情况,包括是否有关系,以及关系紧密程度等.此分析方法通常用于回归分析之前;相关分析与回归分析的逻辑关系为:先有相关关系,才有可能有回归关系。'''


class advance_a_Cluster(ModelBase):

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
        
        self._name_ = '聚类分析方法'
        
        
        
    def get_info(self):
        
        return {'id': self._id, 
                'name': self._name,
                'info':self._description, 
                'abstract': ABSTRACT,
                'doc': self._doc,
                'limited':'',
                'args': [{'id': 'x', 'name': '分析项x', 'type': 'dataframe', 'requirement': '每个元素必须包含在df的列中'}],
                'extra_args': [{'id': 'n_clusters',
                                'default': 3,
                                'name': "计算方法",
                                'type': "inputNumber"
                                },
                               ],
                'schema': {
                    'type': 'object',
                    'properties': {
                        'n_clusters': {'type': 'number'}
                    },
                }
                }
        


                
                
    
    def run(self, 
            df,
            x,
            y,
            extra_args={'n_clusters':3}):
        self.n_clusters = int(extra_args.get('n_clusters'))
        dfx  = df[x]        
        
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

        y = KMeans(n_clusters=self.n_clusters, init='k-means++', random_state=17).fit_predict(dfu)
        
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
        df_res = res
        return {'tables': [{'table_json': df_res.reset_index().to_json(orient='index'),
                            'table_html': df_res.to_html(),
                            'table_info': '生成的字段之间的相关系数和p-值表',
                            'chart': ['heatmap', 'line', 'bar']},
                            {'table_json': dfu.reset_index().to_json(orient='index'),
                            'table_html': dfu.to_html(),
                            'table_info': '生成的字段之间的相关系数和p-值表',
                            'chart': ['heatmap', 'line', 'bar']}],
                'conf': self.get_info(),
                'msg': msg}, [{'table_df': df_res, 'label': '生成的字段之间的相关系数和p-值表'},{'table_df': dfu, 'label': '生成的字段之间的相关系数和p-值表'}]

        # return {'result':res, 'msg':msg, 'cluster':dfu}


        
        
    
    
    
    
    
    
    
    
    
    

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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
            
  