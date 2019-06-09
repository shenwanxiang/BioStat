#游程检验


# more details: https://www.statsmodels.org/dev/generated/statsmodels.sandbox.stats.runs.Runs.html#statsmodels.sandbox.stats.runs.Runs
#  for runs in a binary sequence


from statsmodels.sandbox.stats import runs
import pandas as pd
import numpy as np





def core(x):
    
    
    if x.unique().shape[0] > 2:
        x = (x >= x.median())*1
        
    r = runs.Runs(x)
    z, p = r.runs_test()
    
    
    N = len(x)
    
    ts = pd.Series({'样本量':N, '统计量':z, 'p':p, '名称':x.name})
    df = ts.to_frame().T.set_index('名称')
    res ={'游程分析结果': df}
    return res










if __name__ == '__main__':


    
    data = np.random.choice(a=[1,2, 3,4,5,6], size=(100,))
    
    x = pd.Series(data)
    x.name = '扔骰子点数'
    res = core(x)






