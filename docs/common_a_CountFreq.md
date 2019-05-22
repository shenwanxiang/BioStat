频数分析方法，适用于定类（pandas dtypes: category和bool）数据，如果非定类数据，则
    根据指定的bins参数，将定量数据转化为定类数据，执行run返回的结果为一个json，其中的result是
    dataframe，具有multiindex，显示了每列中每个类别所占的百分比和每个类别出现的次数.
    
    方法
    -------
    get_info : 
        获取该模型的信息， 返回一个字典，包含‘id’和‘name’, 'description','limited'关键字
        含义分别为：模型的id, 模型的名称，模型的描述，模型的适用范围


    run:  
        参数
        ----------
        df: pandas DataFrame
            原始要分析的数据
            
        bins: int, default:10
            如果一列为数值型数据，则根据这个参数自动转化为类别型数据
            
            
        返回结果
        ----------        
            返回一个字典，带有‘result’关键字，其值为具有muti-index的pandas dataframe