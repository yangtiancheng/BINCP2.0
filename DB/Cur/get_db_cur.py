#-*- coding:utf8 -*-
import MySQLdb

def get_cur():
    """数据库游标获取"""
    # 打开数据库连接
    try:
        # print '正在连接mysql数据库...'
        conn = MySQLdb.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='123456',
            db='db2.0',
            charset='utf8'
        )
        # print '数据库连接成功!'
    except Exception:
        # print '数据库连接异常:' + Exception;
        print 'Connection MysqlDB find error:' + Exception;

    # 定义一个空列表，用于接收查询结果
    lst = []

    # 获取数据库链接的游标
    cur = conn.cursor()

    # 返回数据库的游标,使用过后记得关闭游标
    return [cur, conn]
