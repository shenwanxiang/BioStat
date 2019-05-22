#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 17:50:20 2018

@author: charleshen
"""

import pandas as pd

import os




def load_MedExp():
    
    """
    >>> from dataset import load_MedExp
    >>> df = load_MedExp()
    """
    
    data_path  = os.path.join(os.path.dirname(__file__),'data','MedExp.csv')
    return pd.read_csv(data_path,index_col=0)
    


def load_SPSS():

    """
    >>> from dataset import load_SPSS
    >>> df = load_SPSS()
    """
    
    data_path  = os.path.join(os.path.dirname(__file__),'data','SPSSAU.xls')
    return pd.read_excel(data_path,index_col=0).reset_index(drop=True)    