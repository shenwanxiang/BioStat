#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 22:33:50 2019

@author: shenwanxiang
"""

#多分类Logit分析


import sys,os
sys.path.insert(0,'/Users/shenwanxiang/Desktop/smap/medical-learn/')

from MedLearn.utils.pandastool import ParseDFtypes,isCategory
from MedLearn.utils.modelbase import ModelBase
from MedLearn.dataset import load_MedExp


from MedLearn.docs import getDoc
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import roc_curve, auc

from io import StringIO

import pandas as pd
import numpy as np
import statsmodels.api as sm

import coloredlogs,logging
coloredlogs.install()


docfilename = os.path.basename(__file__).replace('.py','.md')
DOC = getDoc(docfilename)  

ABSTRACT = '''二元Logit回归分析用于研究X对于Y的影响关系，其中X通常为定量数据（如果X为定类数据，一般需要做虚拟(哑)变量设置），Y为二分类定类数据（Y的数字一定只能为0和1）'''





class advance_MultiLogReg(ModelBase):

    """
    
    
    方法
    -------
        get_info : 
            获取该模型的信息， 返回一个字典，包含‘id’和‘name’, 'description','limited'关键字
            含义分别为：模型的id, 模型的名称，模型的描述，模型的适用范围
        
        run:  
            参数
            ----------
            df: pandas DataFrame
                如果方法为‘pearson’，需要每列的数据都是数字型数据，不能是字符串或者object
            
            x: string
            
            y: string
            
            
            
            
    返回结果
    ----------        
        返回一个字典，带有‘result’关键字，其值为相关系数和p-value组成的dataframe
            
    """
    
    
    
    def __init__(self, 
                 model_id = None, 
                 model_limiation = None,
                 ):
        
        self._name_ = '二元Logit回归分析'

        
        
    def get_info(self):
        
        return {'id': self._id, 
                'name': self._name, 
                
                'info': self._description,
                'abstract':ABSTRACT,
                'doc':DOC,
                'limited':'如果方法为‘pearson’，需要输入的每列的数据都是数值型数据，不能是字符串或者object',
                'args':[{"id": "x", "name": "分析项x",'type':'dataframe', 'requirement':'每个元素必须包含在df的列中'},
                        {"id": "y", "name": "分析项y",'type':'dataframe', 'requirement':'每个元素必须包含在df的列中'}],
                
                'extra_args':[ { 'id': "method", 
                                'default': 'pearson',
                                'name':"计算方法", 
                                'type': "select",
                                'choice':[{'value':'kendall', 'label':'kendall相关系数'},
                                         {'value':'spearman','label':'spearman相关系数'},
                                         {'value':'pearson', 'label':'pearson相关系数'}]
                                },
                
                                {'id': "crosstab", 
                                'default': 'False',
                                'name':"生成交叉表", 
                                'type': "select",
                                'choice':[{'value':'False', 'label':'否'},
                                          {'value':'True', 'label':'是'}]
                                }
                            ]
            }
    
    
        
    def run(self, df, x, y, *args):

        '''
        
        x:
        y: y的唯一个数只能为2
        
        '''
        msg = {}

        dfx = df[x].reset_index(drop=True)
        dfx = sm.add_constant(dfx, prepend=True)
        dfx = dfx.rename(columns={'const':'截距'})
        
        numeric_cols,category_cols = ParseDFtypes(dfx)
        
        target = y[0]
        tsy= df[target].reset_index(drop=True)
        
        
        types = list(tsy.unique())
        types.sort()
        
        
        
        # build init model
        model = sm.MNLogit(tsy, dfx[numeric_cols])
        res = model.fit()
        
        
        #predict result        
        prediction_probs = res.predict()
        tsy_predict = pd.DataFrame(prediction_probs).apply(lambda x: types[x.idxmax()],axis=1)
        tsy_predict.name = '预测的' + tsy.name
        df_predict_result = pd.concat([tsy,tsy_predict],axis=1)
        df_dumps = pd.get_dummies(tsy)[types]
        df_prediction_probs = pd.DataFrame(prediction_probs,columns=types)
        #fpr, tpr, thresholds =roc_curve(tsy.map(myd), prediction_probs)        
        
        #report
        df_report = pd.DataFrame(list(precision_recall_fscore_support(tsy, 
                                                                      tsy_predict)),
                                 index=['召回率','精确度',  'F1-值', '样本个数'],
                                columns=types).T.round(5)
        
        
        #confusion matrix
        df_confusion_matrix = pd.DataFrame(res.pred_table(),index = types,columns = types)
        
        
        
        #roc
        roc_res_dict = {}
        for i in types:
            fpr, tpr, thresholds =roc_curve(df_dumps[i], df_prediction_probs[i])
            tpr = pd.DataFrame(tpr, columns=['真阳性率'])
            fpr = pd.DataFrame(fpr, columns=['假阳性率'])
            
            roc_auc = auc(fpr, tpr)
            desc = "（曲线下面积:%0.3f）" % roc_auc
            key = '%s_%s' % (i, desc)
            r = fpr.join(tpr).T.reset_index()
            roc_res_dict[key] = r
        
        
        
        #model description
        tables = res.summary().tables
        df_list = [pd.read_html(StringIO(t.as_html()))[0] for t in tables ]
        dfinfo1 = df_list[1].fillna('Variables').set_index(0)
        t = []
        for i in res.params.columns:
            odd = np.exp(res.params[[i]]).round(5)
            odd.columns=['or值']
            odd = odd.T.reset_index().T
            t.append(odd)
        dft = pd.concat(t)
        dft.index = dfinfo1.index
        dft.columns = [7]
        df_res = dfinfo1.reset_index().join(dft.reset_index(drop=True))
        df_res = df_res.set_index(0)
        change_lst = list(set(dfinfo1.index) - set(dfx.columns))
        for i in change_lst:
            df_res.loc[i] = ['回归系数', '标准误差','Z值','p值', '95%CI(下限)','95%CI(上限)','or值']
            
        
        
        df_report = df_report.append(df_report.sum().to_frame(name='总和/平均').T)
        df_report['召回率'].loc['总和/平均'] = df_report['召回率'].loc['总和/平均']/2
        df_report['F1-值'].loc['总和/平均'] = df_report['F1-值'].loc['总和/平均']/2
        df_report = df_report.T
        df_report['name'] = ['模型效果','模型效果','模型效果','样本量']
        
        
        df_confusion_matrix = df_confusion_matrix.append(df_confusion_matrix.sum().to_frame(name='总和/平均').T)
        df_confusion_matrix = df_confusion_matrix.T
        df_confusion_matrix['name'] = '混淆矩阵'
        df_confusion_matrix = df_confusion_matrix.append(df_report).reset_index().set_index(['name','index'])
        df_confusion_matrix = df_confusion_matrix.T
        df_confusion_matrix.columns.names=[None, None]
        
        
        df_predict_result = df_predict_result.round(5)
        df_confusion_matrix = df_confusion_matrix.round(5)
        
        df_description = df_res.round(5)

        tt = []
        for i in roc_res_dict.keys():
            df = roc_res_dict[i]
            d = {'table_info':i,'table_json':df.to_json(),
             'table_html':df.to_html(), 'chart':['scatter']} 
            
            tt.append(d)
            
            
        #self.df_confusion_matrix = df_confusion_matrix
        #self._df_description = df_description
        return {'tables':[
                        {'table_info':'多元Logit回归分析结果汇总',
                        'table_json':df_description.reset_index().to_json(),
                        'table_html':df_description.to_html(),
                        'chart':['line','bar']},
                        {'table_info':'多元Logit回归预测效果汇总:',
                        'table_json':df_confusion_matrix.T.reset_index().to_json(),
                        'table_html':df_confusion_matrix.to_html(),
                        'chart':[]}] + tt,
                'conf':self.get_info(),
                'msg':msg}, [{'table_df':df_predict_result,'label':'实际值与预测值'}]
        
        
        
conf =  advance_MultiLogReg().get_info()


if __name__ == '__main__':
    
    #读取数据

    df = load_MedExp()
    x = ['med', 'lc', 'lpi', 'fmde', 'ndisease', 'linc', 'lfam', 'educdec','age']
    #因为二元Logit分析，要求输入的y为2分类的数据，所以y可以分为两种情况0，1的时候适用
    y = ['health']

    #类的初始化

    C = advance_MultiLogReg()
    #打印该类描述的信息
    print(conf)
    
    extra_args={'method':'pearson', 'crosstab':False}    
    
    #执行运算，传入tsx、tsy参数
    cal_results = C.run(df,x,y,extra_args)
    
    #获取返回的字典
    cal_results