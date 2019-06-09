#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 22:30:12 2019

@author: shenwanxiang
"""

#分层聚类



import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage  
from scipy.cluster.hierarchy import fcluster
from matplotlib import pyplot as plt
import pandas as pd

def core(df, k = 2):

    
    Z = linkage(df)
    labelList = df.index
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    dendrogram(Z,  
                orientation='left',
                labels=labelList,
                distance_sort='descending',
                show_leaf_counts=True,
                ax = ax)
    
    fig.savefig('cluster.png')
    
    dfc = pd.Series(fcluster(Z, k, criterion='maxclust'), index = df.index, name = '类别')
    dfres = df.join(dfc)
    
    return {'聚类的类别':dfres, '层次聚类图': fig}



if __name__ == '__main__':
    # generate two clusters: a with 100 points, b with 50:
    np.random.seed(4711)  # for repeatability of this tutorial
    a = np.random.multivariate_normal([10, 0], [[3, 1], [1, 4]], size=[10,])
    b = np.random.multivariate_normal([0, 20], [[3, 1], [1, 4]], size=[5,])
    X = np.concatenate((a, b),)
    df = pd.DataFrame(X)
    core(df)