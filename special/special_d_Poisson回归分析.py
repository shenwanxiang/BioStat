
#泊松回归 Poisson回归分析

#泊松回归假设反应变量Y是泊松分布，并假设它期望值的对数可由一组未知参数进行线性表达

import pandas as pd
import statsmodels.api as sm
import numpy as np





X = sm.add_constant(X, prepend=False)
Y = [elem for elem in dataWithDummies['num_awards'].values]

# building the model
poisson_mod = sm.Poisson(Y, X)
poisson_res = poisson_mod.fit(method="newton")
print(poisson_res.summary())
