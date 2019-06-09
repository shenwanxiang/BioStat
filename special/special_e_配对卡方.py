#配对卡方： https://spssau.com/front/spssau/helps/medicalmethod/pairedchisquare.html


#研究判断两种诊断方法是否有差异性，即两种方法之间的差异情况如何，是否有一定的可替代性等。研究的核心在于对于数据的差异性
#明显的，此数据为配对数据，而且对比的数据为定类数据（诊断结果 阴性、阳性 为定类数据），因而需要使用配对卡方检验。



import sys
sys.path.insert(0,'/Users/charleshen/Desktop') #改成你的路径


import pandas as pd
import scipy.stats as stats
from statsmodels.stats import contingency_tables




def core(tsx,tsy):

    
    '''
    input
    --------
      tsx: 定类型数据
      tsy: 定类型数据
    '''


    crosstab = pd.crosstab(tsx, tsy)
    crosstab2 = pd.crosstab(tsx, tsy,margins = True)
    crosstab2 = crosstab2.rename(columns={'All':'总计'}, index={'All':'总计'})
    

    if crosstab.shape == (2,2):
        res = contingency_tables.mcnemar(crosstab)
        method = 'mcnemar'
     
    else:
        res = contingency_tables.SquareTable(crosstab).symmetry(method="bowker")
        method = 'bowker'
        
    chi2 = res.statistic
    p = res.pvalue
    expected = stats.contingency.expected_freq(crosstab)
    
         
    dfe = pd.DataFrame(expected,columns=tsy.unique(),index=tsx.unique()).round(3)
    dfte = crosstab.astype(str) +' (' +  dfe.astype(str) + ')'
    dfte['总计'] =  crosstab2['总计']
    dfte.loc['总计'] = crosstab2.loc['总计'] 
    dfte['检验方法'] = method
    dfte['卡方统计量'] = chi2
    dfte['p-值'] = p
    dfte.index.name = '类别'
    return dfte.reset_index().set_index(['检验方法','卡方统计量','p-值','类别'])



if __name__ == '__main__':
    d = 'A方法\tB方法\n1\t1\n1\t2\n2\t1\n2\t2\n1\t2\n2\t1\n2\t1\n2\t1\n2\t1\n2\t1\n2\t1\n2\t1\n2\t1\n2\t1\n2\t1\n2\t2\n2\t2\n2\t2\n2\t2\n2\t2\n2\t2\n2\t2\n2\t2\n2\t2\n2\t2\n2\t2\n2\t2\n2\t2\n2\t2\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1\n1\t1'
    
    
    df = pd.DataFrame([i.split('\t') for i in d.split('\n')]).T.set_index(0).T
    df = df.astype(int).reset_index(drop=True)
    
    tsx = df['A方法']
    tsy = df['B方法']
    dfte = core(tsx,tsy)