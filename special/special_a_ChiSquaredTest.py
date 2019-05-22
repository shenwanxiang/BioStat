#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 2 20:07:26 2018

@author: charleshen

Chi-square test
"""


import sys
sys.path.insert(0,'/home/shenwanxiang/wuhan_software/medical-learn') #改成你的路径

import os
import pandas as pd
import scipy.stats as stats
import numpy as np


from ..dataset import load_MedExp
from ..utils.modelbase import ModelBase
from ..utils.pandastool import isCategory, isSeries
from ..docs import common_doc
from ..utils import logtools

#filename = os.path.basename(__file__)
filename = 'special_a_ChiSquaredTest.py'
ABSTRACT = '''卡方检验用于分析定类数据与定类数据之间的关系情况.例如不同减肥治疗方式对于减肥的帮助情况（胆固醇水平）。'''
DOC = common_doc.DOC(filename=filename)



def core(tsx,tsy,method = 'pearson'):

    
    '''
    input
    --------
      tsx: 定类型数据
      tsy: 定类型数据
      method: 方法，下拉菜单
    '''

    methods = {"pearson":"Pearson卡方检验", 
               "freeman-tukey":"Freeman-Tukey卡方检验" , 
               "log-likelihood":"最大似然卡方[G-test](https://en.wikipedia.org/wiki/G-test)", 
               "neyman":"Neyman卡方检验" , 
              "fisher":"fisher精确卡方检验"}

    crosstab = pd.crosstab(tsx, tsy)
    crosstab2 = pd.crosstab(tsx, tsy,margins = True)
    crosstab2 = crosstab2.rename(columns={'All':'总计'}, index={'All':'总计'})
    
    msg = {}
    
    if not isCategory(tsx):
        msg['error'] = '输入的%s不是类别型数据（category data)\n' % tsx.name
        return pd.DataFrame(), msg
        
    if not isCategory(tsy):
        msg['error'] = '输入的%s不是类别型数据(category data)\n' % tsy.name
        return pd.DataFrame(),msg
        
    if method not in methods.keys():    
        logtools.print_error('不支持的方法:%s，只支持以下方法：%s' % (method, list(methods.keys()) ))
        
    if method == "fisher":
        odd_rates, p = stats.fisher_exact(crosstab)
        expected = stats.contingency.expected_freq(crosstab)
        chi2 = '--'
        
    else:
        chi2, p, dof, expected = stats.chi2_contingency(crosstab, lambda_ = method)   

    dfe = pd.DataFrame(expected,columns=tsy.unique(),index=tsx.unique()).round(3)
    dfte = crosstab.astype(str) +' (' +  dfe.astype(str) + ')'
    dfte['总计'] =  crosstab2['总计']
    dfte.loc['总计'] = crosstab2.loc['总计'] 
    dfte['检验方法'] = method
    dfte['卡方统计量'] = chi2
    dfte['p-值'] = p
    dfte.index.name = '类别'
    return dfte.reset_index().set_index(['检验方法','卡方统计量','p-值','类别']), msg



#df = load_MedExp()
#tsx = df.black
#tsy = df.health
#core(tsx,tsy)[0]    



class ChiSquareCrossTab(ModelBase):

    """基于交叉列联表的卡方检验方法，适用于定类（pandas dtypes: category和bool）数据，
    如果非定类数据，则根据指定的bins参数，将定量数据转化为定类数据，执行run需要输入tsx,tsy
    的数据参数，分别代表X和y,类型为pandas Series,只含有一列数据，返回的结果为一个json，
    其中的table是类型的交叉列联表，其中的result是卡方检验的结果参数，包含了卡方值χ2，p值，系数Cramer’s V

    方法
    -------
    get_info :
        获取该模型的信息， 返回一个字典，包含‘id’和‘name’, 'description','limited'关键字
        含义分别为：模型的id, 模型的名称，模型的描述，模型的适用范围

    run:
        参数
        ----------
        tsx: pandas Series
            输入的分析项X, 只能包含一列

        tsy:pandas Series
            输入的分析项Y，只能包含一列

        bins: int, default:10
            将定量型数据转化为定类的参数

        返回结果
        ----------
            返回一个字典，带有‘result’关键字，其值为具有muti-index的pandas dataframe
    """

    def __init__(self,
                 model_id=None,
                 model_limiation=None,
                 bins=10
                 ):

        self._name_ = '卡方检验方法'

    def get_info(self):

        return {'id': self._id,
                'name': self._name,
                'info': self._description,
                'abstract': ABSTRACT,
                'doc': DOC,
                'limited': '',
                'args': [{"id": "x", "name": "分析项x", 'type': 'series', 'requirement': '每个元素必须包含在df的列中'},
                         {"id": "y", "name": "分析项y", 'type': 'series',
                             'requirement': '每个元素必须包含在df的列中'}
                         ],
                'extra_args': [{'id': "bins",
                                'default': 10,
                                'name': "计算方法",
                                'type': "input",
                                },


                               ]
                }

    def run(self,
            df, x, y, extra_args={'bins': 10}, method = 'pearson'):

        #msg={'error':None,'warning':None}

        tsy = df[x]
        tsx = df[y]
        tsy = tsy.reset_index(drop=True)
        tsx = tsx.reset_index(drop=True)

        msg = {}

        xl = len(tsx)
        yl = len(tsy)
        if xl != yl:
            msg['error'] = '输入的tsx的长度为:%s 不等于输入的tsy的长度: %s !\n ' % (xl, yl)
            return {'result': pd.DataFrame(), 'msg': msg}

        self.bins = extra_args.get('bins')
        if not isSeries(tsy) & isSeries(tsx):
            msg['error'] = 'tsx或者tsy不是 pandas Series 数据类型!\n'
            return {'result': pd.DataFrame(), 'msg': msg}

        else:
            if not isCategory(tsy):
                tsy = pd.cut(tsy, bins=self.bins)
                msg['warning'] = '列tsy不是定类（category）数据, 将强制通过bins:%d为转化为定类型数据\n' % self.bins

            if not isCategory(tsx):
                tsx = pd.cut(tsx, bins=self.bins)
                if msg.get('warning'):
                    msg['warning'] = msg['warning'] + '列tsx不是定类（category）数据, 将强制通过bins:%d为转化为定类型数据\n' % self.bins
                else:
                    msg['warning'] = 't列tsx不是定类（category）数据, 将强制通过bins:%d为转化为定类型数据\n' % self.bins


            dfres, msg1 = core(tsx,tsy, method)
            
            msg =  {**msg, **msg1}
            
            return {'tables': [{'table_json': dfres.T.reset_index().to_json(orient='index'),
                                'table_html': dfres.to_html(),
                                'table_info': '卡方检验分析结果',
                                'chart': ['heatmap', 'line', 'bar']}],
                    'conf': self.get_info(),
                    'msg': msg}, [{'table_df': dfres, 'label': '卡方检验分析结果'}]


if __name__ == '__main__':

    #读取数据

    testdata = load_MedExp()
    tsx = testdata['sex']
    tsy = testdata['idp']

    #类的初始化
    c = ChiSquareCrossTab()

    #打印该类描述的信息
    print(c.get_info().get('description'))

    #执行运算，传入tsx、tsy参数
    res = c.run(tsx, tsy)

    #获取返回的字典
    res.get('result')
