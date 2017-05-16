# -*- coding:utf8 -*-
# 磋商公告
import re

from DB.Cur import get_db_cur as analysis
from OPERATIONS.get_page import get_per_page_info as page_info
from BeautifulSoup import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def _get_operation(html):
    """网站的分析取值"""

    html = html.replace('</span>', '')
    html = html.replace('&nbsp;', ' ')
    html = html.replace('\"', '#tc1#')
    html = html.replace('\'', '#tc2#')
    html = html.replace('<h2>', '#title#')
    html = html.replace('</h2>', '#/title#')
    html = html.replace('</u>', '')
    html = html.replace('<u>', '')
    html = html.replace('</b>', '')
    html = html.replace('<b>', '')
    html = html.replace(':', '：')
    html = html.replace('</a>', '')
    html = html.replace('<br />', '')
    html = html.replace('<br>', '')
    html = html.replace('\r', '')

    p = re.compile(r'(<a.*?>)')
    pp = p.findall(html)
    pp = list(set(pp))
    for i in range(len(pp)):
        html = html.replace(pp[i], '')

    html2 = html
    p = re.compile(r'(<span.*?>)')
    pp = p.findall(html)
    pp = list(set(pp))
    for i in range(len(pp)):
        html = html.replace(pp[i], '')

    p = re.compile(r'(<span.*?>)')
    pp = p.findall(html2)
    pp = list(set(pp))
    for i in range(len(pp)):
        html2 = html2.replace(pp[i], ' ')

    # 不加这个可以获得较为完整的H5信息
    p = re.compile(r'(<.*?>)')
    pp = p.findall(html)
    pp = list(set(pp))
    for i in range(len(pp)):
        html = html.replace(pp[i], '')

    p = re.compile(r'(<.*?>)')
    pp = p.findall(html2)
    pp = list(set(pp))
    for i in range(len(pp)):
        html2 = html2.replace(pp[i], '')
    # 删除空行
    lst2 = """"""
    lst = html.split('\n')
    while '' in lst:
        lst.remove('')
    for i in lst:
        lst2 += i + "\n"
    html = lst2.encode("utf-8")

    lst2 = """"""
    lst = html2.split('\n')
    while '' in lst:
        lst.remove('')
    for i in lst:
        lst2 += i + "\n"
    html2 = lst2.encode("utf-8")

    # 打印处理后的H5 #
    # print html2

    # 局部变量定义
    # 标题
    title = ""

    # 项目名称
    program_name = ""

    # 项目编号
    program_num = ""

    # 采购人/单位名称
    purchase_unit_name = ""

    # 代购代理机构名称
    agency_orgaization_name = ""

    # 采购项目联系人
    purchase_contacts = []

    # 联系方式
    contact_info = []

    # 文件递交截止日期
    receiving_time = ""

    # 磋商时间
    begin_time = ""

    # 磋商地点
    begin_addr = ""

    try:
        # 标题正则
        title_rule = re.compile(r'#title#(.*?)#/title#')
        titles = title_rule.findall(html)
        if titles:
            # print title[0]
            title = titles[0]
        else:
            print '未找到 title name'
            # title = ' '

        # 采购项目名称
        program_rule = re.compile(r'(采购项目名称：|项目名称：|采购项目名称|项目名称)(.*)')
        programs = program_rule.findall(html)
        if programs:
            for i in range(len(programs)):
                if len(programs[i][1]) > 1:
                    # print "项目名称:" + program[i][1]
                    program_name = str(programs[i][1])
                    break
                else:
                    pass
                if i == len(programs) - 1:
                    break
        else:
            print '未找到 项目名称'
            # program_name = ' '

        # 采购项目编号
        program_num_rule = re.compile(r'(项目编号：|招标编号：|采购编号：|编号：)(.*)')
        program_nums = program_num_rule.findall(html)
        if program_nums:
            for i in range(len(program_nums)):
                if len(program_nums[i][1]) > 1:
                    # print "采购项目编号:" + program_num[i][1]
                    program_num = str(program_nums[i][1])
                else:
                    program_num_rule = re.compile(r'(项目编号：|招标编号：|采购编号：|编号：)\n(.*)')
                    program_nums = program_num_rule.findall(html)
                    program_num = str(program_nums[i][1])

                if i == len(program_nums) - 1:
                    break
        else:
            print '未找到 项目编号'
            # program_num = ' '

        # 采购人/单位名称
        purchase_rule = re.compile(r'(采购人：|采购人名称：|采购单位名称：|单位名称：|采购方名称：|采购单位：)(.*)')
        purchases = purchase_rule.findall(html)
        if purchases:
            # 输出匹配到的字符串
            for i in range(len(purchases)):
                if len(purchases[i][1]) > 1:
                    # print "采购人/单位名称:" + purchase[i][1]
                    purchase_unit_name = str(purchases[i][1])
                else:
                    purchase_rule = re.compile(r'(采购人：|采购人名称：|采购单位名称：|单位名称：|采购方名称：|采购单位：)\n(.*)')
                    purchases = purchase_rule.findall(html)
                    purchase_unit_name = str(purchases[i][1])
                if i == len(purchases) - 1:
                    break
        else:
            purchase = '未找到 采购人名称'
            # purchase_unit_name = ' '

        # 采购代理机构名称
        organization_rule = re.compile(r'(机构：|招标机构：|组织单位：|代理机构名称：|采购代理机构：|代理机构：|机构名称：|采购机构：|采购代理单位：|代理单位：)(.*)')
        organizations = organization_rule.findall(html)
        if organizations:
            for i in range(len(organizations)):
                if len(organizations[i][1]) > 1:
                    # print "采购代理机构名称:" + organization[i][1]
                    agency_orgaization_name = str(organizations[i][1])
                    break
                else:
                    organization_rule = re.compile(r'(机构：|招标机构：|组织单位：|代理机构名称：|采购代理机构：|代理机构：|机构名称：|采购机构：|采购代理单位：|代理单位：)\n(.*)')
                    organizations = organization_rule.findall(html)
                    agency_orgaization_name = str(organizations[i][1])
                if i == len(organizations) - 1:
                    break
        else:
            print '未找到 采购代理机构名称'
            # agency_orgaization_name = ' '

        # 采购项目联系人（最后一个是采购项目联系人）
        pro_purchase_rule1 = re.compile(r'(负\s*责\s*人：|采购项目联系人：|联系人及电话：|联\s*系\s*人：)(.*)')
        pro_purchase_rule2 = re.compile(r'(负\s*责\s*人：|采购项目联系人：|联系人及电话：|联\s*系\s*人：)\n(.*)')
        pro_purchase1 = pro_purchase_rule1.findall(html2)
        pro_purchase2 = pro_purchase_rule2.findall(html2)
        if pro_purchase1 or pro_purchase2:
            variable_string = []
            if pro_purchase1:
                for i in range(len(pro_purchase1)):
                    if len(pro_purchase1[i][1]) > 1:
                        # print "采购项目联系人:" + pro_purchase[i][1]
                        variable_string.append(str(pro_purchase1[i][1]))
            if pro_purchase2:
                for i in range(len(pro_purchase2)):
                    if len(pro_purchase2[i][1]) > 1:
                        # print "采购项目联系人:" + pro_purchase[i][1]
                        variable_string.append(str(pro_purchase2[i][1]))

            purchase_contacts = variable_string
        else:
            print '未找到 采购项目联系人'

        # 联系方式(最后一个一定是采购人联系方式)
        contact_info_rule1 = re.compile(r'(联\s*系\s*方\s*式：|联\s*系\s*电\s*话：|联\s*系\s*方\s*式\s*（电\s*话\s*/\s*传\s*真）：|联\s*系\s*方\s*式（传\s*真）：|联\s*系\s*方\s*式（电\s*话）：|电\s*话\s*/\s*传\s*真：|电\s*话\s*)(.*)')
        contact_info_rule2 = re.compile(r'(联\s*系\s*方\s*式：|联\s*系\s*电\s*话：|联\s*系\s*方\s*式\s*（电\s*话\s*/\s*传\s*真）：|联\s*系\s*方\s*式（传\s*真）：|联\s*系\s*方\s*式（电\s*话）：|电\s*话\s*/\s*传\s*真：|电\s*话\s*)(\n)(.*)')
        contact_infos1 = contact_info_rule1.findall(html)
        contact_infos2 = contact_info_rule2.findall(html)
        if contact_infos1 or contact_infos2:
            variable_string = []
            if contact_infos1:
                for i in range(len(contact_infos1)):
                    if len(contact_infos1[i][1]) > 1:
                        # print "采购项目联系人:" + pro_purchase[i][1]
                        variable_string.append(str(contact_infos1[i][1]))
            if contact_infos2:
                for i in range(len(contact_infos2)):
                    if len(contact_infos2[i][1]) > 1:
                        # print "采购项目联系人:" + pro_purchase[i][1]
                        variable_string.append(str(contact_infos2[i][2]))
            contact_info = variable_string
        else:
            print '未找到 联系方式'

        # 投标文件接收截止时间
        receiving_time_rule = re.compile(r'(递交时间：|截止时间：|截止日期：|日 期：|递交时间：|递交截止时间及磋商时间：|时 间：)(.*)')
        receiving_times = receiving_time_rule.findall(html)
        if receiving_times:
            for i in range(len(receiving_times)):
                if len(receiving_times[i][1]) > 1:
                    # print "文件接收截止时间:" + receiving_time[i][1]
                    receiving_time = receiving_times[i][1]
                    break
                else:
                    receiving_time_rule = re.compile(r'(递交时间：|截止时间：|投标截止日期：|日\s*期：|递交时间：|递交截止时间及磋商时间：|时\s*间：)\n(.*)')
                    receiving_times = receiving_time_rule.findall(html)
                    receiving_time = receiving_times[i][1]
                    break
        else:
            print '未找到 投标文件接收截止时间'
            # p_receiving_time = ' '

        # 谈判时间
        begin_time_rule = re.compile(r'(时间）：|大\s*会\s*时\s*间：|开\s*启\s*时\s*间：|磋\s*商\s*时\s*间：|时\s*间：|日\s*期：)(.*)')
        begin_times = begin_time_rule.findall(html)
        if begin_times:
            for i in range(len(begin_times)):
                if len(begin_times[i][1]) > 1:
                    # print "开标时间:" + begin_time[i][1]
                    begin_time = begin_times[i][1]
                    break
                else:
                    begin_time_rule = re.compile(r'(时间）：|大\s*会\s*时\s*间：|开\s*启\s*时\s*间：|磋\s*商\s*时\s*间：|时\s*间：|日\s*期：)\n(.*)')
                    begin_times = begin_time_rule.findall(html)
                    begin_time = begin_times[i][1]
                    break
        else:
            print '未找到 谈判时间'
            # p_begin_time = ' '

        # 谈判地点
        begin_addr_rule = re.compile(r'(地点）：|会\s*议\s*地\s*点：|开\s*标\s*地\s*点：|磋\s*商\s*地\s*点：| 地\s*址：|竞\s*谈\s*地\s*点：|召\s*开\s*地\s*点：|大\s*会\s*地\s*点：|\s+地\s*点：|、地\s*点：|.地\s*点：)(.*)')
        begin_addrs = begin_addr_rule.findall(html)
        if begin_addrs:
            for i in range(len(begin_addrs)):
                if len(begin_addrs[i][1]) > 1:
                    # print "地点:" + begin_addr[i][1]
                    begin_addr = begin_addrs[i][1]
                    break
                else:
                    begin_addr_rule = re.compile(r'(地点）：|会\s*议\s*地\s*点：|开\s*标\s*地\s*点：|磋\s*商\s*地\s*点：| 地\s*址：|竞\s*谈\s*地\s*点：|召\s*开\s*地\s*点：|大\s*会\s*地\s*点：|\s+地\s*点：|、地\s*点：|.地\s*点：)\n(.*)')
                    begin_addrs = begin_addr_rule.findall(html)
                    begin_addr = begin_addrs[0][1]
                    break
        else:
            print '未找到 谈判地点'
            # p_begin_addr = ' '

    except Exception, e:
        print str(repr(e))+"<1>"
    # -----------------信息手动处理--------------------


    if title:
        if not program_name:
            program_name = title.replace('公告', '')
            # '谈判时间'不存在 ’截止时间’存在 默认截止时间
    if not begin_time:
        if receiving_time:
            begin_time = receiving_time
        if not receiving_time:
            begin_time = "未提及"
            receiving_time = "未提及"

    # '截止时间'不存在 ’谈判时间’存在 默认谈判时间
    if begin_time:
        if not receiving_time:
            receiving_time = begin_time
        if receiving_time:
            pass
    # 如果项目名称不能获取 就取标题名
    if program_name == '':
        program_name = title

    # 处理字段 防止sql出问题
    if title == "":
        title = "Not Found"
    if program_name == "":
        program_name = "Not Found"
    if program_num == "":
        program_num = "Not Found"
    if purchase_unit_name == "":
        purchase_unit_name = "Not Found"
    if agency_orgaization_name == "":
        agency_orgaization_name = "Not Found"
    if not purchase_contacts:
        purchase_contacts.append("Not Found",)
    if not contact_info:
        contact_info.append("Not Found",)
    # 文件递交截止日期
    if receiving_time == "":
        receiving_time = "Not Found"
    # 谈判时间
    if begin_time == "":
        begin_time = "Not Found"
    # 谈判地点
    if begin_addr == "":
        begin_addr = "Not Found"


    info = {'p_title': title,
            'p_program_name': program_name,
            'p_program_num': program_num,
            'p_purchase_unit_name': purchase_unit_name,
            'p_agency_orgaization_name': agency_orgaization_name,
            'p_purchase_contacts': purchase_contacts,
            'p_contact_info': contact_info,
            'p_receiving_time': receiving_time,
            'p_begin_time': begin_time,
            'p_begin_addr': begin_addr,
            }
    return info


def _get_consult_info(max_number):
    """获取招标网站的信息"""
    info = []
    string = ''
    url_prefix = 'http://'
    url_suffix = ''

    # 获取数据库游标和连接口(用于调用和关闭)
    db_request = analysis.get_cur()

    # 获取数据库游标
    cur = db_request[0]

    # 获取连接口
    conn = db_request[1]

    # 定义一个空列表，用于接收查询结果 用于后期扩展速率
    lst = []

    sql = """
        select link_address,line_number
        from pro_info pi
        where pi.p_type = "CS001"
        and pi.line_number > """
    sql += str(max_number)

    sql +="""
        order by upload_date
        ;"""
    # 获取url
    cur_result = cur.execute(sql)

    # ----------------------------------------------------------------------------------------------#
    # 批量
    #
    # 打算每10条一次commit
    commit_flag = 0
    #
    # 利用游标,获取所有结果
    result = cur.fetchmany(cur_result)

    # 如果结果存在 遍历入库
    if result:
        for each_lst in result:
            commit_flag += 1

            # 获取地址 www.****
            url_suffix = each_lst[0]
            pro_number = each_lst[1]
            # 拼接成完整链接 http://www.****
            url = url_prefix + url_suffix
            print url

            # 过去网页信息
            p_list = page_info(url)

            # 获取单个网页的元素信息
            try:
                result_info = _get_operation(p_list[0])
                # p_lst.append(result_info)

                if not result_info['p_program_name']:
                    print "项目名称:不存在" + url
                sql2 = ""
                sql2 += "insert into all_detail_info(" \
                        "title,pro_number," \
                        "program_name," \
                        "program_num, " \
                        "purchase_unit_name ," \
                        "agency_orgaization_name," \
                        "purchase_contacts, " \
                        "contact_info, " \
                        "receiving_time, " \
                        "begin_time, " \
                        "begin_addr, " \
                        "url,types" \
                        ") values" \
                        u"(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % \
                        (result_info['p_title'],
                         pro_number,
                         result_info['p_program_name'],
                         result_info['p_program_num'],
                         result_info['p_purchase_unit_name'],
                         result_info['p_agency_orgaization_name'],
                         result_info['p_purchase_contacts'][-1],
                         result_info['p_contact_info'][-1],
                         result_info['p_receiving_time'],
                         result_info['p_begin_time'],
                         result_info['p_begin_addr'],
                         url,'CS001')
                # print sql2

                cur.execute(sql2)
                cur.execute('commit')
                # # 标题
                # print "标题 " + result_info["p_title"]
                #
                # # 项目名称
                # print "项目名称 " + result_info["p_program_name"]
                #
                # # 项目编号
                # print "项目编号 " + result_info["p_program_num"]
                #
                # # 采购人/单位名称
                # print "采购人/单位名称 " + result_info["p_purchase_unit_name"]
                #
                # # 代购代理机构名称
                # print "代购代理机构名称 " + result_info["p_agency_orgaization_name"]
                #
                # # 采购项目联系人
                # if result_info["p_purchase_contacts"]:
                #     print "采购项目联系人 " + str(result_info["p_purchase_contacts"][-1])
                # if result_info["p_contact_info"]:
                #     # 联系方式
                #     print "联系方式 " + str(result_info["p_contact_info"][-1])
                # # 投递文件截止时间
                # print "投递文件截止时间 " + result_info["p_receiving_time"]
                # # 谈判时间
                # print "磋商时间 " + result_info["p_begin_time"]
                # # 谈判地点
                # print "磋商地点 " + result_info["p_begin_addr"]

                # # url
                # print "url " + url

                print 'render number:' + str(commit_flag) + '/' + str(cur_result)
                # print '\n\n'
            except Exception, e:
                print str(repr(e))+"<2>"
                continue
    # ----------------------------------------------------------------------------------------------#

    # 关闭游标
    cur.close()

    # 提交操作
    conn.commit()

    # 关闭数据库连接
    conn.close()


# 调用测试方法
# _get_consult_info(0)
