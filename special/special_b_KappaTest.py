#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 2 20:07:26 2018

@author: charleshen

Kappa test
"""



import sys
sys.path.insert(0,'/Users/shenwanxiang/Desktop/') #改成你的路径

from THU_STATS.dataset import load_MedExp, load_SPSS
from THU_STATS.utils.modelbase import ModelBase
from THU_STATS.utils.pandastool import isCategory, isSeries
from THU_STATS.docs import common_doc


from statsmodels.stats.inter_rater import cohens_kappa
import pandas as pd





#filename = os.path.basename(__file__)
filename = 'special_b_KappaTest.py'
ABSTRACT = '''在诊断试验中，研究者希望考察不同的诊断方法在诊断结果上是否具有一致性。如：评价两种诊断试验方法对同一个样本或研究对象的化验结果的一致性。此时，Kappa值可以作为评价判断的一致性程度的指标。'''
DOC = common_doc.DOC(filename=filename)

def core(tsx,tsy,weights = None,  method = '简单kappa'):
    
    '''
    input
    --------
      tsx: 定类型数据， 和tsy的unique应该有相同的值
      tsy: 定类型数据
      weights: 加权项（可选）
      method: {"简单kappa", 
              "加权kappa（线性cohens）",
              "加权kappa（二次cohens）" }, 方法，下拉菜单
    '''
    
    
    table = pd.crosstab(tsx,tsy)
    
    s = list(set(table.columns) & set(table.index))
    
    table = table.loc[s][s]
    
    
    
    
    if method == '简单kappa':
        res = cohens_kappa(table, 
                           weights = None, 
                           return_results=True)
        
        
    elif method == '加权kappa（线性cohens）': 
        res = cohens_kappa(table, 
                           wt = 'linear', 
                           weights = weights, 
                           return_results=True)
        
        
    elif method == '加权kappa（二次cohens）': 
        res = cohens_kappa(table, 
                           wt = 'quadratic', 
                           weights = weights,
                           return_results=True)
        
        
    columns = {'名称':'%s & %s' % (tsx.name, tsy.name) ,
               'Kappa值':res.get('kappa'),
               'Z值':res.get('z_value'),
               'P值':res.get('pvalue_two_sided'),
               '95%CI(下限)':round(res.get('kappa_low'),5),
               
               '95%CI(上限)':round(res.get('kappa_upp'),5),
               
               'ASE':round(res.get('std_kappa0'),5),
              '类型':res.get('kind')}
        
    return pd.DataFrame([columns]).set_index('名称')


df = load_SPSS()
tsx = df['【系统】平台偏好_定类']
tsy = df['【系统】性别_定类']
core(tsx,tsy)
