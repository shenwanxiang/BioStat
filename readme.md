# medical-learn


### 三、安装：

`import sys`
`sys.path.insert(0,'/Users/shenwanxiang/Desktop/smap/medical-learn/') #改成你的路径`



### 三、整体介绍：

#### 以下三个模块分别为通用统计分析（common模块），高级机器学习分析（advance模块）和医学统计中特殊场景的分析（special模块）

#### 导入模块
`>>> from MedLearn import common,advance,special`

1.common模块：

    1.1 频数：common_a_CountFreq
    1.2 交叉（卡方）：common_b_ChiSquareCrossTab
    1.3 描述：common_c_DescripStat
    1.4 分类汇总：common_d_GroupByStat
    1.5 相关：common_e_CorrStat
    1.6 回归：common_f_OlsLinearReg
    1.7 单因素方差：common_g_OnewayAnova
    1.8 T检验：common_h_TTestInd
    1.9 单样本T检验：common_i_TTest1Samp
    1.10 配对T检验：common_j_TTestPair
    1.11 正态性检验：common_k_NormalityTest
    1.12 非参数检验：common_l_NonparametricStat
    1.13 方差齐检验：common_m_HOVTest


2.advance模块：

    2.1 K-均值聚类：advance_a_Cluster  
    2.2 因子:advance_b_FA
    2.3 主成分:advance_c_PCA
    2.4 事后检验:advance_d_PostHocTest
    2.5 逐步回归:advance_e_StepwiseReg
    2.6 分层回归: advance_f_HierarchicalReg
    2.7 双因素方差: advance_g_TwowayAnova
    2.8 二元Logit分析: advance_h_BinLogReg
    2.9 多分类Logit分析: advance_i_MultiLogReg
    2.10 岭回归分析: advance_j_RingeReg

3.special模块：

    3.1 卡方检验: special_a_ChiSquaredTest
    3.2 Kappa一致性检验: special_b_KappaTest
    3.3 二元Probit回归分析: special_c_Probit
    3.4 Poisson回归分析:  special_d_Poisson
    3.5 多因素方差分析:  special_e_MultiVariance
    
    
    
4.额外的模块（可以预测输入的结果，分割训练、测试集）：

    4.1: 层次聚类法
    4.2: 聚类热图分析
   ![image](http://genomicsclass.github.io/book/pages/figure/clustering_and_heatmaps-heatmap.2-1.png)
    4.3: DBSCAN(基于密度聚类)
    
    
    4.4: 决策树分类分析法（可视化输出决策树，自动寻找最佳参数）
    4.5：随机森林分类
    4.6：决策树回归
    4.7: 随机森林回归
    4.8：SVM多分类
    4.9: SVM二分类
    4.10. SVR回归分析（roc曲线等等，自动寻找最佳参数）
    4.11. 混合模型分析（集合多重模型，内置SFE特征选择方法）
    4.12. 贝叶斯分类
    4.13. 贝叶斯回归
    4.14.多层神经网络回归（自动寻找最佳参数）
    4.15.多层神经网络分类（自动寻找最佳参数）
    
    4.16.鲁棒回归分析（ RANSAC算法，线性回归的一种，可自动剔除outliers样本，防止过拟合）
    4.17.Ridge 回归
    4.18. 核PCA分析（非线性下适用）
    
    4.19.时间序列ARIMA模型
    4.20.时间序列LSTM模型
    
5.额外的数据处理模块： 
    
    
    5.1.数据归一化法（均值、最大最小等多种归一化）
    5.2.数据正太化处理（将数据处理成近正态分布）
    5.3.数据异常值检测和剔除方法（多种统计方法检测异常值）
    5.4.数据编码方法（采用分词将字符串转为one-hot等）
    5.5.数据离散化方法（采用多种方法离散数据，如指定bins，基于计数、将缺失值作为其自己的组处理）
    5.6.数据采样与分配（平衡、分层、分组等等多种采样方法，训练测试集合分割等）
    5.7.数据属性特征生成（自动构建特征，属性加权，还有时间序列数据自动生成lag下的特征等等）
    5.8.数据缺失处理（基于KANN，决策树、时间维度等等多种方法补全缺失数据）
    5.9.数据标签生成（专门负责处理Y，生成特有标签）