#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 22:32:14 2019

@author: shenwanxiang
"""

#典型相关分析
# https://spssau.com/front/spssau/helps/advancedmethods/caacorr.html

'''
典型相关分析用于研究一组X与另一组Y数据之间的相关关系情况。
它借助主成分分析思想，结合变量间的相关关系情况，
寻找出一个或少数几个综合变量（即典型变量）来替代原变量，
从而对两组变量关系集中到少数几对典型变量间的关系之上。

'''
from statsmodels.multivariate.cancorr import CanCorr
#from sklearn.cross_decomposition import CCA
import numpy as np
import pandas as pd



def core(x, y):
    '''
    x: pd.DataFrame()
    y: pd.DataFrame()
    
    '''
    
    cca = CanCorr(y,x)
    t = cca.corr_test()
    tb1 = t.stats
    tb1.columns = ['典型相关系数','wilks统计量', 'Num DF', 'Den DF', 'F-值', 'p']
    tb1.index.name = '典型变量'
    colsx = '典型变量-X' + tb1.index.astype(str)
    colsy = '典型变量-Y' + tb1.index.astype(str)
    
    tb1.index = ['典型相关对(X%s, Y%s)' % (i,i) for i in tb1.index.astype(str)]
    
    
    x_coef = pd.DataFrame(cca.x_cancoef, index = x.columns, columns = colsx)
    y_coef = pd.DataFrame(cca.y_cancoef, index = y.columns, columns = colsy)
    
    
    ## 典型变量X1 = -0.015*x1-0.014*x2-0.002*x3-0.009*x4
    x_typical_variables = x_coef.apply(lambda a: (a*x).sum(axis=1))
    y_typical_variables = y_coef.apply(lambda b: (b*y).sum(axis=1))
    
    
    ## 典型变量X1与x组4项的相关关系为载荷系数
    x_loadings = x.join(x_typical_variables).corr().loc[x.columns][x_typical_variables.columns]
    y_loadings = y.join(y_typical_variables).corr().loc[y.columns][y_typical_variables.columns]
    
    
    al = []
    for col in x_coef.columns:
        l = x_loadings[[col]]
        e = x_coef[[col]]
        e['名称'] = '系数'
        l['名称'] = '荷载'
        k = l.append(e)
        k.index.name = '变量'
        s = k.reset_index().sort_values(['变量', '名称'])
        s = s.set_index(['变量', '名称'])
        al.append(s)
        
    tb2 = pd.concat(al, axis=1)
    
    
    al3 = []
    for col in y_coef.columns:
        l = y_loadings[[col]]
        e = y_coef[[col]]
        e['名称'] = '系数'
        l['名称'] = '荷载'
        k = l.append(e)
        k.index.name = '变量'
        s = k.reset_index().sort_values(['变量', '名称'])
        s = s.set_index(['变量', '名称'])
        al3.append(s)
        
    tb3 = pd.concat(al3, axis=1)
    tb4 = x_typical_variables.join(y_typical_variables)
    
    
    res = {'典型成分的相关系数及显著性': tb1, 
             '典型系数和典型荷载系数(X)': tb2,
             '典型系数和典型荷载系数(Y)': tb3, 
             '典型变量': tb4}

    return res

if __name__ == '__main__':
    
    
    n = 500
    # 2 latents vars:
    l1 = np.random.normal(size=n)
    l2 = np.random.normal(size=n)
    
    latents = np.array([l1, l1, l2, l2]).T
    
    latentsy = np.array([l1, l1, l2, l2, l1]).T
    
    X = latents + np.random.normal(size=4 * n).reshape((n, 4))
    Y = latentsy + np.random.normal(size=5 * n).reshape((n, 5))
    
    x = pd.DataFrame(X, columns= ['x1', 'x2', 'x3', 'x4'])
    y = pd.DataFrame(Y, columns=['y1', 'y2', 'y3', 'y4', 'y5'])
    res = core(x, y)