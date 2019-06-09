
#泊松回归 Poisson回归分析

#泊松回归假设反应变量Y是泊松分布，并假设它期望值的对数可由一组未知参数进行线性表达


import sys
sys.path.insert(0,'/Users/charleshen/Desktop') #改成你的路径


import numpy as np
import pandas as pd
from io import StringIO
import statsmodels.api as sm
from sklearn.metrics import r2_score
from THU_STAT.dataset import load_SPSS



def core(X, Y, Z = None):
    
    '''
    X: X变量
    Y: 预测值
    Z 为基数， 可以为空或者为一个Series，长度与Y一致
    
    '''
    X = sm.add_constant(X, prepend=False)
    X = X.rename(columns = {'const' : '截距'})


    if Z is None:
        Z = pd.Series([1 for i in range(len(Y))])
        
    ### 除以基数 然后取对数
    y = Y/Z
    y_log = np.log(y)
    
    
    # building the model
    poisson_mod = sm.Poisson(y_log, X)
    res = poisson_mod.fit(method="bfgs")
    y_pre = res.predict(X)
    
    
    Y_predict = np.exp(y_pre) * Z
    Y_predict.name = '预测值'
    df_predict_result = Y.to_frame(name = '实际值').join(Y_predict)
    
        #model description
    tables = res.summary().tables
    df_list = [pd.read_html(StringIO(t.as_html()))[0] for t in tables ]
    dfinfo1 = df_list[1].fillna('Variables').set_index(0)
    dfinfo1 = dfinfo1.T.set_index('Variables').T
    dfinfo1.index.name = '项'
    dfinfo1.columns.name = '参数类型'
    dfinfo1.columns = ['回归系数', '标准误差','Z值','p值', '95%CI(下限)','95%CI(上限)']
    dfinfo1['or值'] = np.exp(res.params)
    dfinfo1 = dfinfo1.round(3)
    

    R_Squared = r2_score(y_log, y_pre)

    
    tb2 = {'BIC':res.bic,
            'AIC':res.aic,
            'df':res.df_model,
            'p': res.llr_pvalue,
            '似然比卡方值': res.llr,
            'R²':R_Squared, 
            'Pseud_R²':res.prsquared}
    dfinfo2 = pd.DataFrame([tb2]).round(3)
    dfinfo2 = dfinfo2.set_index('似然比卡方值')
    
    r = {'模型似然比检验和效果汇总': dfinfo2,  'Poisson回归分析结果汇总': dfinfo1, '实际值与预测值': df_predict_result}
    
    return r

    

if __name__ == '__main__':
    
    
    df = load_SPSS()
    Y = df['【系统】网购满意度_定量']
    X =  df[['【系统】退货次数_定量',  '【系统】投诉次数_定量', '【系统】平台偏好_定类', '【系统】网购忠诚度_定量']]

    
    res = core(X, Y, Z = None)
    
    print(res.get('模型似然比检验和效果汇总'))
    print(res.get('Poisson回归分析结果汇总'))
    
    
    
        
    
    
    