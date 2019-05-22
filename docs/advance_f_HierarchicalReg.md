#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 12:50:24 2018

@author: shenwanxiang
"""


from utils.pandastool import ParseDFtypes
from utils.modelbase import ModelBase
#from dataset import load_MedExp
from io import StringIO

import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor

import pandas as pd

import coloredlogs,logging
coloredlogs.install()




class HierarchicalReg(ModelBase):

    """
    数据的回归分析方法，要求输入一个list_dfx( list of dataframe),dfy(dataframe),其中dfy为一列数据，
    返回一个最小二乘的线性模型的参数dataframe，在‘result‘关键字中
    
    
    方法
    -------
    get_info : 
        获取该模型的信息， 返回一个字典，包含‘id’和‘name’, 'description','limited'关键字
        含义分别为：模型的id, 模型的名称，模型的描述，模型的适用范围

    run:  
        参数
        ----------
        list_dfx: list of pandas DataFrame
            需要dataframe 每列的数据都是数字型数据，不能是字符串或者object
        
        dfy: pandas DataFrame
            需要一列的数据都是数字型数据，不能是字符串或者object
            
            
        返回结果
        ----------        
            返回一个字典，带有‘result’关键字，其值为coef, p, r, VIF 等等系数组成的dataframe

            
    """
    
    
    
    def __init__(self, 
                 model_id = None, 
                 model_limiation = None,
                 ):
        
        self._id_ = model_id
        self._limitation_ = model_limiation

        
        
    def get_info(self):
        
        return {'id': self._id, 
                'name': self._name, 
                'description': self._description,
                'limited':self._limitation
                }
    
    
    def run(self, 
            list_dfx, 
            dfy,
            ): 

            
            dfy = dfy.reset_index(drop=True)
            
            dfx_list = [i.reset_index(drop=True) for i in list_dfx]
            
            
            res= []
            
            for i, dfx in enumerate(dfx_list):
                         
                #print(i)
                msg = {}
                
                xl = len(dfx)
                yl = len(dfy)
                if  xl != yl:
                    logging.error('the length of input X:%s is not equal the length of Y: %s ! ' % (xl,yl))
                    msg['error'] = 'the length of input X:%s is not equal the length of Y: %s ! ' % (xl,yl)
                    return  {'result':pd.DataFrame(), 'msg':msg}        
            
        
        
                if len(dfy.columns) != 1:
                    logging.warning('input DataFrame dfy has more than one columns, but only the first colum will be used!')
                    msg['warning'] = 'input DataFrame dfy has more than one columns, but only the first colum will be used!'
                    
                    _dfy = dfy[[dfy.columns[0]]]
                    
                else:
                    _dfy = dfy
                    
                    
                    
                    
                dfx = pd.concat(dfx_list[:i+1], axis=1)
                
                x_numer_cols, x_cate_cols = ParseDFtypes(dfx)
                y_numer_cols, y_cate_cols = ParseDFtypes(_dfy)
        
                if (x_numer_cols ==[]) | (y_numer_cols == []):
                    logging.error('All input DataFrame are no numeric columns, Please check your input data!')
                    
                    msg['error'] = 'All input DataFrame are no numeric columns, Please check your input data!'
                    dfmain =pd.DataFrame()
                    
                    return  {'result':dfmain, 'msg':msg}  
                    
                    
                else:
                    
                    
                    _dfx = dfx[x_numer_cols]
                    
                    X = sm.add_constant(_dfx, prepend=True)
                    X = X.rename(columns={'const':'常数'})
                    
                    y = _dfy
                    
                    f = smf.OLS(y, X).fit()
                    tables = f.summary().tables
        
                    df_list = [pd.read_html(StringIO(t.as_html()))[0] for t in tables ]
        
                    def parse_table02(m_inf):
                        df1 = m_inf[[0,1]]
                        df1.columns=['items','values'] 
                        df2 = m_inf[[2,3]]
                        df2.columns=['items','values'] 
                        dfinfo1 = df1.append(df2).dropna().set_index('items')  
                        return dfinfo1.T
        
                    dfinfo0 = parse_table02(df_list[0])
                    #dfinfo2 = parse_table02(df_list[2])
        
                    dfinfo1 = df_list[1].fillna('Variables').set_index(0)
                    dfinfo1 = dfinfo1.T.set_index('Variables').T
        
                    dfmain = dfinfo1[dfinfo1.columns[:4]]
        
                    dfad = dfinfo0[['R-squared:','Adj. R-squared:', 'F-statistic:']]
        
        
                    variables = f.model.exog
                    dfmain['VIF'] =  [variance_inflation_factor(variables, i) for i in range(variables.shape[1])]
                    for k in dfad.columns:
                        dfmain[k] = dfad[k].iloc[0]
                    
                    
                    dfmain.columns = ['系数','标准误','t值','P值',
                                   'VIF','R平方','调整后R平方','F值']
                    
                    dfmain['层级'] = '分层%s' % (i+1)
                    dfmain = dfmain.reset_index().rename(columns={0:'变量'}).set_index(['层级', 'R平方','调整后R平方','F值','变量'])

                    res.append(dfmain)
            
            
            
            return {'result':pd.concat(res), 'msg':msg}
        
        
        
            

if __name__ == '__main__':
    
    #读取数据
    from dataset import load_MedExp
    

    testdata = load_MedExp()
    
    df1 = testdata[['educdec']]
    df2 = testdata[[ 'med']]
    df3 = testdata[['age']]
    
    
    list_dfx = [df1,df2,df3]
    dfy = testdata[['ndisease']]
    
    
    
    #类的初始化
    O = HierarchicalReg()

    #打印该类描述的信息
    print(O.get_info().get('description'))
    
    #执行运算，传入tsx、tsy参数
    res = O.run(list_dfx,dfy)
    
    #获取返回的字典
    res.get('result')