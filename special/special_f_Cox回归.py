#Cox回归

#Cox回归模型，又称“比例风险回归模型(proportional hazards model)”,
#简称Cox回归。它是一种研究相关因素对于生存时间影响的回归模型，
#其已在医疗，金融和市场研究等专业领域中广泛使用

#https://nbviewer.jupyter.org/urls/umich.box.com/shared/static/epie6pcdk1rgb10zcd5v.ipynb



import sys
sys.path.insert(0,'/Users/charleshen/Desktop') #改成你的路径


import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import r2_score
from statsmodels.duration.hazard_regression import PHReg



from THU_STAT.dataset import load_SPSS



def core(X, Y1, Y2, Z = None):
    
    
    '''
    Y1: pd.Series,生存时间， 定量数据
    Y2: pd.Series,生存状态， 定类数据， 只能为0或者1， 1表示活， 0 表示死
    
    X： pd.DataFrame,药物组合的类型、年龄等等定类或者定量数据
    
    Z: pd.Series, 分层项，定类数据
    
    '''
    
    X = X.reset_index(drop = True)
    
    if type(Y1) == np.ndarray:
        Y1 = pd.Series(Y1, name = 'futime')
    else:
        Y1 = Y1.reset_index(drop=True)
        
        
    if type(Y2) == np.ndarray:
        Y2 = pd.Series(Y2, name = 'death')
    else:
        Y2 = Y2.reset_index(drop=True)
        

    if type(Z) == np.ndarray:
        Z = pd.Series(Z, name = 'class')
        
    elif type(Z) == pd.Series:
        Z = Z.reset_index(drop=True)
    else:
        Z = pd.Series(['' for i in range(len(Y1))], name = 'class')
    
    
    mod = PHReg(Y1, X, status = Y2)
    res = mod.fit()
    
    tables = res.summary().tables
    dfinfo1 = tables[1]
    dfinfo1.index.name = '项'
    dfinfo1.columns.name = '参数类型'
    dfinfo1.columns = ['回归系数', '标准误差SE','风险比HR', 'Z值','p值', '95%CI(下限)','95%CI(上限)']
    dfinfo1['or值'] = np.exp(res.params)
    dfinfo1 = dfinfo1.round(3)
    

    tb2 = {
            'df':res.df_model,
            '似然比卡方值': res.llf
            }
    
    dfinfo2 = pd.DataFrame([tb2]).round(3)
    dfinfo2 = dfinfo2.set_index('似然比卡方值')
    
    
    ## 生存率曲线
    D = Y1.to_frame(name='futime').join(Y2.to_frame(name='death')).join(Z.to_frame(name='class'))        
    gb = D.groupby("class")
    
    classes = []
    for g in gb:
        sf = sm.SurvfuncRight(g[1]["futime"], g[1]["death"]).summary()
        sl = sf['Surv prob']
        sl.index.name = '生存时间'
        sl.name = str(g[0]) + '_生存率'
        classes.append(sl.to_frame())
    
    df_sl = pd.concat(classes, axis=1)
    
    rr = {'生存函数曲线': df_sl, 
          'Cox回归模型分析结果汇总': dfinfo1, 
          'Cox回归模型似然比检验结果':dfinfo2 }
    
    return rr
    
    

if __name__ == '__main__':
    
    
    d = '''药物组别	性别	年龄	生存时间（周）	生存状态
            0	0	0	21	1
            0	0	0	17	1
            1	1	1	12	0
            1	1	1	61	0
            0	0	0	64	0
            0	0	0	7	0
            1	1	1	51	1
            0	0	0	15	1
            0	1	0	2	1
            0	1	0	9	1
            0	1	0	18	1
            0	1	0	17	1'''
    
    df = pd.DataFrame([i.split('\t') for i in d.split('\n')]).T.set_index(0).T
    df = df.astype(int)
    
    
    X = df[['药物组别', '年龄']]
    Y1 = df['生存时间（周）']
    Y2 = df['生存状态']
    Z = df['性别']
    
    res = core(X, Y1, Y2, Z)
    
 
