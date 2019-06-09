#Kendall协调系数https://spssau.com/front/spssau/helps/medicalmethod/kendall.html

#公式来源： http://www.real-statistics.com/reliability/kendalls-w/



import pandas as pd
from scipy import stats


def kendall_w(X):

    k, m  = X.shape
    
    #自由度
    df = m-1
    
    #denon
    denom = k**2*(m**3-m)
    
    #DEVSQ
    S = X.sum()
    SS = (S - S.mean())**2
    SSS = SS.sum()
    
    # kendel-w
    w = 12*SSS/denom
    
    #chi-squre
    chi = df*k*w
    
    #p_value
    p = stats.chi2.pdf(chi, df)
    
    return w, chi, p



def core(X):
    
    w, chi, p = kendall_w(X)

    z1 = X.median().to_frame(name = '中位数')
    z2 = pd.Series([len(X[i].dropna()) for i in X.columns], index=z1.index, name = '样本量')
    
    
    z = z1.join(z2)
    
    z['kendall 协调系数'] = w
    z['统计量'] = chi
    z['P'] = p
    
    z.index.name = '名称'
    
    return z    

if __name__ == '__main__':
    
    d = '''评委	选手1	选手2	选手3	选手4	选手5	选手6	选手7	选手8	选手9	选手10
    1	9	2	4	10	7	6	8	5	3	1
    2	10	1	3	8	7	5	9	6	4	2
    3	8	4	2	10	9	7	5	6	3	1
    4	9	1	2	10	6	7	4	8	5	3'''
    
    
    
    
    df = pd.DataFrame([i.split('\t') for i in d.split('\n')]).T.set_index(0).T
    df = df.astype(int).set_index('评委')
    df.columns.name=None
    
    
    
    core(df)