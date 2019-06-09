#多样本Friedeman



from scipy.stats import friedmanchisquare
import pandas as pd

def core(X):
    ''' 
    X:pd.DataFrame
    '''
    
    s, p = friedmanchisquare(*[X[i] for i in X.columns])
    
    
    
    z1 = X.median().to_frame(name = '中位数')
    z2 = pd.Series([len(X[i].dropna()) for i in X.columns], index=z1.index, name = '样本量')
    
    
    z = z1.join(z2)
    
    z['统计量'] = s
    z['P'] = p
    
    z.index.name = '名称'
    
    
    
    return {'多样本Friedeman分析结':z}    



if __name__ == '__main__':
    d = '''编号	第1次身高	第2次身高	第3次身高
    1	1.66	1.660	1.700
    2	1.61	1.600	1.610
    3	1.72	1.720	1.750
    4	1.71	1.710	1.660
    5	1.68	1.700	1.720
    6	1.73	1.690	1.730
    7	1.75	1.740	1.760
    8	1.73	1.760	1.730
    9	1.69	1.720	1.660
    10	1.74	1.760	1.700
    11	1.69	1.710	1.640
    12	1.61	1.570	1.610
    13	1.77	1.800	1.750
    14	1.71	1.710	1.710
    15	1.68	1.690	1.710'''
    
    
    df = pd.DataFrame([i.split('\t') for i in d.split('\n')]).T.set_index(0).T
    df = df.astype(float).reset_index(drop=True).set_index('编号')
    df.columns.name=None
    
    res = core(df)


