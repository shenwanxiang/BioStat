from .utils.pandastool import ParseDFtypes
from .utils.modelbase import ModelBase
#from .dataset import load_MedExp
from .dataset import load_MedExp


import pandas as pd
import coloredlogs,logging
coloredlogs.install()



class DescripStat(ModelBase):

    """
    数据的描述性统计分析，适用于定量的数据，对于定量数据主要统计和返回每列数据的
    样本量（count）、最小值(min)、最大值(max)、平均值(mean)、中位数(50%)、1/4分位数(25%)、
    3/4分位数(75%)、标准差(std)、峰度(kurt)、偏度(skew),方差(var),平均绝对误差(mad).
    注意事项：如果输入的pandas DataFrame的所有列都为定量型数据，则返回一个空的DataFrame在resilt关键字中
    
    方法
    -------
    get_info : 
        获取该模型的信息， 返回一个字典，包含‘id’和‘name’, 'description','limited'关键字
        含义分别为：模型的id, 模型的名称，模型的描述，模型的适用范围

    run:  
        参数
        ----------
        df: pandas DataFrame
           【注意】：所有的列都应该为数值型数据或者定量数据
        
     
        返回结果
        ----------        
            返回一个字典，带有‘result’关键字，其值为由统计量组成的dataframe
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
            df): 


        numer_cols,cate_cols = ParseDFtypes(df)
        
        msg = {}
        if numer_cols == []:
            logging.error('All input DataFrame are non-numeric columns, Please check your input data!')
            
            msg['error'] = '输入的所有的列都不是数值型数据，请检查输入数据df！'
            result = pd.DataFrame()
        

        else:
            if cate_cols != []:
                logging.warning('Input DataFrame has non-numeric columns, such as: %s will be ignored!' % cate_cols)
                msg['warning'] = '输入的数据包含非数值型数据, 比如列: %s 将会被忽略!' % cate_cols
                
            dfn = df[numer_cols]
            desb = dfn.describe().T
            
            desb['skew'] = dfn.skew()
            desb['kurt'] = dfn.kurt()
            desb['var'] = dfn.var()
            desb['mad'] = dfn.mad()
            result = desb
            
            result.columns = ['样本量','、平均值', '标准差', '最小值', '1/4分位数', 
                              '中位数', '3/4分位数', '最大值','偏度','峰度','方差','平均绝对误差']

    
    
        return {'result':result, 'msg':msg}
        
        

if __name__ == '__main__':
    
    #读取数据
    
    

    df = load_MedExp()
    
    
    #类的初始化
    D = DescripStat()

    #打印该类描述的信息
    print(D.get_info().get('description'))
    
    #执行运算，传入tsx、tsy参数
    dict_res = D.run(df)
    
    #获取返回的字典
    dict_res.get('result')