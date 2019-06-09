#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 22:31:04 2019

@author: shenwanxiang
"""

#曲线回归分析
#https://spssau.com/front/spssau/helps/advancedmethods/curregression.html

##https://stackoverflow.com/questions/3433486/how-to-do-exponential-and-logarithmic-curve-fitting-in-python-i-found-only-poly


import numpy as np
import pandas as pd
import statsmodels.api as sm
from io import StringIO
from statsmodels.formula.api import ols



def core(x, y, curve_type = '二次曲线'):
    '''
    x: pd.Series
    y: pd.Series
    curve_types = ['二次曲线', '三次曲线', '对数曲线', '指数曲线', '复合曲线', '增长曲线', 'S型曲线']
    '''

    df = x.to_frame().join(y)
    df = sm.add_constant(df, prepend=True)
    df = df.rename(columns = {'const':'常数项'})
    
    if curve_type == '二次曲线':
        formula = '%s ~ %s + %s + %s**2' % (y.name, '常数项', x.name, x.name)
    
    if curve_type == '三次曲线':
        formula = '%s ~ %s + %s + %s**2 + %s**3' % (y.name, '常数项', x.name, x.name, x.name)

    if curve_type == '对数曲线':
        formula = '%s ~ %s + np.log(%s)' % (y.name, '常数项', x.name)  
        
    if curve_type == '指数曲线':
        formula = 'np.log(%s) ~ np.log(%s) + %s' % (y.name, '常数项', x.name)  
    
    if curve_type == '复合曲线':
        formula = 'np.log(%s) ~ np.log(%s) + np.log(%s)*%s' % (y.name, '常数项', '常数项', x.name)  
        
    if curve_type == '增长曲线':
        formula = 'np.log(%s) ~ %s + %s' % (y.name, '常数项', x.name)  
            
    if curve_type == 'S型曲线':
        def _r(x):
           return 1/x
        formula = 'np.log(%s) ~ %s + _r(%s)' % (y.name, '常数项', x.name)  

    
    
            
    res = ols(formula, df).fit()
    tables = res.summary().tables
    df_list = [pd.read_html(StringIO(t.as_html()))[0] for t in tables ]

    td = {'R平方':res.rsquared, 
            '调整R方':res.rsquared_adj,
            '标准误':res.mse_model, 
            'AIC':res.aic, 
            'BIC':res.aic,
            '有效样本':res.nobs}
    tb1 = pd.Series(td).to_frame(name = '模型汇总').T
    
    
    
    tb2 = df_list[1].set_index(0).iloc[1:].loc[['Intercept', x.name]]
    tb2.columns = ['回归系数', '标准误差SE', 'Z值','p值', '95%CI(下限)','95%CI(上限)']
    tb2 = tb2.rename(index={'Intercept':'常数'})
    
    tb3 = pd.Series({'自由度':res.df_model, 'F-值':res.fvalue, 'p-值':res.f_pvalue}).to_frame(name = '回归总体ANOVA')
    
    
    
    s4 = pd.Series(res.predict(), name = str(y.name) + '-拟合')
    if curve_type in ['指数曲线', '复合曲线', '增长曲线', 'S型曲线']:
        s4 = np.exp(s4)
    
    tb4 = y.to_frame().join(s4)
    
    return {'模型汇总':tb1, '回归系数汇总表':tb2, 'ANOVA表格':tb3, '实际值与拟合值':tb4}


if __name__ == '__mian__':
    
    def func(x, a, b, c):
        return a * np.exp(-b * x) + c
    x = np.linspace(1, 5, 50)
    y = func(x, 2.5, 1.3, 0.5)
    
    x = pd.Series(x, name = '时间')
    y = pd.Series(y, name = '药物浓度')

    rs = core(x, y, curve_type =  '对数曲线')
    rs.get('实际值与拟合值').plot()