#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 21:00:36 2018

@author: charleshen
"""





from scipy.stats import levene
import pandas as pd

from utils.pandastool import ParseDFtypes, isCategory, isSeries
from utils.modelbase import ModelBase

import coloredlogs,logging
coloredlogs.install()









class HOVTest(ModelBase):

    """
    方差齐检验,用于分析不同定类数据组别 对定量数据时的波动情况是否一致.也叫F检验，例如想知道三组学生的智商tsy
    身高波动（dfx）情况是否一致（通常情况希望波动一致，即方差齐）。F检验仅可对比多组数据的差异,也即tsy的unqiue元素个数可以大于2，
    返回一个dataframe，在‘result‘关键字中
    
    
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
        
        tsy: pandas Series
             需要一列的数据都是分类型数据
            
            
        返回结果
        ----------        
            返回一个字典，带有‘result’关键字，其值为按照tsy分组的均值和标准差、F-值、p-值等等系数组成的dataframe

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
            tsy): 

            tsy = tsy.reset_index(drop=True)
            dfx = dfx.reset_index(drop=True)            
        
        
        
            msg = {}
            
            xl = len(dfx)
            yl = len(tsy)
            if  xl != yl:
                logging.error('the length of input X:%s is not equal the length of Y: %s ! ' % (xl,yl))
                msg['error'] = 'the length of input X:%s is not equal the length of Y: %s ! ' % (xl,yl)
                return  {'result':pd.DataFrame(), 'msg':msg}
                
            
            if not isSeries(tsy) or not isCategory(tsy):
                logging.error('input tsy is not a pandas Series or not a category data!')
                msg['error'] = 'input tsy is not a pandas Series or not a category data!'
                
                return  {'result':pd.DataFrame(), 'msg':msg}
                
            
            
            else:
                

                x_numer_cols, x_cate_cols = ParseDFtypes(dfx)


                if x_numer_cols ==[]:
                    logging.error('All input dfx are no numeric columns, Please check your input dfx data!')
                    msg['error'] = 'All input dfx are no numeric columns, Please check your input dfx data!'
                    return  {'result':pd.DataFrame(), 'msg':msg}
                
                
                else:
                    
                    if x_cate_cols != []:
                        logging.warning('input dfx has non-numeric columns: %s, will ignore these columns!' % x_cate_cols)
                    
                        msg['warning'] = 'input dfx has non-numeric columns: %s, will ignore these columns!' % x_cate_cols
                    
                    
                    name = tsy.name
                    
                    dfu = dfx[x_numer_cols].join(tsy)
                    m = dfu.groupby(name).mean().T
                    s = dfu.groupby(name).std().T

                    def change(ts):
                        v= []
                        for i in ts.index:
                            r = '%s±%s' % (round(ts.loc[i],2),round(s[ts.name].loc[i],2))
                            v.append(r)
                        return pd.Series(v,index=ts.index)


                    m1 = m.apply(change)
                    
                    
                    

                    rs = []
                    for i in x_numer_cols:
                        
                        
                        dd = [dfu[dfu[tsy.name] == c][i] for c in tsy.unique()]
                        
                        F, p = levene(*dd)
                        
                        columns = ['F-值', 'p-值']
                        rs.append(pd.DataFrame([F,p],index=columns,columns=[i]).T)

                    
                    
                    res = m1.join(pd.concat(rs))
                    
    
                    return {'result':res, 'msg':msg}
            
        
        
            

if __name__ == '__main__':
    
    #读取数据
    from dataset import load_MedExp
    
    
    df =load_MedExp()

    testdata = load_MedExp()
    dfx = df[['med','age','idp']]
    
    tsy = df.health
    #tsy = tsy[tsy.isin(['good', 'excellent'])]
    
    
    #类的初始化
    O = HOVTest()

    #打印该类描述的信息
    print(O.get_info().get('description'))
    
    #执行运算，传入tsx、tsy参数
    dict_res = O.run(dfx,tsy)
    
    #获取返回的字典
    dict_res.get('result')
















