# 直接描述和间接描述的数组
# 需要更改的话一个[]中，前面是基础词，后面是定位词
# 如第一个["disasters", "natural,nature,weather,environmental"] 中，
# "disasters"是基础词， "natural,nature,weather,environmental"是定位词
# 要加入新的，就新建一个[]，
# 更新原本的话，直接在原本的数组中，加入单词


import sqlite3
Direct_word = [["disasters", "natural,nature,weather,environmental"],
               ["Catastrophe,catastrophic", "natural,nature,weather,disaster,event"], ["Weather",
                                                                                        "Adverse,extreme,severe,event,conditions,unusual,inclement,harsh,unseasonable,unseasonably,abnormal,issue,pattern,warm,cold"],
               [
                   "sea level rise,hurricane,wildfire,drought,earthquake,flood,tsunami,tornado,volcano,volcanic,storm,mudslide,landslide,windstorm,lightningstorm,tropicalstorm,typhoon,blizzard,seismic",
                   ""]
               ]
Idirect_word = [
    ["Business,service,activity,activities,operation,operate,operating,produce,product,labor,construct,manufacture,manufacturing,supply,supplies,supplier,ship,distribute,distribution,deliver,delivery,deliveries,ability,abilities,perform,system,data,information,transmission,investment,infrastructure,predict",
        "Interrupt,disrupt,damage,fail,adverse,reduce,delay,harm,diminish,impair,impede,suspension,suspect,threat,negative,material,cancel,restrict,inability,unable,prevent,discard,decline,cease,loss,limit,obstruct,difficult,difficulties,jeopardize"],
    ["facility,facilities,property,properties,equipment,infrastructure,asset",
     "damage,failure,destruction,close,closure,repair,shut down, sabotage,replace,adverse"],
    ["Recovery,response", "Disaster,plan,program"], ["Continuity,contigency", "Business,service,plan,measure"],
    ["Vulnerabilities,vulnerable,fine,penalty,penalties", ""], ["Insurance,insure",
                                                                "Cover,inadequate,adequate,loss,unavailable,exceed,excessive,policy,policies,arrangement,against"],
    ["coverage", "inadequate,adequate,unavailable,exceed,excessive,loss"], ["Injury,injuries", ""],
    ["Fatality,fatalities,deathInsure,uninsured", ""], [
        "sale,revenue,customer,profit,cashflow,confidence,earning,margin",
        "Lost,loss,damage,reduce,adverse,diminish,insufficient,lower,decrease,negative,fluctuate,fluctuation,fail"],
    ["relation", "Damage,loss,"], ["Reputation", "Harm,loss,damage"], ["Financial,price,contract,stock",
                                                                       "Loss,harm,damage,negative,material,diminish,adverse,fluctuate,fluctuation,cancel,decline"]
]

# 处理上面的词语，不建议修改
for i in range(len(Direct_word)):
    Direct_word[i][0] = Direct_word[i][0].split(',')
    Direct_word[i][1] = Direct_word[i][1].split(',')
for i in range(len(Idirect_word)):
    Idirect_word[i][0] = Idirect_word[i][0].split(',')
    Idirect_word[i][1] = Idirect_word[i][1].split(',')
# print(Direct_word)
# print(Idirect_word)

# 连接数据库
conn = sqlite3.connect(r'test.db')
# 新建一个自然灾害风险描述的表
conn.execute('''
CREATE TABLE IF NOT exists 自然灾害风险描述
(oid TEXT,
CIK TEXT ,
"公司" TEXT,
年报类型 TEXT,
时间 TEXT,
文本链接 TEXT,
网页链接 TEXT,
具体链接 TEXT,
年 TEXT,
季度 TEXT,
财政年    TEXT,
CONFORMED_SUBMISSION_TYPE TEXT,
COMPANY_CONFORMED_NAME TEXT,
CENTRAL_INDEX_KEY TEXT,
STANDARD_INDUSTRIAL_CLASSIFICATION TEXT,
CITY TEXT,
STATE TEXT,
PUBLIC_DOCUMENT_COUNT TEXT,
FILED_AS_OF_DATE TEXT,
DATE_AS_OF_CHANGE TEXT,
ABS_ASSET_CLASS TEXT,
STATE_OF_INCORPORATION TEXT,
SEC_ACT TEXT,
SEC_FILE_NUMBER TEXT,
FILM_NUMBER TEXT,
STREET_1 TEXT,
ZIP TEXT,
BUSINESS_PHONE TEXT,
风险描述 TEXT,
风险词频 TEXT,
风险词向量 TEXT,
余弦相似度 TEXT
);
''')
sql = '''insert into 自然灾害风险描述  ("oid","CIK","公司","年报类型","时间","文本链接","网页链接","具体链接","年","季度","财政年","CONFORMED_SUBMISSION_TYPE","COMPANY_CONFORMED_NAME","CENTRAL_INDEX_KEY","STANDARD_INDUSTRIAL_CLASSIFICATION","CITY","STATE","PUBLIC_DOCUMENT_COUNT","FILED_AS_OF_DATE","DATE_AS_OF_CHANGE","ABS_ASSET_CLASS","STATE_OF_INCORPORATION","SEC_ACT","SEC_FILE_NUMBER","FILM_NUMBER","STREET_1","ZIP","BUSINESS_PHONE")
select "oid","CIK","公司","年报类型","时间","文本链接","网页链接","具体链接","年","季度","财政年","CONFORMED_SUBMISSION_TYPE","COMPANY_CONFORMED_NAME","CENTRAL_INDEX_KEY","STANDARD_INDUSTRIAL_CLASSIFICATION","CITY","STATE","PUBLIC_DOCUMENT_COUNT","FILED_AS_OF_DATE","DATE_AS_OF_CHANGE","ABS_ASSET_CLASS","STATE_OF_INCORPORATION","SEC_ACT","SEC_FILE_NUMBER","FILM_NUMBER","STREET_1","ZIP","BUSINESS_PHONE"
from TABLE1 
'''

# 将其余列内容复制到新表，注意此sql只有不存在表 自然灾害风险描述 的时候运行
# 如果已经存在表 自然灾害风险描述 ，先将它删除，再运行这个文件
conn.execute(sql)
cur = conn.cursor()
count = 0
# 只执行，1--600个文件，如果文件更多，将601改为你的文件数量+1
for i in range(67, 601):
    cur.execute('''select 风险因子 from TABLE1 where rowid = %d''' % i)
    result = cur.fetchall()
    # print(result)
    # print(len(result))
    for tmp in result:  # 取出所有风险因子
        text = ''
        for j in tmp:  # 元组转化为字符串
            text += j
    # text为一个文件的，所有描述，按换行符分割
        text = text.split(r'\n')

    res = ''
    k = 0
    tmp_including = ''
    while (k < len(text)):
        # print(text[k])
        # 用------，判断是否为标题
        if '-----' in text[k]:
            for word in Direct_word:
                for word1 in word[0]:
                    if word1.upper() in text[k]:
                        for word2 in word[1]:
                            if word2.upper() in text[k] and not text[k] in res and not text[k + 1] in res:
                                if (text[k][min(text[k].index(word1.upper()),text[k].index(word2.upper())):1+max(text[k].index(word1.upper()),text[k].index(word2.upper()))]).count(' ')<6: # 前后五个词
                                    res += text[k]+'\n'
                                    res += text[k + 1]+'\n'
                                    k+=1
        # 判断不是标题的情况
        else:
            sentences = text[k].split('.')
            flag_direct = 0
            tmp_direct =''
            tmp_indirect =''
            flag_indirect = 0
            for j in range(len(sentences)):
                # tmp = sentences[j].split(" ,!.")
                for word in Direct_word:
                    for word1 in word[0]:
                        if word1.lower() in sentences[j]:
                            for word2 in word[1]:
                                if word2.lower() in sentences[j] and not sentences[j] in res and (sentences[j][min(sentences[j].index(word1.lower()),sentences[j].index(word2.lower())):1+max(sentences[j].index(word1.lower()),sentences[j].index(word2.lower()))]).count(' ')<6:
                                    if "#" in sentences[j] and  not tmp_including in res :
                                        res+=tmp_including+'\n'
                                    if  not tmp_indirect in res and abs(j-flag_indirect)<10:
                                        res+=tmp_indirect+'\n'
                                    res+=sentences[j]+'\n'
                                    print(word1,word2)
                                    flag_direct = j
                                if word2.lower() in sentences[j] and not sentences[j] in res and word2=='':
                                    if "#" in sentences[j] and  not tmp_including in res :
                                        res+=tmp_including+'\n'
                                    if  not tmp_indirect in res and abs(j-flag_indirect)<10:
                                        res+=tmp_indirect+'\n'
                                    res += sentences[j] + '\n'
                                    print(word1, word2)
                                    flag_direct = j
                for word in Idirect_word:
                    for word1 in word[0]:
                        if word1.lower() in sentences[j]:
                            for word2 in word[1]:
                                if word2.lower() in sentences[j] :
                                    if  abs(j-flag_direct)<10 and not sentences[j] in res and flag_direct!=0 and (sentences[j][min(sentences[j].index(word1.lower()),sentences[j].index(word2.lower())):1+max(sentences[j].index(word1.lower()),sentences[j].index(word2.lower()))]).count(' ')<6:
                                        res+=sentences[j]+'\n'
                                        print(word1, word2)
                                        flag_indirect = j
                                        break
                                    if abs(j-flag_direct)<10 and not sentences[j] in res and flag_direct!=0 and word2=='':
                                        res+=sentences[j]+'\n'
                                        print(word1, word2)

                if ("includ" in sentences[j]) and  ":" in sentences[j] or ("provid" in sentences[j]) and  ":" in sentences[j]:
                    tmp_including = sentences[j]

        k += 1
    print(res)
    break
    # conn.execute(''' INSERT INTO 自然灾害风险描述 ('风险描述') values ("{}")'''.format(res))
    # 插入进去
    conn.execute('''UPDATE 自然灾害风险描述 SET 风险描述 = "{}" where ROWID = {}'''.format(res, i))
    conn.commit()


conn.close()
