#CochranQ检验 https://spssau.com/front/spssau/helps/medicalmethod/cochranQ.html


import pandas as pd

from statsmodels.sandbox.stats.runs import cochrans_q




def core(x):
    '''
    x: pd.DataFrame()
    '''
    n = len(x)
    
    
    
    freq = x.apply(lambda a:a.value_counts()).T
    perc = freq.apply(lambda a:a/n) 
    
    
    f1 = freq.T
    f1 = f1.reset_index()
    f1.index = ['频数', '频数']
    f1 = f1.reset_index().set_index(['level_0','index'])

    f2 = perc.T
    f2 = f2.reset_index()
    f2.index = ['百分比', '百分比']
    f2 = f2.reset_index().set_index(['level_0','index'])

    f = f1.append(f2).T
    f.columns.names = [None, None]
    
    z, p = cochrans_q(x)
    
    df = pd.Series({'样本量':n, 'CochransQ 统计量':z, 'p':p, 'df':x.shape[1]-1})
    df = df.to_frame().T.set_index('样本量')
    res = {'频数分析结果':f, 'CochranQ检验结果': df}
    
    return res
    
    


if __name__ == '__main__':
    d = '''村长	村民1	村民2	村民3	村民4	村民5	村民6	村民7	村民8	村民9	村民10
    村长1	0	1	1	0	0	1	1	1	1	1
    村长2	1	1	0	0	0	1	1	1	1	1
    村长3	0	1	1	1	1	0	0	0	0	1
    村长4	0	0	0	0	1	1	0	0	1	0'''
    
    
    
    df = pd.DataFrame([i.split('\t') for i in d.split('\n')]).T.set_index(0).T
    df = df.set_index('村长')
    df.columns.name = None
    df = df.astype(int)
    res = core(x)