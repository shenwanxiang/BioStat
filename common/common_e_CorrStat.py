#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 15:48:50 2018

@author: charleshen
"""

import logging
import os

import coloredlogs
import pandas as pd
from scipy.stats import kendalltau, pearsonr, spearmanr

from ..dataset import load_MedExp
from ..utils.modelbase import ModelBase
from ..utils.pandastool import ParseDFtypes

coloredlogs.install()

# DOC = common_doc.CorrStat_DOC()
ABSTRACT = '''相关分析用于研究定量数据之间的关系情况,包括是否有关系,以及关系紧密程度等.此分析方法通常用于回归分析之前;相关分析与回归分析的逻辑关系为:先有相关关系,才有可能有回归关系。'''


def get_corr_func(method):

    def _pearson(a, b):
        return pearsonr(a, b)

    def _kendall(a, b):
        return kendalltau(a, b)

    def _spearman(a, b):
        return spearmanr(a, b)

    _cor_methods = {
        'pearson': _pearson,
        'kendall': _kendall,
        'spearman': _spearman
    }
    return _cor_methods.get(method)


class common_e_CorrStat(ModelBase):

    """
    数据的相关性统计方法，要求输入一个dfx(dataframe),dfy(dataframe),
    求dfx的每列和dfy的每列的相关系数及p值，需要指定相关系数的方法meathod：'pearson'
    、'kendall'、'spearman'，返回一个相关系数和p-value的dataframe在‘result‘关键字中


    方法
    -------
        get_info : 
            获取该模型的信息， 返回一个字典，包含‘id’和‘name’, 'description','limited'关键字
            含义分别为：模型的id, 模型的名称，模型的描述，模型的适用范围

        run:  
            参数
            ----------
            df: pandas DataFrame
                如果方法为‘pearson’，需要每列的数据都是数字型数据，不能是字符串或者object

            dfy: pandas DataFrame
                ‘pearson’，需要每列的数据都是数字型数据，不能是字符串或者object

            method: str
                需要计算相关系数的方式，可选'pearson'(默认),'kendall'、'spearman'

            crosstab: bool, default:False
                是否需要转换返回的dataframe的数据布局格式，如果为True则转为x,y的矩阵对应格式

    返回结果
    ----------        
        返回一个字典，带有‘result’关键字，其值为相关系数和p-value组成的dataframe


    """

    def __init__(self,
                 model_id=None,
                 model_limiation=None,
                 ):

        self._name_ = '相关性统计'

    def get_info(self):

        return {'id': self._id,
                'name': self._name,

                'info': self._description,
                'abstract': ABSTRACT,
                'doc': self._doc,
                'limited': '如果方法为‘pearson’，需要输入的每列的数据都是数值型数据，不能是字符串或者object',
                'args': [{"id": "x", "name": "分析项x", 'type': 'dataframe', 'requirement': '每个元素必须包含在df的列中'},
                         {"id": "y", "name": "分析项y", 'type': 'dataframe', 'requirement': '每个元素必须包含在df的列中'}],

                'extra_args': [{'id': "method",
                                'default': 'pearson',
                                'name': "计算方法",
                                'type': "select",
                                'choice': [{'value': 'kendall', 'label': 'kendall相关系数'},
                                           {'value': 'spearman',
                                               'label': 'spearman相关系数'},
                                           {'value': 'pearson', 'label': 'pearson相关系数'}]
                                },

                               {'id': "crosstab",
                                'default': 'False',
                                'name': "生成交叉表",
                                'type': "select",
                                'choice': [{'value': 'False', 'label': '否'},
                                           {'value': 'True', 'label': '是'}]
                                }
                               ],
                 'schema': {
                    'type': 'object',
                    'properties': {
                        'method': {'type': 'string'},
                        'crosstab':{'type':'string'}
                    },
                }
        }
    def run(self, df, x, y,
            extra_args={'method': 'pearson',
                        'crosstab': False}):

        method = extra_args.get('method')
        crosstab = extra_args.get('crosstab')

        m = get_corr_func(method)
        # msg={'error':None,'warning':None}
        msg = {}

        dfx = df[x]
        dfy = df[y]

        if m:
            if method == 'pearson':
                x_numer_cols, x_cate_cols = ParseDFtypes(dfx)
                y_numer_cols, y_cate_cols = ParseDFtypes(dfy)

                if (x_numer_cols == []) | (y_numer_cols == []):

                    logging.error(
                        'All input DataFrame are no numeric columns, Please check your input data!')
                    msg['error'] = '输入的所有的列都不是数值型数据，请检查输入数据'
                    dfres = pd.DataFrame()

                else:

                    res = []
                    if (x_cate_cols != []) | (x_cate_cols != []):
                        logging.warning(
                            'input DataFrame has no numeric data columns, will be ignored!')
                        msg['warning'] = '输入的数据包含非数值型数据, 将会被忽略!'

                    for xc in x_numer_cols:
                        for yc in y_numer_cols:
                            c, p = pearsonr(dfx[xc], dfy[yc])
                            res.append([xc, yc, c, p])
                    dfres = pd.DataFrame(
                        res, columns=['x-列', 'y-列', '相关系数', 'p-值'])
                    #dfres['p-值'] = dfres['p-值'].apply(lambda x:'{:.5f}'.format(x))

                    if crosstab:
                        dfres = dfres.pivot_table(index='x-列', columns='y-列')

            else:
                res = []
                for xc in dfx.columns:
                    for yc in dfy.columns:
                        c, p = m(dfx[xc], dfy[yc])
                        res.append([xc, yc, c, p])
                dfres = pd.DataFrame(
                    res, columns=['x-列', 'y-列', '相关系数', 'p-值'])
                #dfres['p-值'] = dfres['p-值'].apply(lambda x:'{:.5f}'.format(x))

                if crosstab:
                    dfres = dfres.pivot_table(index='x-列', columns='y-列')

        else:
            logging.error(
                "unknow method, only 'pearson','kendall'、'spearman' are supported!")
            dfres = pd.DataFrame()
            msg['error'] = "未知的方法, （meathd参数）只支持 'pearson','kendall'、'spearman' 这三种!"

        dfres = dfres.round(5)

        return {'tables': [{'table_json': dfres.T.reset_index().to_json(),
                            'table_html': dfres.to_html(),
                            'table_info': '生成的字段之间的相关系数和p-值表',
                            'chart': ['heatmap', 'line', 'bar']}],
                'conf': self.get_info(),
                'msg': msg}, [{'table_df': dfres, 'label': '生成的字段之间的相关系数和p-值表'}]


if __name__ == '__main__':

    # 读取数据

    df = load_MedExp()
    x = ['educdec', 'med', 'age', 'fmde']
    y = ['ndisease']

    # 类的初始化
    C = CorrStat()

    # 打印该类描述的信息
    print(conf)

    extra_args = {'method': 'pearson', 'crosstab': False}

    # 执行运算，传入tsx、tsy参数
    cal_results = C.run(df, x, y, extra_args)

    # 获取返回的字典
    cal_results
