#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 21:19:09 2018

@author: charleshen
"""

#单因素方差分析

import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

from utils.pandastool import ParseDFtypes, isCategory, isSeries
from utils.modelbase import ModelBase
import statsmodels.api as sm

import coloredlogs,logging
coloredlogs.install()



'''

dfx #定量，

tsy(定类) #固定 


'dfx[0] ~ tsy'
cw_lm=ols('weight ~ Time + C(Diet)', data=cw).fit() #Specify C for Categorical
print(sm.stats.anova_lm(cw_lm, typ=2))


model = ols("y ~ x", data).fit()

'''

class TwowayAnova(ModelBase):

    """
    单因素方差分析法，要求输入一个tsx(Series),dfy(pd.DataFrame),其中tsx必须是定量数据，
    ，dfy的2列应该都是定类数据）， 返回一个dataframe，在‘result‘关键字中，补充表在‘table’中
    
    
    方法
    -------
    get_info : 
        获取该模型的信息， 返回一个字典，包含‘id’和‘name’, 'description','limited'关键字
        含义分别为：模型的id, 模型的名称，模型的描述，模型的适用范围

    run:  
        参数
        ----------
        tsx: pandas Series
            需要数据都是数字型数据，不能是字符串或者object
        
        dfy: pandas DataFrame
             需要2列的数据都是分类型数据
            
            
        返回结果
        ----------        
            返回一个字典，带有‘result’关键字，自由度、平方和、F-值、p-值等等系数组成的dataframe
            'table'其值为按照dfx分组的均值、标准差和样本量等
            
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
            tsx, 
            dfy): 

            tsx = tsx.reset_index(drop=True)
            dfy = dfy.reset_index(drop=True)        
            
            msg = {}
            
            
            
            xl = len(dfx)
            yl = len(tsy)
            if  xl != yl:
                logging.error('输入的dfx的长度为:%s 不等于输入的tsy的长度: %s ，请检查输入的数据! ' % (xl,yl))
                msg['error'] = '输入的dfx的长度为:%s 不等于输入的tsy的长度: %s ，请检查输入的数据! ' % (xl,yl)
                return  {'result':pd.DataFrame(), 'msg':msg}            
            
            
            if not isSeries(tsx) or isCategory(tsx):
                logging.error('输入的tsx变量不是Series类型或者不是数值型数据，请检查输入的数据！')
                msg['error'] = '输入的tsx变量不是Series类型或者不是数值型数据，请检查输入的数据！'
                
                return  {'result':pd.DataFrame(), 'msg':msg}
                
            
            else:
                y_numer_cols, y_cate_cols = ParseDFtypes(dfy)


                if len(y_cate_cols) < 2:
                    logging.error('需要输入的dfy的所有列至少有2列是字符型数据，请检查输入的数据！')
                    msg['error'] = '需要输入的dfy的所有列至少有2列是字符型数据，请检查输入的数据！'
                    return  {'result':pd.DataFrame(), 'msg':msg}
                
                
                else:
                    
                    if y_numer_cols != []:
                        logging.warning('输入的dfy中包含数值型的列: %s, 系统将自动忽略这些列！' % y_numer_cols)
                        msg['warning'] = '输入的dfy中包含数值型的列: %s, 系统将自动忽略这些列！' % y_numer_cols
                        
                    if len(y_cate_cols) > 2:
                        logging.warning('输入的dfy中包含2列以上的字符型数据 %s, 系统将自动忽略这些列:%s ' % y_cate_cols[2:])
                        
                        if msg.get('warning'):
                            msg['warning'] = msg['warning'] +'\n'+ '输入的dfy中包含2列以上的字符型数据 %s, 系统将自动忽略这些列:%s ' % y_cate_cols[2:]
                        
                        else:
                            msg['warning'] = '输入的dfy中包含2列以上的字符型数据 %s, 系统将自动忽略这些列:%s ' % y_cate_cols[2:]
                            
                            
                            
                    name = tsx.name
                    y_cate_cols = y_cate_cols[:2]
                    
                    dfu = dfy[y_cate_cols].join(tsx)
                    
                    rs= []
                    for c in y_cate_cols:
                        m = dfu.groupby(c)[name].mean().to_frame(name='平均值').round(2)
                        s = dfu.groupby(c)[name].std().to_frame(name='标准差').round(2)
                        n = dfu.groupby(c)[name].size().to_frame(name='样本量')
                        dfr = pd.concat([m,s,n],axis=1).reset_index().rename(columns={c:'标签'})
                        dfr['分析项'] = c
                        
                        dfr = dfr.set_index(['分析项','标签'])
                        rs.append(dfr)
                        
                    tb1 = pd.concat(rs)

                    dfu = sm.add_constant(dfu, prepend=True).rename(columns={'const':'截距'})
                                    
                    formula = '%s ~ %s + %s + %s + %s*%s' % (tsx.name, '截距', y_cate_cols[0],y_cate_cols[1],y_cate_cols[0],y_cate_cols[1])
                        
                    #formula = '%s ~ C(%s,Sum)*C(%s,Sum)' % (tsx.name, y_cate_cols[0],y_cate_cols[1])

                    
                    df_fit = ols(formula, data=dfu).fit()
                    
                    dfres = anova_lm(df_fit, typ=2)
                    
                    dfres.columns = ['平方和', '自由度', 'F-值', 'p-值']
                    dfres = dfres.rename(index={'Residual':'误差'})
                    dfres.index.name = '差异源'


        
                    return {'result':dfres, 'msg':msg, 'table':tb1}
        
        
        
            

if __name__ == '__main__':
    
    #读取数据
    from dataset import load_MedExp
    
    
    df =load_MedExp()

    testdata = load_MedExp()

    tsx = df.age
    dfy = df[['health', 'sex']]
    
    #类的初始化
    O = TwowayAnova()

    #打印该类描述的信息
    print(O.get_info().get('description'))
    
    #执行运算，传入tsx、tsy参数
    res = O.run(tsx,dfy)
    
    #获取返回的字典
    res.get('result')