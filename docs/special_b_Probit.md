#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 14:59:28 2019

@author: shenwanxiang
"""

#https://www.statsmodels.org/dev/generated/statsmodels.discrete.discrete_model.Probit.html







import sys
sys.path.insert(0,'/Users/shenwanxiang/Desktop/') #改成你的路径


from THU_STATS.dataset import load_SPSS, load_MedExp
from THU_STATS.utils.modelbase import ModelBase
from THU_STATS.utils.pandastool import isCategory, isSeries
from THU_STATS.docs import common_doc

from statsmodels.discrete.discrete_model import Probit
import statsmodels.api as sm
from sklearn.metrics import (auc, classification_report, confusion_matrix,
                             precision_recall_fscore_support, roc_curve)


#filename = os.path.basename(__file__)
filename = 'special_b_Probit.py'
ABSTRACT = '''二元Probit回归分析用于研究X对于Y的影响关系，其中X通常为定量数据（如果X为定类数据，一般需要做虚拟(哑)变量设置），Y为二分类定类数据（Y的数字一定只能为0和1）'''
DOC = common_doc.DOC(filename=filename)




def core(tsy, dfx, map = {0:'非肺癌', 1: '肺癌'}):
    
    
    assert set(tsy.unique()) == {0,1}, 'Y值只能为0或1'
    
    
    dfx = sm.add_constant(dfx, prepend=True)
    dfx = dfx.rename(columns={'const':'截距'}) 
    p = Probit(tsy, dfx)
    res = p.fit()    
    summary2 = res.summary2()
    

    #predict result
    prediction_probs = res.predict()
    prediction_bins = pd.Series([1 if i >= 0.5 else 0 for i in prediction_probs],
                                name='predicted_bins',
                                index = tsy.index)
    tsy_predict = prediction_bins
    tsy_predict.name = '预测的' + tsy.name
    df_predict_result = pd.concat([tsy,tsy_predict],axis=1)


    #confusion matrix
    df_confusion_matrix = pd.DataFrame(confusion_matrix(tsy, tsy_predict),index = tsy.unique(),columns = tsy.unique())
    df_confusion_matrix.index = df_confusion_matrix.index.map(map)
    df_confusion_matrix.columns  = df_confusion_matrix.columns.map(map)
    
    #report
    df_report = pd.DataFrame(list(precision_recall_fscore_support(tsy, 
                                                                  tsy_predict)),
                index=['精确度', '召回率', 'F1-值', '样本个数']).T.round(5)

    df_report.index = df_report.index.map(map)

    #roc
    fpr, tpr, thresholds =roc_curve(tsy, prediction_probs)
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
                    {'table_info':'二元Logit回归分析结果汇总',
                    'table_json':'{}',
                    'table_html':df_description.to_html(),
                    'chart':['line','bar']},
                    {'table_info':'二元Logit回归预测效果汇总:',
                    'table_json':df_confusion_matrix.T.reset_index().to_json(),
                    'table_html':df_confusion_matrix.to_html(),
                    'chart':[]},                    
                    {'table_info':"ROC曲线（曲线下面积:%0.3f）" % roc_auc,
                    'table_json':df_roc.to_json(),
                    'table_html':df_roc.to_html(),
                    'chart':['scatter']},                              
                    ]}, 
    [{'table_df':df_predict_result,'label':'实际值与预测值'}]


