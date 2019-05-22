# 我的文档
## 一个描述
    数据的相关性统计方法，要求输入一个dfx(dataframe),dfy(dataframe),
求dfx的每列和dfy的每列的相关系数及p值，需要指定相关系数的方法meathod：'pearson'
、'kendall'、'spearman'，返回一个相关系数和p-value的dataframe在‘result‘关键字中
    
    
    方法
-------
        get_info : 
            获取该模型的信息， 返回一个字典，包含‘id’和‘name’,
'description','limited'关键字
            含义分别为：模型的id, 模型的名称，模型的描述，模型的适用范围
run:  
            参数
            ----------
            df: pandas DataFrame
如果方法为‘pearson’，需要每列的数据都是数字型数据，不能是字符串或者object
            
            dfy:
pandas DataFrame
                ‘pearson’，需要每列的数据都是数字型数据，不能是字符串或者object
method: str
                需要计算相关系数的方式，可选'pearson'(默认),'kendall'、'spearman'
crosstab: bool, default:False
是否需要转换返回的dataframe的数据布局格式，如果为True则转为x,y的矩阵对应格式
            
    返回结果
----------        
        返回一个字典，带有‘result’关键字，其值为相关系数和p-value组成的dataframe
## 一个表格
### html 格式
<table border="1" class="dataframe">  <thead>    <tr
style="text-align: right;">      <th></th>      <th>med</th>      <th>lc</th>
<th>idp</th>      <th>lpi</th>      <th>fmde</th>      <th>physlim</th>
<th>ndisease</th>      <th>health</th>      <th>linc</th>      <th>lfam</th>
<th>educdec</th>      <th>age</th>      <th>sex</th>      <th>child</th>
<th>black</th>    </tr>  </thead>  <tbody>    <tr>      <th>1</th>
<td>62.07547</td>      <td>0.0</td>      <td>yes</td>      <td>6.907755</td>
<td>0.0</td>      <td>no</td>      <td>13.73189</td>      <td>good</td>
<td>9.528776</td>      <td>1.386294</td>      <td>12.0</td>
<td>43.87748</td>      <td>male</td>      <td>no</td>      <td>no</td>    </tr>
<tr>      <th>2</th>      <td>0.00000</td>      <td>0.0</td>      <td>yes</td>
<td>6.907755</td>      <td>0.0</td>      <td>no</td>      <td>13.73189</td>
<td>excellent</td>      <td>9.528776</td>      <td>1.386294</td>
<td>12.0</td>      <td>17.59138</td>      <td>male</td>      <td>yes</td>
<td>no</td>    </tr>    <tr>      <th>3</th>      <td>27.76280</td>
<td>0.0</td>      <td>yes</td>      <td>6.907755</td>      <td>0.0</td>
<td>no</td>      <td>13.73189</td>      <td>excellent</td>
<td>9.528776</td>      <td>1.386294</td>      <td>12.0</td>
<td>15.49966</td>      <td>female</td>      <td>yes</td>      <td>no</td>
</tr>  </tbody></table>
### md格式
|    | med    | lc   | idp   | lpi   | fmde   |
physlim   | ndisease   | health    | linc   | lfam   | educdec   | age    | sex
| child   | black   |
|:---|:-------|:-----|:------|:------|:-------|:----------|:-----------|:----------|:-------|:-------|:----------|:-------|:-------|:--------|:--------|
| 1  | 62.075 | 0.0  | yes   | 6.908 | 0.0    | no        | 13.732     | good
| 9.529  | 1.386  | 12.0      | 43.877 | male   | no      | no      |
| 2  | 0.0
| 0.0  | yes   | 6.908 | 0.0    | no        | 13.732     | excellent | 9.529  |
1.386  | 12.0      | 17.591 | male   | yes     | no      |
| 3  | 27.763 | 0.0
| yes   | 6.908 | 0.0    | no        | 13.732     | excellent | 9.529  | 1.386
| 12.0      | 15.5   | female | yes     | no      |

## 一张照片
![我的照片](https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=2791261768,1320060678&fm=26&gp=0.jpg)

```python
! notedown doc.ipynb --to markdown --strip > doc.md
```

```python
def to_markdown(df):
    from subprocess import Popen, PIPE
    s = df.to_latex()
    p = Popen('pandoc -f latex -t markdown',
              stdin=PIPE, stdout=PIPE, shell=True)
    stdoutdata, _ = p.communicate(input=s.encode("utf-8"))
    return stdoutdata.decode("utf-8")
```

```python
def df_to_markdown(*dfs, sep_line='\n---\n', **kwargs):
    """Convert pandas dataframe to markdown table."""
    import tabulate

    disable_numparse = kwargs.pop('disable_numparse', True)
    tablefmt = kwargs.pop('tablefmt', 'pipe')
    headers = kwargs.pop('headers', 'keys')
    
    for df in dfs:
        print(tabulate.tabulate(df, tablefmt=tablefmt, headers=headers,
                                disable_numparse=disable_numparse, **kwargs))
        if sep_line is not None:
            print(sep_line)
```

```python
df_to_markdown(df.head(3).round(3))
```

|    | med    | lc   | idp   | lpi   | fmde   | physlim   | ndisease   | health
| linc   | lfam   | educdec   | age    | sex    | child   | black   |
|:---|:-------|:-----|:------|:------|:-------|:----------|:-----------|:----------|:-------|:-------|:----------|:-------|:-------|:--------|:--------|
| 1  | 62.075 | 0.0  | yes   | 6.908 | 0.0    | no        | 13.732     | good
| 9.529  | 1.386  | 12.0      | 43.877 | male   | no      | no      |
| 2  | 0.0
| 0.0  | yes   | 6.908 | 0.0    | no        | 13.732     | excellent | 9.529  |
1.386  | 12.0      | 17.591 | male   | yes     | no      |
| 3  | 27.763 | 0.0
| yes   | 6.908 | 0.0    | no        | 13.732     | excellent | 9.529  | 1.386
| 12.0      | 15.5   | female | yes     | no      |

```python
|    | med    | lc   | idp   | lpi   | fmde   | physlim   | ndisease   | health    | linc   | lfam   | educdec   | age    | sex    | child   | black   |
|:---|:-------|:-----|:------|:------|:-------|:----------|:-----------|:----------|:-------|:-------|:----------|:-------|:-------|:--------|:--------|
| 1  | 62.075 | 0.0  | yes   | 6.908 | 0.0    | no        | 13.732     | good      | 9.529  | 1.386  | 12.0      | 43.877 | male   | no      | no      |
| 2  | 0.0    | 0.0  | yes   | 6.908 | 0.0    | no        | 13.732     | excellent | 9.529  | 1.386  | 12.0      | 17.591 | male   | yes     | no      |
| 3  | 27.763 | 0.0  | yes   | 6.908 | 0.0    | no        | 13.732     | excellent | 9.529  | 1.386  | 12.0      | 15.5   | female | yes     | no      |

---
```
