# 此文件是将文本存入数据库
# 在此之前，先要有自己的数据库文件，
# 如果没有可能，连接到我的  test.db中
# 文本文件，执行一次，会在表中插入所有文件，如果要更新表格，需要将表格 TABLE1 删除

import sqlite3
import os
import json

# 此处路径替换为自己的文件路径
dir = os.listdir(r'./抽查数据600/鎶芥煡鏁版嵁600')
for i in dir:
    path = r"抽查数据600/鎶芥煡鏁版嵁600/" + i
    if path == r'抽查数据600/鎶芥煡鏁版嵁600/desktop.ini': continue
    print(path)
    with open(path, 'r', encoding='UTF-8') as f:
        rows = json.loads(f.read().encode().decode('utf-8'), encoding='UTF-8')

    conn = sqlite3.connect('test.db')

    # 这个是新建一个地方数据库表
    conn.execute('''
    CREATE TABLE IF NOT exists TABLE1
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
    风险因子 TEXT
    );
    ''')

    # 对文本做了部分处理，可以不修改
    rows['风险因子']=rows['风险因子'].replace("(",' ')[:]
    rows['风险因子']=rows['风险因子'].replace(")",' ')[:]
    rows['风险因子']=rows['风险因子'].replace("{",' ')[:]
    rows['风险因子']=rows['风险因子'].replace("}",' ')[:]
    rows['风险因子']=rows['风险因子'].replace("'",' ')[:]
    rows['风险因子']=rows['风险因子'].replace('"',' ')[:]
    rows['风险因子']=rows['风险因子'].replace('[',' ')[:]
    rows['风险因子']=rows['风险因子'].replace(']',' ')[:]
    rows['风险因子']=rows['风险因子'].replace(',',' ')[:]
    rows['风险因子']=rows['风险因子'].replace('·','##')[:]
    rows['风险因子']=rows['风险因子'].replace('•','##')[:]
    rows['风险因子']=rows['风险因子'].replace('u.s. ','US')[:]
    rows['风险因子']=rows['风险因子'].replace('vs.','vs')[:]
    rows['风险因子']=rows['风险因子'].replace('\\n','')[:]
    # for i in range(len(rows['风险因子'])):
    #     #
    #     tmp =rows['风险因子'][i]
    #     if rows['风险因子'][i] == "#" and i > 5:
    #         rows['风险因子'] = rows['风险因子'][:i-5]+'#'+rows['风险因子'][i+1:]

    # for i in range(len(rows['风险因子'])):
    #     # 将多余的换行符去掉
    #     tmp =rows['风险因子'][i - 1:i]
    #     if rows['风险因子'][i - 2:i] == "\\n" and i > 2:
    #         rows['风险因子'] = rows['风险因子'][:i-2]+rows['风险因子'][i+1:]


    for i in range(len(rows['风险因子'])):
        # # 将文本中的为分段的内容，添加 \n 进行分段标记
        if (rows['风险因子'][i - 8:i] == '--------' and i > 11) :
            rows['风险因子'] = rows['风险因子'][:i]+'\\n'+rows['风险因子'][i:]
    i = 0

    while(i<len(rows['风险因子'])):
        # 将每个标题前描述段，加上换行符
        tmp = rows['风险因子'][i:i+5]
        if (rows['风险因子'][i:i+5].isupper() and i > 10) and i<len(rows['风险因子'])-10 and  not rows['风险因子'][i-6:i].isupper():
            rows['风险因子'] = rows['风险因子'][:i-1]+'\\n'+rows['风险因子'][i:]
            i = i+2
            while(rows['风险因子'][i:i+2].isupper()):
                i+=1
        # if rows['风险因子'][i] == "@":
        #     rows['风险因子'] = rows['风险因子'][:i-1] + '\\n' + rows['风险因子'][i-1:]
        #     i = i + 2

        i+=1
    # 这个’#‘用来标记 关键词列举的情况
    rows['风险因子'] = rows['风险因子'].replace('#', '.#')
        # if rows['风险因子'][i] in '''",'[]{}?! ''':
        #     # print(i)
        #     rows['风险因子'] = rows['风险因子'][:(rows['风险因子']).index(rows['风险因子'][i])] + " " + rows['风险因子'][
        #                                                                         (rows['风险因子']).index(rows['风险因子'][i]) + 1:]

    # 进文件插入到刚才新建的表里
    sql = '''INSERT INTO TABLE1 ("oid","CIK","公司","年报类型","时间","文本链接","网页链接","具体链接","年","季度","财政年","CONFORMED_SUBMISSION_TYPE","COMPANY_CONFORMED_NAME","CENTRAL_INDEX_KEY","STANDARD_INDUSTRIAL_CLASSIFICATION","CITY","STATE","PUBLIC_DOCUMENT_COUNT","FILED_AS_OF_DATE","DATE_AS_OF_CHANGE","ABS_ASSET_CLASS","STATE_OF_INCORPORATION","SEC_ACT","SEC_FILE_NUMBER","FILM_NUMBER","STREET_1","ZIP","BUSINESS_PHONE","风险因子")values("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'''.format(
        rows['oid'],
        rows['CIK'],
        rows['公司'],
        rows['年报类型'],
        rows['时间'],
        rows['文本链接'],
        rows['网页链接'],
        rows['具体链接'],
        rows['年'],
        rows['季度'],
        rows['财政年'],
        rows['CONFORMED_SUBMISSION_TYPE'],
        rows['COMPANY_CONFORMED_NAME'],
        rows['CENTRAL_INDEX_KEY'],
        rows['STANDARD_INDUSTRIAL_CLASSIFICATION'],
        rows['CITY'],
        rows['STATE'],
        rows['PUBLIC_DOCUMENT_COUNT'],
        rows['FILED_AS_OF_DATE'],
        rows['DATE_AS_OF_CHANGE'],
        rows['ABS_ASSET_CLASS'],
        rows['STATE_OF_INCORPORATION'],
        rows['SEC_ACT'],
        rows['SEC_FILE_NUMBER'],
        rows['FILM_NUMBER'],
        rows['STREET_1'],
        rows['ZIP'],
        rows['BUSINESS_PHONE'],
        rows['风险因子'])

    conn.execute(sql)
    conn.commit()
conn.close()
