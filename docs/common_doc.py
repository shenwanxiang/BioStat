
import os


def DOC(filename=''):
    docpath = os.path.dirname( __file__)
    #docfile = os.path.join(mypath,'docs/common_e_CorrStat.md')
    docfile = os.path.join(docpath, filename.split('.')[0]+'.md')
    with open(docfile) as f:
        doc = f.read()
    return doc


def test1(doc_path=None):
    #docfile = os.path.join(mypath,'docs/common_e_CorrStat.md')
    if not doc_path:
        docfile = os.path.join(docpath, 'common_e_CorrStat.md')
    with open(docfile) as f:
        doc = f.read()
    return doc


def test2(doc_path=None):
    #docfile = os.path.join(mypath,'docs/common_e_CorrStat.md')
    if not doc_path:
        docfile = os.path.join(docpath, 'common_e_CorrStat.md')
    with open(docfile) as f:
        doc = f.read()
    return doc