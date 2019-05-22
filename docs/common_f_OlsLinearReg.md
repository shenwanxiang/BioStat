#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 18:05:45 2018

@author: charleshen
"""

from .utils.pandastool import ParseDFtypes
from .utils.modelbase import ModelBase
from .dataset import load_MedExp
from io import StringIO

import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor

import pandas as pd

import coloredlogs,logging
coloredlogs.install()




class OlsLinearReg(ModelBase):

    """
    数据的回归分析方法，要求输入一个dfx(dataframe),dfy(dataframe),其中dfy为一列数据，
    返回一个最小二乘的线性模型的参数dataframe，在‘result‘关键字中
    
    
    方法
    -------
    get_info : 
        获取该模型的信息， 返回一个字典，包含‘id’和‘name’, 'description','limited'关键字
        含义分别为：模型的id, 模型的名称，模型的描述，模型的适用范围

    run:  
        参数
        ----------
        dfx: pandas DataFrame
            需要每列的数据都是数字型数据，不能是字符串或者object
        
        dfy: pandas DataFrame
            只能一列的数据都是数字型数据，不能是字符串或者object
            
            
        返回结果
        ----------        
            返回一个字典，带有‘result’关键字，其值为coef, p, r, VIF 等等系数组成的dataframe, 
            'predicted_result'关键字包含了一个实际值和预测值的dataframe

            
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
            dfx, 
            dfy): 

        
            dfy = dfy.reset_index(drop=True)
            dfx = dfx.reset_index(drop=True)            
        
        
        
            msg = {}
            
            xl = len(dfx)
            yl = len(dfy)
            if  xl != yl:
                logging.error('the length of input X:%s is not equal the length of Y: %s ! ' % (xl,yl))
                msg['error'] = '输入的dfx的长度为:%s 不等于输入的dfy的长度: %s ! ' % (xl,yl)
                return  {'result':pd.DataFrame(), 'msg':msg}        
        
    
    
            if len(dfy.columns) != 1:
                logging.warning('input DataFrame dfy has more than one columns, but only the first colum will be used!')
                msg['warning'] = '输入的dfy不只有一列数据，但是只有第一列会被使用'
                
                _dfy = dfy[[dfy.columns[0]]]
                
            else:
                _dfy = dfy
                
            x_numer_cols, x_cate_cols = ParseDFtypes(dfx)
            y_numer_cols, y_cate_cols = ParseDFtypes(_dfy)

            if (x_numer_cols ==[]) | (y_numer_cols == []):
                logging.error('All input DataFrame are no numeric columns, Please check your input data!')
                
                msg['error'] = '输入的所有的列都不是数值型数据，请检查输入数据'
                dfmain =pd.DataFrame()
                
                
            else:
                
                _dfx = dfx[x_numer_cols]
                
                X = sm.add_constant(_dfx, prepend=True)
                y = _dfy
                
                f = smf.OLS(y, X).fit()
                
                y_pre = f.predict(X)
                
                
                df_predicted = pd.DataFrame(y_pre,index = y.index, columns=['预测值'])
                
                df_predicted = y.join(df_predicted)
                
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
                dfinfo2 = parse_table02(df_list[2])

                dfinfo1 = df_list[1].fillna('Variables').set_index(0)
                dfinfo1 = dfinfo1.T.set_index('Variables').T

                dfmain = dfinfo1[dfinfo1.columns[:4]]

                dfad = dfinfo0[['R-squared:',
                                'Adj. R-squared:', 
                                'F-statistic:']].join(dfinfo2[['Durbin-Watson:',
                                                               'Jarque-Bera (JB):',
                                                               'Omnibus:']])

                variables = f.model.exog
                dfmain['VIF'] =  [variance_inflation_factor(variables, i) for i in range(variables.shape[1])]
                for i in dfad.columns:
                    dfmain[i] = dfad[i].iloc[0]
                
                
                dfmain.columns = ['系数', '标准偏差', 't值', 'P值', 
                                  'VIF值', 'R平方:', '调整后R平方',
                                  'F值:', 'Durbin-Watson检验:', 
                                  'Jarque-Bera (JB检验):', 'Omnibus检验']
                
                dfmain.index.name = '变量'
                dfmain = dfmain.rename(index = {'const':'常数项'})
                dfmain = dfmain.round(5)
                dfmain['P值'] = dfmain['P值'].apply(lambda x:'{:.5f}'.format(x))
                
            return {'result':dfmain, 'msg':msg, 'model':f, 'predicted_result':df_predicted}
        
        
        
            

if __name__ == '__main__':
    
    #读取数据
    #from dataset import load_MedExp
    

    testdata = load_MedExp()
    dfx = testdata[['educdec', 'med','age','fmde']]
    dfy = testdata[['ndisease']]
    
    
    
    #类的初始化
    O = OlsLinearReg()

    #打印该类描述的信息
    print(O.get_info().get('description'))
    
    #执行运算，传入tsx、tsy参数
    res = O.run(dfx,dfy)
    
    #获取返回的字典
    res.get('predicted_result')
            