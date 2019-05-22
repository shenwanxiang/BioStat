基于交叉列联表的卡方检验方法，适用于定类（pandas dtypes: category和bool）数据，
    如果非定类数据，则根据指定的bins参数，将定量数据转化为定类数据，执行run需要输入tsx,tsy
    的数据参数，分别代表X和y,类型为pandas Series,只含有一列数据，返回的结果为一个json，
    其中的table是类型的交叉列联表，其中的result是卡方检验的结果参数，包含了卡方值χ2，p值，系数Cramer’s V
    
    方法
    -------
    get_info : 
        获取该模型的信息， 返回一个字典，包含‘id’和‘name’, 'description','limited'关键字
        含义分别为：模型的id, 模型的名称，模型的描述，模型的适用范围

    run:  
        参数
        ----------
        tsx: pandas Series
            输入的分析项X, 只能包含一列
        
        tsy:pandas Series
            输入的分析项Y，只能包含一列
            
        bins: int, default:10
            将定量型数据转化为定类的参数
            
        返回结果
        ----------        
            返回一个字典，带有‘result’关键字，其值为具有muti-index的pandas dataframe