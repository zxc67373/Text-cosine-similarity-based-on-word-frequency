# 本文件中，将上述5文件中得到的，词语向量，用余弦相似度函数计算得到
# 其中按每年前20个公司，为基准，并去除为0的公司，求均值，得到基准向量
# 然后用基准向量 与每一个求余弦值

import sqlite3
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

conn = sqlite3.connect('./test.db')
cur = conn.cursor()
for year in range(12):
    cur.execute('''select 风险词向量 from 自然灾害风险描述 where 年=%d''' % (2008+year))
    print('''select 风险词向量 from 自然灾害风险描述 where 年=%d''' % (2008+year))
    tmp = cur.fetchall()
    n = 20  # 取每年的前20个为样本
    arr = []
    count = 0
    for i in range(n):
        a = list(map(lambda v: int(v), tmp[i][0][1:-1].split(', ')))
        arr.append(a)
    count = 0
    for i in arr:
        if sum(i) > 0:
            count += 1
    standard_vec = np.array(arr).sum(axis=0) / count
    for i in range(len(list(tmp))):  # 分别计算每个的余弦相似度
        res = cosine_similarity(standard_vec.reshape(1, -1),
                                np.array(list(map(lambda v: int(v), tmp[i][0][1:-1].split(', ')))).reshape(1, -1))
        conn.execute('''update  自然灾害风险描述 SET 余弦相似度 = "{}" where ROWID = {}'''.format(float(res), year*50+i + 1))
        # print('''update  自然灾害风险描述 SET 余弦相似度 = "{}" where ROWID = {}'''.format(res,year*50+i + 1))
        conn.commit()
