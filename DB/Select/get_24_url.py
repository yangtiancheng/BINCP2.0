# -*- coding:utf8 -*-
import MySQLdb

# 1 - 获取24个url的信息
def mysql_conn():
    #  打开数据库连接
    try:
        # print '正在连接mysql数据库...'
        conn = MySQLdb.connect(

            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='123456',
            db='python',
            charset='utf8'
        )
        # print '数据库连接成功!'
    except Exception:
        # print '数据库连接异常:' + Exception;
        print 'Connection MysqlDB find error:' + Exception;

    cur = conn.cursor()

    # 将存储的每个字典用list保存起来
    lst_info = []

    # mysql查询条件
    url = 'select * from url_info'

    # mysql执行查询操作(long类型数据)
    url_info = cur.execute(url)

    # 获取查询到到的信息（tuple类型）
    info = cur.fetchmany(url_info)

    # 判断是否查询到数据
    if url_info:
        # 将查询到的信息存在lst_info这个列表里
        print '查询出%d条记录' % url_info

        # 初始化字典结构
        for per in info:
            dict_info = {'line_number': '', 'code': '', 'url': '', 'name': '', 'last_update_time': ''}
            dict_info['line_number'] = per[0]
            dict_info['code'] = per[1]
            dict_info['url'] = per[2]
            dict_info['name'] = per[3]
            dict_info['last_update_time'] = per[4]
            lst_info.append(dict_info)
    else:
        print '没有查询到任何记录'

    # 关闭游标
    cur.close()

    # 提交操作
    conn.commit()

    # 关闭数据库连接
    conn.close()

    # 打印查询到的数据
    # for i in lst_info:
    #     print i
    # 返回dict的list包含所有的select信息
    return lst_info
