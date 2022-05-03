# 将每个文本中的描述，和前面统计的基准词，做比较，得到词频
# 此处1-600个文件，一样是根据总文件，601改为最后的文件数量+1
# 最后词频保存到了表 自然灾害风险描述 中的新加列中


import numpy
import sqlite3
from collections import Counter
# 读取 基准词.npy
words = numpy.load(r'基准词.npy', allow_pickle=True).item()
# 连接数据库
conn = sqlite3.connect(r"test.db")
cur = conn.cursor()
for row in range(1, 601):  # 根据总列数
    cur.execute('''select 风险描述 from 自然灾害风险描述 where rowid = %d''' % row)
    Risk_description = cur.fetchall()
    # print(Risk_description)
    tmp = ''
    for i in str(Risk_description):
        if i in '''()[]{}'",''':
            continue
        else:
            tmp += i
    # 此处除去了一部分无意义的符号
    res = str(Risk_description)
    res = res.replace('\\n', '')
    res = res.replace('#', '')
    Risk_description = Counter(tmp.split())
    # Risk_description 为每一个风险描述分词之后得到的结果
    tmp = ''
    count = 0
    for i in Risk_description:
        for j in words:
            if i == j:
                tmp += str(i) + ":" + str(Risk_description.get(i)) + '\n'
    conn.execute('''UPDATE 自然灾害风险描述 SET 风险词频 = "{}" where ROWID = {}'''.format(tmp, row))
    conn.commit()
conn.close()
