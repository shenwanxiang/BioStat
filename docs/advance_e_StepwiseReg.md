#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 18:05:45 2018

@author: charleshen
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







class StepwiseReg(ModelBase):

    """
    逐步回归分析方法，要求输入一个dfx(dataframe),dfy(dataframe),其中dfy为一列数据，
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
            如果方法为‘pearson’，需要每列的数据都是数字型数据，不能是字符串或者object
        
        dfy: pandas DataFrame
            ‘pearson’，需要一列的数据都是数字型数据，不能是字符串或者object
            
            
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
            dfx, 
            dfy): 

        
            dfy = dfy.reset_index(drop=True)
            dfx = dfx.reset_index(drop=True)            
        
        
        
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
                
            x_numer_cols, x_cate_cols = ParseDFtypes(dfx)
            y_numer_cols, y_cate_cols = ParseDFtypes(_dfy)

            if (x_numer_cols ==[]) | (y_numer_cols == []):
                logging.error('All input DataFrame are no numeric columns, Please check your input data!')
                
                msg['error'] = 'All input DataFrame are no numeric columns, Please check your input data!'
                dfmain =pd.DataFrame()
                
                
            else:
                
                _dfx = dfx[x_numer_cols]
                X_cols = stepwise_selection(_dfx, _dfy)
                
                logging.info('the following variables are selected: %s' % X_cols)
                
                dfXS = _dfx[X_cols]
                
                X = sm.add_constant(dfXS, prepend=True)
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
                

            return {'result':dfmain, 'msg':msg}
        
        
        
    
def stepwise_selection(X, y, 
                       initial_list=[], 
                       threshold_in=0.05, 
                       threshold_out = 0.1, 
                       verbose=True):
    """ Perform a forward-backward feature selection 
    based on p-value from statsmodels.api.OLS
    Arguments:
        X - pandas.DataFrame with candidate features
        y - list-like with the target
        initial_list - list of features to start with (column names of X)
        threshold_in - include a feature if its p-value < threshold_in
        threshold_out - exclude a feature if its p-value > threshold_out
        verbose - whether to print the sequence of inclusions and exclusions
    Returns: list of selected features 
    Always set threshold_in < threshold_out to avoid infinite looping.
    See https://en.wikipedia.org/wiki/Stepwise_regression for the details
    """
    included = list(initial_list)
    while True:
        changed=False
        # forward step
        excluded = list(set(X.columns)-set(included))
        new_pval = pd.Series(index=excluded)
        for new_column in excluded:
            model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[included+[new_column]]))).fit()
            new_pval[new_column] = model.pvalues[new_column]
        best_pval = new_pval.min()
        if best_pval < threshold_in:
            best_feature = new_pval.idxmin()
            included.append(best_feature)
            changed=True
            if verbose:
                logging.info('Add  {:3} with p-value {:.6}'.format(best_feature, best_pval))

        # backward step
        model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[included]))).fit()
        # use all coefs except intercept
        pvalues = model.pvalues.iloc[1:]
        worst_pval = pvalues.max() # null if pvalues is empty
        if worst_pval > threshold_out:
            changed=True
            worst_feature = pvalues.idxmax()
            included.remove(worst_feature)
            if verbose:
                logging.info('Drop {:3} with p-value {:.6}'.format(worst_feature, worst_pval))
        if not changed:
            break
    return included
        

if __name__ == '__main__':
    
    #读取数据
    from dataset import load_MedExp
    

    testdata = load_MedExp()
    dfx = testdata[['educdec', 'med','age','fmde']]
    dfy = testdata[['ndisease']]
    
    
    
    #类的初始化
    O = StepwiseReg()

    #打印该类描述的信息
    print(O.get_info().get('description'))
    
    #执行运算，传入tsx、tsy参数
    dict_res = O.run(dfx,dfy)
    
    #获取返回的字典
    dict_res.get('result')
            