#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 22:26:59 2019

@author: shenwanxiang
"""

#多重响应分析
#https://spssau.com/front/spssau/helps/advancedmethods/multipleresponse.html



import numpy as np
import pandas as pd

def core(x, y):
    
    
    '''
    x: pd.DataFrame(), Note: values must be 0 and 1  
    y: pd.Series
    '''
        
    df = x.join(y)
    '''
    
    def _value_counts_df(df):
        al = []
        for col in df.columns:
            if col == y.name:
                continue
            al.append(df[col].value_counts())
        return pd.concat(al, axis=1)
        
    '''
        
    tb1 = df.groupby(y.name).sum().T
    
    
    c = df.groupby(y.name).size()
    c = pd.Series(c.index.astype(str) + '(N=' + c.astype(str) + ')', index = c.index)
    tb1.columns = tb1.columns.map(c.to_dict())
    s = tb1.sum(axis=1)
    N = df.groupby(y.name).size().sum()
    tb1['汇总(N=%s)' % N] = s
    tb1.index.name = '项'
    
    
    tb2 = s.to_frame(name = 'N')
    s2 = tb2.sum().loc['N']
    tb2.loc['汇总'] = s2
    tb2['响应率'] = tb2['N']/s2
    
    tb2['响应率'] = tb2['响应率'].apply(lambda x: "{0:.2f}%".format(x*100))
    tb2['普及率'] = tb2['N']/N
    tb2['普及率'] = tb2['普及率'].apply(lambda x: "{0:.2f}%".format(x*100))

    return {'交叉汇总表':tb1, '多重响应表格':tb2}




if __name__ == '__main__':
    N = 117
    y_ = np.random.choice(a=['男', '女'], size=(N,))
    columns = ['多选题选项A', '多选题选项B', '多选题选项C', '多选题选项D']
    xa = []
    for col in columns:
        x_ = np.random.choice(a=[0, 1], size=(N,))
        xa.append(pd.Series(x_, name = col))
    x = pd.concat(xa, axis=1)
    y = pd.Series(y_, name = '性别')
    res  = core(x, y)
