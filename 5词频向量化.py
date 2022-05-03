# 根据词语出现的此处，向量化
# 本文件不建议修改，处了总文件数 601-》改为你的文件数

import numpy
import sqlite3
conn= sqlite3.connect('test.db')
cur = conn.cursor()
words = numpy.load('基准词.npy',allow_pickle=True).item()
word = words.keys()

# print(list(word).index('additional'))
for row in range(1,601):
    this_word = cur.execute('''select 风险词频 from 自然灾害风险描述 where rowid={}'''.format(row)).fetchall()
    tmp = ''
    for j in str(this_word):
        if not j in "'(){}[],":
            tmp+=j
    this_word = tmp.split('\\n')
    vector = []
    for i in range(len(word)): vector.append(0) # 新建一个向量空间，长度和基准词个数一致
    for i in this_word:
        tmp=i.split(":")
        print(tmp)
        if not '' in tmp and len(tmp)==2 and tmp[0] in word:
            vector[list(word).index(tmp[0])] = int(tmp[1])
    # print(vector)
    # print('''UPDATE 自然灾害风险描述 set 风险词向量 = '{}' where rowid={} '''.format(vector,i))
    # print(len(vector))
    cur.execute('''UPDATE 自然灾害风险描述 set 风险词向量 = '{}' where rowid={} '''.format(vector,row))
    conn.commit()
conn.close()