# coding:utf-8
import datetime
from mysql import MysqlDB
import hashlib
import xlrd
import json
from collections import Counter
import requests
import time

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
"""
测试用例
"""


def tag_second_class():

    in_file = '/Users/zhangliujie/Documents/project/Youth_data_clean/clean/170621question19.txt'
    # out_file = '../visualization/data_19.txt'
    url = "http://10.108.216.166:5000/predict/secondclass"

    with open(in_file, 'r') as fr:
        cnt = 1
        for data in fr:
            if len(data) < 6:
                continue
            try:
                postdata = {
                    'text': data
                }
                res = json.loads(requests.post(url, postdata).text)
                first_class = res["ML_label"]["first_class"]
                second_class = res["ML_label"]["second_class"]
                tags = ' '.join(res["ML_label"]["tags"])
                # info = ''
                # for key, val in res["ML_label"]["second_class_info"].items():
                #     info += ' %s:%s ' % (key, val)
                # cont_split = [first_class, second_class, tags, data]
                # print(cont_split)
                insertDB(data.encode('utf-8'), first_class, second_class, tags)
                # fw.writelines('@@@'.join(cont_split))
                # time.sleep(1)
                cnt += 1
            except Exception as e:
                print(e)
                print(' '.join([first_class, second_class, tags]))
                print('failed to deal %s .' % data)
            # if cnt == 500:
            #     print('%s : deal line : %s' %
            #           (time.asctime(time.localtime(time.time())), cnt))


def insertDB(question, first_cate, second_cate, tags):

    first_class_id = firstCateTable.query(
        "select id from corpustag_youthfirstcate where name='{}'".format(
            first_cate))[0][0]
    print(first_class_id)
    second_class_id = secondCateTable.query(
        "select id from corpustag_youthsecondcate where name='{}'".format(
            second_cate))[0][0]
    print(second_class_id)
    m = hashlib.md5()
    m.update(question.encode('utf8'))
    # 十六进制
    question_hash = m.hexdigest()
    created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = "insert into corpustag_youthforumdata \
    (question_text, first_class_id, second_class_id, tags,\
    created, modified, mlHit, question_hash) values \
    ('{}', {}, {}, '{}', '{}', '{}', 'unknown', '{}');".format(
        question, first_class_id, second_class_id, tags, created, created,
        question_hash)
    questionTable.update(sql)


def readExcelByCol(file_name, col):
    '''
    按列读取excel数据
    :param file_name: excel路径
    :param col: 列数,可以多列,或者单列
    :return: 迭代器 可调用next(gener)来返回数据
    '''
    wb = xlrd.open_workbook(file_name)
    sheet = wb.sheet_by_index(0)

    if isinstance(col, list):
        for i in col:
            yield sheet.col_values(i)
    elif isinstance(col, int):
        data = sheet.col_values(col)
        yield data


def excel2mysql():
    cates = json.load(open('./classConf.json', 'r'))
    datas, first_class, labels = readExcelByCol('./corpus/train_corpus/创业.xlsx', [0, 1, 3])
    datas = [x.split('@@@')[-1] for x in datas]
    print(len(labels))
    # for i in range(len(first_class)):
    #     if first_class[i] != 'SH':
    #         labels[i] = 'unknown'
    # first_class = '理想信念'
    first_class = ['CY' if x == '' else x for x in first_class]
    print(Counter(first_class))
    labels = ['' if str(int(lbl)) == '6' else lbl for lbl in labels]
    labels = [
        cates[first_class[i]][str(int(lbl))]
        if lbl not in ['', '.'] else 'unknown'
        for i, lbl in enumerate(labels)
    ]
    first_class = [
        cates[x]['CN'] for x in first_class
    ]
    # first_class = cates['CY']['CN']

    print(Counter(first_class))
    print(Counter(labels))
    assert len(first_class) == len(labels)
    print(datas[-10:])
    print(labels[-10:])


if __name__ == '__main__':
    # 初始化 表
    try:
        questionTable = MysqlDB('corpustag_youthforumdata')
        firstCateTable = MysqlDB('corpustag_youthfirstcate')
        secondCateTable = MysqlDB('corpustag_youthsecondcate')

        tag_second_class()
    except:
        print()
    # extractKw('../docs/second_class_corpus/train_corpus/人文科技.xls')

    questionTable.close()
    firstCateTable.close()
    secondCateTable.close()
