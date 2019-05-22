#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 20:06:27 2018

@author: charleshen
"""

from scipy.stats import mannwhitneyu, kruskal
from utils.pandastool import ParseDFtypes, isCategory, isSeries
from utils.modelbase import ModelBase

import pandas as pd
import coloredlogs,logging
coloredlogs.install()



class NonparametricStat(ModelBase):

    """
    非参数检验用于研究定类数据与定量数据之间的关系情况。要求输入一个dfx(dataframe),tsy(Series),其中dfx所有列都必须是定量数据，
    ，tsy可以分为2组或以上的数据（tsy.unique 元素个数大于等于2）， 返回一个dataframe，在‘result‘关键字中。如果tsy的组别为两组，
    比如男和女两组，则应该使用MannWhitney统计量，如果组别超过两组，则应该使用Kruskal-Wallis统计量结果。
    系统自动为你选择MannWhitney或者Kruskal-Wallis统计量
    
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
            返回一个字典，带有‘result’关键字，其值为按照tsy分组的均值和标准差、检验统计量、p-值等等系数组成的dataframe

            
    """
    
    
    
    def __init__(self):
        self._name_ = '非参数检验'
        
        
    def get_info(self):
        
        return {'id': self._id, 
                'args':[{'id':'dfx','name':'分析项X','type':pd.DataFrame}, 
                        {'id':'tsy','name':'分析项Y','type':pd.Series}],
                'name': self._name, 
                'description': self._description,
                'limited':'tsy需要一列的数据都是分类型数据,dfx需要每列的数据都是数字型数据，不能是字符串或者object'
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
                    
                    
                    
                    
                    ui = tsy.unique()
                    
                    if len(ui) == 2:
                        mod = mannwhitneyu
                        cols = ['MannWhitney检验统计量', 'p-值']
                    else:
                        mod = kruskal
                        cols = ['Kruskal-Wallis统计量', 'p-值']
                        
                        
                    input_idx_lst = [tsy[tsy==i].index  for i in ui]
                        
                        
                    rs = []
                    for i in x_numer_cols:
                        
                        
                        dd = [dfu[i].loc[j] for j in input_idx_lst]
                        s,p = mod(*dd)
                        rs.append(pd.DataFrame([s,p], index = cols,columns=[i]).T)

                    res = m1.join(pd.concat(rs))
                    
    
                    return {'result':res, 'msg':msg}
        
        
        
            

conf =  NonparametricStat().get_info()

if __name__ == '__main__':
    
    #读取数据
    from dataset import load_MedExp
    
    
    df =load_MedExp()

    testdata = load_MedExp()
    dfx = df[['med','age','idp']]
    tsy = df.health
    
    
    
    #类的初始化
    O = NonparametricStat()

    #打印该类描述的信息
    print(O.get_info().get('description'))
    
    #执行运算，传入tsx、tsy参数
    dict_res = O.run(dfx,tsy)
    
    #获取返回的字典
    dict_res.get('result')