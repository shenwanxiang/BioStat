#单样本Wilcoxonhttps://spssau.com/front/en/spssau/helps/medicalmethod/onesamplewilcoxon.html

#https://gist.github.com/mblondel/1761714



#单样本Wilcoxon检验用于检验数据是否与某数字有明显的区别，从功能上讲，单样本Wilcoxon检验与单样本T检验完全一致；二者的区别在于数据是否正态分布，如果数据正态分布，则使用单样本T检验，反之则使用单样本Wilcoxon检验。


from scipy.stats import wilcoxon
import pandas as pd


def core(Y, V):
    '''
    Y: pd.Series
    V: number to comparasion, can be float
    
    '''
    
    m = Y.median()
    s = len(Y)
    z_statistic, p_value = wilcoxon(Y - V)
    
    
    res = {'名称':Y.name,
           '样本量':s, 
           '中位数':m, 
           '统计量':z_statistic, 
           'P':p_value}
    
    df = pd.Series(res).to_frame().T.set_index('名称')
    
    
    return {'单样本Wilcoxon分析结果': df}





if __name__ == '__main__':
    
    
    
    d = '''手机尺寸-测量1	手机尺寸-测量2
    6	6.943
    6.832	6
    6.093	6.037
    6	6.749
    6.423	5.55
    6	5.075
    6.499	6.395
    6.922	5.764
    6	6
    6	6
    6	5.122
    6	6
    6	6
    6	5.821
    6	6
    5.28	6.415
    6	6
    6.163	5.655
    5.515	5.346'''


    df = pd.DataFrame([i.split('\t') for i in d.split('\n')]).T.set_index(0).T
    df = df.astype(float).reset_index(drop=True)
    Y1 = df['手机尺寸-测量1']
    Y2 = df['手机尺寸-测量2']
    
    res = core(Y1, 6)
    