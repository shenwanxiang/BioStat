#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 22:35:13 2019

@author: shenwanxiang
"""

import sys,os
sys.path.insert(0,'/Users/shenwanxiang/Desktop/smap/medical-learn/')

from MedLearn.utils.pandastool import ParseDFtypes,isCategory
from MedLearn.utils.modelbase import ModelBase
from MedLearn.dataset import load_MedExp
from MedLearn.docs import getDoc

import statsmodels.formula.api as smf

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

ABSTRACT = '''ridge回归分析用于研究X对于Y的影响关系，其中X通常为定量数据（如果X为定类数据，一般需要做虚拟(哑)变量设置），Y为二分类定类数据（Y的数字一定只能为0和1）'''





class RidgeLogReg(ModelBase):

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
    
    
        
    def run(self, df, x, y, extra_args = {'alpha':0.001}):

        
        alpha = extra_args.get('alpha')
        if not alpha:
            alpha = 0.001
            
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

        #convert dict
        myd={}
        myd_reverse={}
        lst = list(tsy.unique())
        for i,j in enumerate(lst):
            myd[j]=i
            myd_reverse[i]=j


        # build init model
        
        
        model = smf.OLS(tsy.map(myd), dfx[numeric_cols])
        res = model.fit_regularized(maxiter = 1000,
                                    alpha = alpha, #正则化系数
                                    L1_wt=0) #L1_wt 0为l2 loss, 1为l1 loss

        #predict result
        prediction_probs = res.predict()
        prediction_bins = pd.Series([1 if i >= 0.5 else 0 for i in prediction_probs],name='predicted_bins')
        tsy_predict = prediction_bins.map(myd_reverse)
        tsy_predict.name = '预测的' + tsy.name
        df_predict_result = pd.concat([tsy,tsy_predict],axis=1)


        #confusion matrix
        df_confusion_matrix = pd.DataFrame(confusion_matrix(tsy, tsy_predict),index = tsy.unique(),columns = tsy.unique())


        #report
        df_report = pd.DataFrame(list(precision_recall_fscore_support(tsy, 
                                                                      tsy_predict)),
                    index=['精确度', '召回率', 'F1-值', '样本个数']).T.round(5)

        df_report.index = df_report.index.map(myd_reverse)

        #roc
        fpr, tpr, thresholds =roc_curve(tsy.map(myd), prediction_probs)
        roc_auc = auc(fpr, tpr)
        logging.info("Area under the ROC curve : %f" % roc_auc)
        i = np.arange(len(tpr)) # index for df
        df_roc = pd.DataFrame({'假阳性率' : pd.Series(fpr, index=i),
                               '真阳性率' : pd.Series(tpr, index = i)})



        #model description
        tables = res.summary().tables
        df_list = [pd.read_html(StringIO(t.as_html()))[0] for t in tables ]
        dfinfo1 = df_list[1].fillna('Variables').set_index(0)
        dfinfo1 = dfinfo1.T.set_index('Variables').T
        dfinfo1.index.name = '项'
        dfinfo1.columns.name = '参数类型'
        dfinfo1.columns = ['回归系数', '标准误差','Z值','p值', '95%CI(下限)','95%CI(上限)']
        dfinfo1['or值'] = np.exp(res.params)
        df_description  = dfinfo1


        df_report = df_report.append(df_report.sum().to_frame(name='总和/平均').T)
        df_report['召回率'].loc['总和/平均'] = df_report['召回率'].loc['总和/平均']/2
        df_report['F1-值'].loc['总和/平均'] = df_report['F1-值'].loc['总和/平均']/2
        df_report = df_report.T
        df_report['name'] = ['模型效果','模型效果','模型效果','样本量']


        df_confusion_matrix = df_confusion_matrix.append(df_confusion_matrix.sum().to_frame(name='总和/平均').T)
        df_confusion_matrix = df_confusion_matrix.T
        df_confusion_matrix['name'] = ['混淆矩阵','混淆矩阵']
        df_confusion_matrix = df_confusion_matrix.append(df_report).reset_index().set_index(['name','index'])
        df_confusion_matrix = df_confusion_matrix.T
        df_confusion_matrix.columns.names=[None, None]


        df_predict_result = df_predict_result.round(5)
        df_confusion_matrix = df_confusion_matrix.round(5)
        df_roc = df_roc.round(5)
        df_description = df_description.round(5)

        
        #self._debug = df_confusion_matrix
        return {'tables':[
                        {'table_info':'Ringe回归分析结果汇总',
                        'table_json':df_description.to_json(),
                        'table_html':df_description.to_html(),
                        'chart':['line','bar']},
                        {'table_info':'Ringe回归预测效果汇总:',
                        'table_json':df_confusion_matrix.T.reset_index().to_json(),
                        'table_html':df_confusion_matrix.to_html(),
                        'chart':[]},                    
                        {'table_info':"ROC曲线（曲线下面积:%0.3f）" % roc_auc,
                        'table_json':df_roc.to_json(),
                        'table_html':df_roc.to_html(),
                        'chart':['scatter']},                              
                        ],
                'conf':self.get_info(),
                'msg':msg}, [{'table_df':df_predict_result,'label':'实际值与预测值'}]
        
        
        
conf =  RidgeLogReg().get_info()


if __name__ == '__main__':
    
    #读取数据

    df = load_MedExp()
    x = ['med', 'lc', 'lpi', 'fmde', 'ndisease', 'linc', 'lfam', 'educdec','age']
    
    y = ['child']

    #类的初始化

    C = RidgeLogReg()
    #打印该类描述的信息
    print(conf)
    
    extra_args={'method':'pearson', 'crosstab':False}    
    
    #执行运算，传入tsx、tsy参数
    cal_results = C.run(df,x,y,extra_args)
    
    #获取返回的字典
    cal_results