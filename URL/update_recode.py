# -*- coding:utf8 -*-
import DB.Cur.get_db_cur as CUR
from OPERATIONS.get_page import get_per_page_info
import re
import urllib2
import cookielib
import sys
import datetime
from BeautifulSoup import BeautifulSoup
from Analysis import consult_h5_analysis,consult_deal_h5_analysis,hitted_h5_analysis,inquiry_deal_h5_analysis,obsolete_h5_analysis,inquiry_h5_analysis,change_h5_analysis,talks_deal_h5_analysis,talks_h5_analysis,render_h5_analysis
reload(sys)
sys.setdefaultencoding('utf-8')

# GLOBAL - 1 - 全局变量的申明
agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
prefix_url = 'www.ccgp-shaanxi.gov.cn/'


# GLOBAL - 2 - Url-links信息的抓取
def get_links_info(line_number, code, url, p_name, last_update_time):
    print "开始执行: " + str(p_name) + " 部分,Loading..."

    # 1 - 省.市.单一公告 的url前缀判断获取到底属于那个类型
    #     省级和市级的单一公告的url前缀是一样的
    sub_url_available = ['http://www.ccgp-shaanxi.gov.cn/zbAll_view.jsp?ClassName=',
                         'http://www.ccgp-shaanxi.gov.cn/zbAllDq_view.jsp?ClassName=',
                         'http://www.ccgp-shaanxi.gov.cn/publicityTool.jsp?NewsID=']
    if line_number < 12:
        sub_url = sub_url_available[0]
    elif 12 < line_number < 24:
        sub_url = sub_url_available[1]
    elif line_number % 12 == 0:
        sub_url = sub_url_available[2]
    else:
        pass

    # 2 - 加载cookie
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    request_index = urllib2.Request(url)
    request_index.add_header("User-Agent", agent)

    # 3 - 在网络情况不好的时候会超时,断定网络超时异常,循环提取
    while 1:
        try:
            response2 = urllib2.urlopen(request_index, timeout=60)
            html = response2.read()
            html = BeautifulSoup(html).__unicode__().decode('utf-8')
        except Exception:
            print str(repr(Exception)) + str(' :2')
            continue
        if html:
            break

    # 4 - 正则表达式群

    # eg:saveData.jsp?ClassBID=C0001
    rule_link = u"href=\"(.+?&)amp;ClassBID="
    # eg:type=AllView
    rule_flag = u"&amp;(.+?)\"\starget"
    # 链接是什么名字
    rule_name = u"class=\"b\">(.+?)</a>"
    # 总纪录共有多少页
    rule_page_num = u"<font\scolor=\"red\">(.+?)</font>"
    # url时间戳正则表达式
    date_num_flag = u"=[a-zA-Z]*([0-9]*)[US|&]"
    # 5 - 页数 总条数[0] 总页数[1] 每页多少条[2] 当前页数[3]
    page_num = re.compile(rule_page_num).findall(html)

    # 总条数(暂时没有用到,占位)
    all_line_num = page_num[0]
    # 总页数(用于百分比计数)
    all_page_num = page_num[1]

    """ old_time和max_update_time本质上是一样的，只不过old_time是原始值，我们不要动他,只让它在更新的时候进行比较
       而max_update_time因为是个副本，最后我们肯定要更新数据库的old_time，所以我们可以在最后回写old_time到数据库时用它来更新old_time
       相当于一个是比较标志，一个是最后要回写的最大值"""
    old_time = int(last_update_time)
    max_update_time = int(old_time)

    # 更新了多少条(计数)
    update_num = 0
    # 插入pro_info数据表模板
    sql = 'insert into pro_info(location_level,link_address,title_name,p_type,upload_date) VALUES '
    # 为了更好的效率使用一次insert形式，先将要插入的记录放在sal_add这个列表中，然后在下文实现相关的sql语句逻辑处理拼接
    sql_add = []

    # 区分省级和市级的标识
    if line_number < 13:
        location_level = 'province'
    else:
        location_level = 'city'

    """为了防止更新的条目不太多而总页数很大,然后可能导致我们更新一条记录却读了100页，做了很多无用功
      现在我设立一个标志update_flag,当我们发现项目的时间戳一只在比数据库的时间戳小，那么一定是出现了已经更新完，
      却还在向后读取页面的现象，这时候我们用这个标志数来断定，当项目时间戳小于数据库时间戳的个数已经有40条，
      那么就直接跳出循环，并告知增量的数据已经完成,但是如果一旦中途有项目时间戳比数据库时间戳大了，立刻置零重新计数"""
    update_flag = 0

    # 6 - 循环取页数,下载链接和标题
    for num in range(int(all_page_num)):  # all_page_num

        # 已经更新完,且不再继续向后页读取
        if update_flag >= 40:
            break

        # 打开第几页
        str_num = bytes(num + 1)
        # 请求URL
        request_index = urllib2.Request(sub_url + code + "&pages=" + str_num)
        # eg:http://www.ccgp-shaanxi.gov.cn/zbAll_view.jsp?ClassName=   C0001  &pages=    2
        # 添加头信息
        request_index.add_header("User-Agent", agent)

        # 注释: 解决网络较差的时候会出现超时或者打不开的情况
        timeout_flag = 0
        # print sub_url + code + "&pages=" + str_num
        while 1:
            try:
                response2 = urllib2.urlopen(request_index)
            except Exception:
                print str(repr(Exception)) + str(' :1')
                continue
            if response2:
                # print timeout_flag
                timeout_flag += 1
                break
        # 读取这个子页面
        html = response2.read()
        response2.close()
        html = BeautifulSoup(html).__unicode__().decode('utf-8')
        # [x]表示数据库必须要用的项
        # 匹配链接表达式[1]
        links_compile = re.compile(rule_link, re.M)
        # 匹配标题表达式[2]
        names_compile = re.compile(rule_name, re.DOTALL)
        # 匹配省/市标志表达式
        flags_compile = re.compile(rule_flag, re.M)
        # url上的时间戳获取表达式[3]
        date_compile = re.compile(date_num_flag)
        # 找到匹配信息的集合
        links = links_compile.findall(html)
        names = names_compile.findall(html)
        flags = flags_compile.findall(html)

        # 各个集合的长度
        links_len = len(links)
        names_len = len(names)
        flags_len = len(flags)

        # 当连接数目等于标识数目(有多少链接就有多少对应的名字)
        if (links_len == names_len):
            for i in range(links_len):  # links_len
                dates = date_compile.findall(links[i])
                if (int(dates[0]) > int(old_time)):
                    update_flag = 0
                    # 是否符合动态增量的条件
                    if (int(dates[0]) > int(max_update_time)):
                        # 现在的时间戳是不是比前面保存的时间戳大,如果是则将最新的时间戳保留，用作下次更新的数据库时间戳
                        max_update_time = dates[0]
                    else:
                        pass
                    p_date = '20' + dates[0][0:2] + '-' + dates[0][2:4] + '-' + dates[0][4:6] + ' ' + dates[0][
                                                                                                      6:8] + ':' + \
                             dates[0][8:10] + ':' + dates[0][10:]
                    # print '数据库时间戳：'+ str(old_time) +'当前时间戳：'+ dates[0] +"现在最大的时间戳是:" + max_update_time + 'pages:' + str_num+ 'pages:' + all_page_num
                    p_url = prefix_url + links[i] + flags[i]
                    update_num = update_num + 1

                    # sql中要insert的一条数据的拼接字符转
                    sql_value = '(\'' + location_level + '\',\'' + p_url + '\',\'' + names[
                        i].strip() + '\',\'' + code + '\',\'' + p_date + '\')'
                    # 将这条要insert的字符串放进列表，供后期拼接sql使用
                    sql_add.append(sql_value)
                    # print update_num
                elif (int(dates[0]) < int(old_time)):
                    update_flag += 1
                else:
                    pass
                    # # 进度条
                    # if update_flag > 0:
                    #     print '['+'|'*update_flag+' '*(40-update_flag)+']'
                    # else:
                    #     print '['+'|'*int((int(str_num) / 1.00) / (int(all_page_num) / 1.00) * 40)+' '*(40-int((int(str_num) / 1.00) / (int(all_page_num) / 1.00) * 40))+']'
                    # print str(line_number) + '/24 ' + 'Type' + ":" + location_level + ' ' + code + "->" + bytes(
                    #     (int(str_num) / 1.00) / (int(all_page_num) / 1.00) * 100) + "%"

    # sql语句的拼接处理逻辑
    string = ''
    # 只有当sql_add中有数据的时候才拼接然后入库处理，没有的话直接略过
    print "执行完成: " + p_name + " 部分,Over!"

    if sql_add:
        for i in range(len(sql_add)):
            if i < len(sql_add) - 1:
                string += sql_add[i] + ','
            else:
                string += sql_add[i]
        # sql记录links 信息的insert语句
        sql += string
        # sql2记录最大时间戳的update语句
        sql2 = 'update url_info set last_update_time = ' + str(
            max_update_time) + " where line_number = " + str(line_number)
        print "正在更新" + p_name + '  共有记录条数:' + str(update_num) + "\n"
        return sql, sql2
    else:
        print location_level + " " + p_name + " 没有新的记录需要更新!\n"
        return None


# GLOBAL - 3 - Links信息更新处理入库的主要操作函数
def update_recode():
    # 1 - 获取mysql数据库游标和连接接口
    p_cur = CUR.get_cur()
    cur = p_cur[0]
    conn = p_cur[1]

    # 2 - 获取 24 个页面的基本信息
    url = 'select * from url_info'
    url_info = cur.execute(url)
    info = cur.fetchmany(url_info)

    # 3 - 获取最大的项目编号(前)
    if 1 == 1:
        try:
            max_line_number_before = cur.execute('select max(t.line_number) from pro_info t')
        except Exception, e:
            print str(repr(e))
        finally:
            # 如果max_line_number_before存在则直接输出
            if max_line_number_before:
                pass
            # 如果max_line_number_before不存在则给默认值为0
            else:
                max_line_number_before = 0

    if url_info:
        # 初始化字典结构
        for per in info:
            dict_info = {'line_number': '', 'code': '', 'url': '', 'name': '', 'last_update_time': ''}
            dict_info['line_number'] = per[0]
            dict_info['code'] = per[1]
            dict_info['url'] = per[2]
            dict_info['name'] = per[3]
            dict_info['last_update_time'] = per[4]

            # 通过传入参数 获取 insert links信息的sql和修改最大时间戳的SQL语句
            results = get_links_info(per[0], per[1], per[2], per[3], per[4])
            if results:
                # 4 - 插入links信息
                cur.execute(results[0])
                # 5 - 更新时间戳
                cur.execute(results[1])
                # 6 - 每一个模块完成后进行一次提交
                cur.execute("commit")
            else:
                pass
    else:
        print '数据库类别表数据错误,请查验后运行重启服务!'

    # 7 - 对写入的页面进行信息获取与装载
    if 1 == 1:
        sql = 'select * from pro_info where line_number > ' + str(max_line_number_before)
        sql_result = cur.execute(sql)
        info = cur.fetchmany(sql_result)
        # 将存储的每个字典用list保存起来
        lst_info = []

        # 判断是否查询到数据
        if sql_result:
            # 将查询到的信息存在lst_info这个列表里
            print "正在装载单个页面的信息..."

            # 初始化字典结构
            for per in info:
                dict_info = {'line_number': '', 'code': '', 'url': '', 'name': '', 'last_update_time': ''}
                dict_info['line_number'] = per[0]
                dict_info['code'] = per[1]
                dict_info['url'] = per[2]
                dict_info['name'] = per[3]
                dict_info['last_update_time'] = per[4]
                url = 'http://' + str(dict_info['url'])

                # 获取没有处理的 html信息[0] 和处理过的 文本字符串信息[1]
                html_available_info = get_per_page_info(url)
                # 使转义符号\'失效 ,否则sql时inset会报错
                try:
                    # html信息经过字符处理转换成可以利用sql存储的文本
                    html_available_info[0] = html_available_info[0].replace('\"', '#tc1#')
                    html_available_info[0] = html_available_info[0].replace('\'', '#tc2#')

                    html_available_info[1] = ' '.join(html_available_info[1].split())

                    sql2 = 'insert into per_pro_info(pro_number,html_info,available_info,download_time) values' \
                           '(\"' + str(dict_info['line_number']) + '\",\"' + html_available_info[0] + '\",\'' \
                           + html_available_info[1] + '\',\'' + str(datetime.datetime.now()) + '\')'
                    # print sql2
                    print '存储页面有效信息进度:' + str(dict_info['line_number'] - max_line_number_before) + '/' + str(sql_result)
                    cur.execute(sql2)
                    # 每2百条1次commit
                    if dict_info['line_number'] % 200 == 0:
                        cur.execute('commit')
                        print dict_info['line_number'] + ' have commited!'
                    else:
                        pass
                except Exception, e:
                    continue
            cur.execute('commit')
        else:
            print '本次操作没有需要更新的记录!'

    # 8 - 获取最大的项目编号(后)
    if 1 == 1:
        try:
            max_line_number_after = cur.execute('select max(t.line_number) from pro_info t')
        except Exception, e:
            print str(repr(e))
        finally:
            # 如果max_line_number_after存在则直接输出
            if max_line_number_after:
                pass
            # 如果max_line_number_after不存在则给默认值为0
            else:
                max_line_number_after = 0

    # 9 - 详细信息提取入库
    if 1 == 1:
        def auto_insert_lib(max_number):
            # 页面信息提取入库函数
            if max_number > 0:
                # if code == 'C0001':
                render_h5_analysis._get_tender_info(max_number)
                # if code == 'D0002':
                talks_h5_analysis._get_talks_info(max_number)
                # if code == 'CS001':
                consult_h5_analysis._get_consult_info(max_number)
                # if code == 'D0003':
                inquiry_h5_analysis._get_inquiry_info(max_number)
                # if code == 'E0001':
                change_h5_analysis._get_change_info(max_number)
                # if code == 'FB001':
                obsolete_h5_analysis._get_obsolete_info(max_number)
                # if code == 'C0002':
                hitted_h5_analysis._get_hitted_info(max_number)
                # if code == 'D0001':
                talks_deal_h5_analysis._get_talks_deal_info(max_number)
                # if code == 'CS002':
                consult_deal_h5_analysis._get_consult_deal_info(max_number)
                # if code == 'DY001':
                #     pass
                # if code == 'XC001':
                inquiry_deal_h5_analysis._get_inquiry_deal_info(max_number)
                # if code == 'T0001':
                #     pass
    # - 关闭数据库游标和连接接口
    cur.close()
    conn.commit()
    conn.close()


# GLOBAL - X - 测试入口
if __name__ == "__main__":
    update_recode()
