# 从文件中查找所有风险描述中 词语出现的频率
# 用numpy保存在  基准词.py  文件中
# 可以替换停用词表.txt， 直接将自己想要去掉的词语或者符号，添加到文件中即可
# 取出了出现频率最高的20个词语，并画图显示，并将图片保存到了  tfwords.jpg

import sqlite3
from collections import Counter
import numpy
import matplotlib.pyplot as plt

# 连接数据库，从表中取出数据
conn = sqlite3.connect(r"test.db")
cur = conn.cursor()
cur.execute('select 风险描述 FROM 自然灾害风险描述')
res = cur.fetchall()
res = str(res)

# 取出一些干扰性的符号
res = res.replace('\\n', '')
res = res.replace('#', '')
res = str(res).split(' ')  # 将所有的风险描述取出，并用空格分词
res = Counter(res)
# print(res)
list_no_meaning = ''

# 停用词表，替换一些无意义的词语
tmp = open('停用词表.txt', 'r')
for i in tmp.readlines():
    list_no_meaning += i
list_no_meaning = list_no_meaning.split()
# print(list_no_meaning)

# 除去停用词
tmp = []
for i in res:
    for j in list_no_meaning:
        # 去除频率低于100的词语，此处100可以替换为，需要的频率，
        # 如，出去出现低于200的词语：res.get(i) < 200
        if (j == i or res.get(i) < 100 or i == '') and not i in tmp:
            tmp.append(i)
            break

# print(tmp)
for i in tmp:
    res.pop(i)
print(res, len(res))
# 将选到的基准词保存
numpy.save('基准词.npy', res)
cur.close()

# 画个图，取出词频高的看看
res = sorted(res.items(), key=lambda x: x[1], reverse=True)
word_name = []
word_num = []
count = 0

# 取出出现频率最高的20个词语，并画图显示
for i in range(20):  # 取20个
    word_name.append(res[i][0])
    word_num.append(res[i][1])
print(word_name)
plt.figure(figsize=(20, 5))
plt.bar(range(20), word_num)
plt.xticks(range(20), word_name)  # 将x轴变量变成词名
plt.show()
plt.rcParams['font.sans-serif'] = ['SimHei']  # 为了让x轴显示中文的需要加这条（不然就会显示乱码）
plt.savefig('tfwords.jpg')  # 保存图片
conn.close()
