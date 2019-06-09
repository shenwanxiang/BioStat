#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 18:32:10 2019

@author: shenwanxiang
"""

##多因素方差分析


from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import statsmodels.api as sm
import pandas as pd


def core(x, y, typ = 2):
    '''
    x: dataframe
    y:series
    type: 2,3 : ['二阶效应', '三阶效应']
    
    '''

    dfu = y.to_frame().join(x)
    name = y.name
    rs= []
    for c in x.columns:
        m = dfu.groupby(c)[name].mean().to_frame(name='平均值').round(2)
        s = dfu.groupby(c)[name].std().to_frame(name='标准差').round(2)
        n = dfu.groupby(c)[name].size().to_frame(name='样本量')
        dfr = pd.concat([m,s,n],axis=1).reset_index().rename(columns={c:'标签'})
        dfr['分析项'] = c
        
        dfr = dfr.set_index(['分析项','标签'])
        rs.append(dfr)
        
    tb1 = pd.concat(rs)
    
    
    
    dfu = sm.add_constant(dfu, prepend=True).rename(columns={'const':'截距'})
    cols = list(dfu.columns)
    cols.remove(name)
    s1 = ' + '.join(cols)
    formula = '%s ~ %s' % (name, s1)
    df_fit = ols(formula, data=dfu).fit()
    dfres = anova_lm(df_fit, typ=typ)
    dfres.columns = ['平方和', '自由度', 'F-值', 'p-值']
    dfres = dfres.rename(index={'Residual':'残差'})
    dfres.index.name = '差异源'



    res = {'数据统计结果':tb1, '多因素方差分析结果':dfres}
    return res


if __name__ == '__main__':
    
    
    import sys
    sys.path.insert(0,'/Users/charleshen/Desktop') #改成你的路径
    from THU_STAT.dataset import load_MedExp
        
        
    df =load_MedExp()
    x = df[['idp', 'sex', 'child', 'black']]
    y = df['med']
    res = core(x,y,typ=2)