# coding:utf-8
import datetime
from mysql import MysqlDB
import hashlib


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
        question, first_class_id, second_class_id,
        created, created, question_hash)

    questionTable.update(sql)


if __name__ == '__main__':
    questionTable = MysqlDB('corpustag_youthforumdata')
    firstCateTable = MysqlDB('corpustag_youthfirstcate')
    secondCateTable = MysqlDB('corpustag_youthsecondcate')
    question = 'agagagaga'
    first_cate = '教育成长'
    second_cate = '校园生活'
    insertDB(question, first_cate, second_cate)

    questionTable.close()
    firstCateTable.close()
    secondCateTable.close()
