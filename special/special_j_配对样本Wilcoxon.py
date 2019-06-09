#配对样本Wilcoxon


#scipy-1.3.0



#名称	配对1(中位数) 配对2(中位数)	差值(配对1-配对2)	统计量	P
	


from scipy.stats import wilcoxon
import pandas as pd


def core(Y1, Y2):
    '''
    Y1: pd.Series, 测量值1
    Y2: pd.Series，测量值2
    
    '''
    
    m1 = Y1.median()
    m2 = Y2.median()
    
    e = m1-m2
    

    z_statistic, p_value = wilcoxon(Y1-Y2)
    
    
    res = {'名称': '%s 配对 %s' % (Y1.name, Y2.name),
           '%s中位数' % Y1.name: m1, 
           '%s中位数' % Y2.name: m2, 
           '差异':e,
           '统计量':z_statistic, 
           'P':p_value}
    
    df = pd.Series(res).to_frame().T.set_index('名称')
    
    
    return {'配对样本Wilcoxon分析结果': df}













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
    res = core(Y1, Y2)