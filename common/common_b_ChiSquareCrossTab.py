#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 2 20:07:26 2018

@author: charleshen

Chi-square test
"""


import logging
import os

import coloredlogs
import pandas as pd
# import researchpy as rp

from ..dataset import load_MedExp
from ..utils.modelbase import ModelBase
from ..utils.pandastool import isCategory, isSeries


coloredlogs.install()

ABSTRACT = '''相关分析用于研究定量数据之间的关系情况,包括是否有关系,以及关系紧密程度等.此分析方法通常用于回归分析之前;相关分析与回归分析的逻辑关系为:先有相关关系,才有可能有回归关系。'''


class common_b_ChiSquareCrossTab(ModelBase):

    """基于交叉列联表的卡方检验方法，适用于定类（pandas dtypes: category和bool）数据，
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
    """

    def __init__(self,
                 model_id=None,
                 model_limiation=None,
                 bins=10
                 ):

        self._name_ = '卡方检验方法'

    def get_info(self):

        return {'id': self._id,
                'name': self._name,
                'info': self._description,
                'abstract': ABSTRACT,
                'doc': self._doc,
                'limited': '',
                'args': [{"id": "x", "name": "分析项x", 'type': 'series', 'requirement': '每个元素必须包含在df的列中'},
                         {"id": "y", "name": "分析项y", 'type': 'series',
                             'requirement': '每个元素必须包含在df的列中'}
                         ],
                'extra_args': [{'id': "bins",
                                'default': 10,
                                'name': "计算方法",
                                'type': "input",
                                },
                               ],
                 'schema': {
                    'type': 'object',
                    'properties': {
                        'bins': {'type': 'number'}
                    },
                }
                }

    def run(self,
            df, x, y, extra_args={'bins': 10}):

        #msg={'error':None,'warning':None}

        tsy = df[x]
        tsx = df[y]
        tsy = tsy.reset_index(drop=True)
        tsx = tsx.reset_index(drop=True)

        msg = {}

        xl = len(tsx)
        yl = len(tsy)
        if xl != yl:
            logging.error(
                'the length of input X:%s is not equal the length of Y: %s ! ' % (xl, yl))
            msg['error'] = '输入的tsx的长度为:%s 不等于输入的tsy的长度: %s ! ' % (xl, yl)
            return {'result': pd.DataFrame(), 'msg': msg}

        self.bins = extra_args.get('bins')
        if not isSeries(tsy) & isSeries(tsx):
            logging.error('X or y data are not a pandas Series type!')

            msg['error'] = 'tsx或者tsy不是 pandas Series 数据类型!'
            return {'result': pd.DataFrame(), 'msg': msg}

        else:
            if not isCategory(tsy):
                tsy = pd.cut(tsy, bins=bins)
                logging.warning(
                    'the Series tsy is not category type, will be convert to category type by bins of %d' % self.bins)
                msg['warning'] = '列tsy不是定类（category）数据, 将强制通过bins:%d为转化为定类型数据' % self.bins

            if not isCategory(tsx):
                tsx = pd.cut(tsx, bins=bins)
                logging.warning(
                    'the Series tsx is not category type, will be convert to category type by bins of %d' % self.bins)

                if msg.get('warning'):

                    msg['warning'] = msg['warning'] + \
                        '列tsx不是定类（category）数据, 将强制通过bins:%d为转化为定类型数据' % self.bins

                else:
                    msg['warning'] = 't列tsx不是定类（category）数据, 将强制通过bins:%d为转化为定类型数据' % self.bins

            table, results = rp.crosstab(tsx,
                                         tsy,
                                         prop='col',
                                         test='chi-square')

            return {'tables': [{'table_json': dfres.T.reset_index().to_json(orient='index'),
                                'table_html': dfres.to_html(),
                                'table_info': '生成的字段之间的相关系数和p-值表',
                                'chart': ['heatmap', 'line', 'bar']}],
                    'conf': self.get_info(),
                    'msg': msg}, [{'table_df': dfres, 'label': '生成的字段之间的相关系数和p-值表'}]


if __name__ == '__main__':

    #读取数据

    testdata = load_MedExp()
    tsx = testdata['sex']
    tsy = testdata['idp']

    #类的初始化
    c = ChiSquareCrossTab()

    #打印该类描述的信息
    print(c.get_info().get('description'))

    #执行运算，传入tsx、tsy参数
    res = c.run(tsx, tsy)

    #获取返回的字典
    res.get('result')
