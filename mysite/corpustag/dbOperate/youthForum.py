# coding:utf-8
import datetime
from mysql import MysqlDB
import hashlib
import xlrd
import json


def insertDB(question, first_cate, second_cate):

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
    (question_text, first_class_id, second_class_id, \
    created, modified, mlHit, question_hash) values \
    ('{}', {}, {}, '{}', '{}', 'unknown', '{}');".format(
        question, first_class_id, second_class_id, created, created,
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


if __name__ == '__main__':
    cates = json.load(open('./classConf.json', 'r'))
    datas, _labels = readExcelByCol('./corpus/人文_新二级.xlsx', [0, 2])
    datas = [x.split('@@@')[-1] for x in datas]
    print(len(_labels))
    labels = [
        cates['RW'][str(int(lbl))]
        if lbl not in ['', '  '] and str(int(lbl)) != '0' else 'unknown' for lbl in _labels
    ]
    # first_class = cates['CY']['CN']
    first_class = [
        cates['RW']['CN'] if lbl in ['', '  '] or str(int(lbl)) != '0' else 'unknown'
        for lbl in _labels
    ]
    # print(datas[-10:])
    # print(labels[-10:])
    # print(first_class[-10:])
    # print(len([i for i, lbl in enumerate(first_class) if lbl == 'unknown']))
    # exit()
    questionTable = MysqlDB('corpustag_youthforumdata')
    firstCateTable = MysqlDB('corpustag_youthfirstcate')
    secondCateTable = MysqlDB('corpustag_youthsecondcate')
    for i, question in enumerate(datas):
        try:
            insertDB(question, first_class[i], labels[i])
        except Exception as e:
            print(e)

    questionTable.close()
    firstCateTable.close()
    secondCateTable.close()
