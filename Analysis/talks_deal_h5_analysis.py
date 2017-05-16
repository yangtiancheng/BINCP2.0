# -*- coding:utf8 -*-
# 谈判成交公告
import re
from DB.Cur import get_db_cur as analysis
from OPERATIONS.get_page import get_per_page_info as page_info
from BeautifulSoup import BeautifulSoup


def _get_operation(html):
    """中标网站的分析取值"""
    info = []
    string = ''

    html = html.replace('</span>', '')
    html = html.replace('&nbsp;', '')
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
    # print html

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

    # 成交供应商(可能有多个)
    hitted_orgaization_name = ""

    # 谈判小组成员名单
    judgor_name = ""

    # 采购项目联系人
    purchase_contacts = []

    # 联系方式
    contact_info = []
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
                    program_name = str(programs[i][1]).replace('\r', '')
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
                    program_num = str(program_nums[i][1]).replace('\r', '')
                else:
                    program_num_rule = re.compile(r'(项目编号：|招标编号：|采购编号：|编号：)\n(.*)')
                    program_nums = program_num_rule.findall(html)
                    program_num = str(program_nums[i][1]).replace('\r', '')

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
                    purchase_unit_name = str(purchases[i][1]).replace('\r', '')
                else:
                    purchase_rule = re.compile(r'(采购人：|采购人名称：|采购单位名称：|单位名称：|采购方名称：|采购单位：)\n(.*)')
                    purchases = purchase_rule.findall(html)
                    purchase_unit_name = str(purchases[i][1]).replace('\r', '')
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
                    agency_orgaization_name = str(organizations[i][1]).replace('\r', '')
                    break
                else:
                    organization_rule = re.compile(r'(机构：|招标机构：|组织单位：|代理机构名称：|采购代理机构：|代理机构：|机构名称：|采购机构：|采购代理单位：|代理单位：)\n(.*)')
                    organizations = organization_rule.findall(html)
                    agency_orgaization_name = str(organizations[i][1]).replace('\r', '')
                if i == len(organizations) - 1:
                    break
        else:
            print '未找到 采购代理机构名称'
            # agency_orgaization_name = ' '

        # 中标单位
        hitted_orgaization_name_rule = re.compile(
            r'(招标结果：|中标社会资本方：|成交企业：|单位排序如下:|供应商\d：|成交单位：|成交单位\d：|成交服务商：|供应商名称：|供应商：|成交人：|报价人：|候选人：|供应商候选人排序：|成交供应商：|单位如下：|预审单位名单如下：|中标单位：|中标供应商：|中标供应商名称：|中标人：|供应商：|第一名：|中标服务商：|成交单位：|入围单位：|中 标 人：|中标人：)(.*)')
        hitted_orgaization_names = hitted_orgaization_name_rule.findall(html)
        hit_string = ""
        if hitted_orgaization_names:
            # print hitted_orgaization_names
            for i in range(len(hitted_orgaization_names)):
                if len(hitted_orgaization_names[i][1]) > 1:
                    hit_string += str(hitted_orgaization_names[i][1]).replace('\r', '') + '<>'
                else:
                    hitted_orgaization_name_rule2 = re.compile(
                        r'(招标结果：|：|成交企业：|单位排序如下:|成交供应商：|供应商\d：|成交单位：|成交单位\d：|成交服务商：|供应商名称：|供应商：|成交人：|报价人：|候选人：|供应商候选人排序：|成交供应商：|单位如下：|预审单位名单如下：|中标单位：|中标供应商：|中标供应商名称：|中标人：|供应商：|第一名：|中标服务商：|成交单位：|入围单位：|中 标 人：|中标人：)\n(.*)')
                    hitted_orgaization_names = hitted_orgaization_name_rule2.findall(html)
                    hit_string = ""
                    if hitted_orgaization_names:
                        # print hitted_orgaization_names
                        for i in range(len(hitted_orgaization_names)):
                            if len(hitted_orgaization_names[i][1]) > 1:
                                hit_string += str(hitted_orgaization_names[i][1]).replace('\r', '') + '<>'
                            else:
                                pass
            hitted_orgaization_name = hit_string
        else:
            print '未找到 成交单位'
            # hitted_orgaization_name = ' '

        # 评标委员会成员
        judgor_name_rule = re.compile(
            r'(评标委员会成员名单：|评标委员会成员名单：|成员名单：|评标委员会成员：|评标小组成员：|成员：|小组人员：|人员：|评标委员会人员：|评标委员.*）：|评标委员会名单：|评审专家|专家|评标委员会：|委员会：|委员： |人员名单：|谈判小组：|小组名单：|名单：|小组成员：)(.*)')
        judgor_names = judgor_name_rule.findall(html2)
        if judgor_names:
            for i in range(len(judgor_names)):
                if len(judgor_names[i][1]) > 1 and judgor_names[i][1] != '\r':
                    # print "采购项目联系人:" + pro_purchase[i][1]
                    judgor_name = str(judgor_names[i][1]).replace('\r', '')
                    break
                else:
                    judgor_name_rule2 = re.compile(
                        r'(评标委员会成员名单：|评标委员会成员名单：|成员名单：|评标委员会成员：|评标小组成员：|成员：|小组人员：|人员：|评标委员会人员：|评标委员.*）：|评标委员会名单：|评审专家|专家|评标委员会：|委员会：|委员：|人员名单：|谈判小组：|小组名单：|名单：|小组成员：)\s*\n(.*)')
                    judgor_names = judgor_name_rule2.findall(html2)
                    if judgor_names:
                        judgor_name = str(judgor_names[i][1])
                    break
                if i == len(judgor_name) - 1:
                    break
        else:
            print '未找到 评标委员会成员'

        # 采购项目联系人（最后一个是采购项目联系人）
        pro_purchase_rule = re.compile(r'(采购项目联系人：|联系人：|联系人及电话：|联 系 人：|联  系  人：)(.*)')
        pro_purchase = pro_purchase_rule.findall(html)
        if pro_purchase:
            variable_string = []
            for i in range(len(pro_purchase)):
                if len(pro_purchase[i][1]) > 1:
                    # print "采购项目联系人:" + pro_purchase[i][1]
                    variable_string.append(str(pro_purchase[i][1]).replace('\r', ''))
                else:
                    pro_purchase_rule = re.compile(r'(采购项目联系人：|联系人：|联系人及电话：|联 系 人：|联  系  人：)\n(.*)')
                    pro_purchase = pro_purchase_rule.findall(html)
                    variable_string.append(str(pro_purchase[i][1]).replace('\r', ''))
            purchase_contacts = variable_string
        else:
            print '未找到 采购项目联系人'

        # 联系方式(最后一个一定是采购人联系方式)
        contact_info_rule = re.compile(r'(联系方式：|联系电话：|联系方式（电话/传真）：|联系方式（传真）：|联系方式（电话）：)(.*)')
        contact_infos = contact_info_rule.findall(html)
        if contact_infos:
            variable_string = []
            for i in range(len(contact_infos)):
                if len(contact_infos[i][1]) > 1:
                    # print "采购项目联系人:" + pro_purchase[i][1]
                    variable_string.append(str(contact_infos[i][1]).replace('\r', ''))
                else:
                    contact_info_rule = re.compile(r'(联系方式：|联系电话：|联系方式（电话/传真）：|联系方式（传真）：|联系方式（电话）：)\n(.*)')
                    contact_infos = contact_info_rule.findall(html)
                    variable_string.append(str(contact_infos[i][1]).replace('\r', ''))
                contact_info = variable_string
        else:
            print '未找到 联系方式'
    except Exception, e:
        print str(repr(e))
    # -----------------信息手动处理--------------------


    if title:
        if not program_name:
            program_name = title.replace('公告', '')

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

    info = {'p_title': title,
            'p_program_name': program_name,
            'p_program_num': program_num,
            'p_purchase_unit_name': purchase_unit_name,
            'p_agency_orgaization_name': agency_orgaization_name,
            'p_hitted_orgaization_name': hitted_orgaization_name,
            'p_judgor_name': judgor_name,
            'p_purchase_contacts': purchase_contacts,
            'p_contact_info': contact_info,
            }
    return info


def _get_talks_deal_info(max_number):
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
        where pi.p_type = "D0001"
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
                        "title," \
                        "pro_number," \
                        "program_name," \
                        "program_num, " \
                        "purchase_unit_name ," \
                        "agency_orgaization_name," \
                        "hitted_orgaization_name," \
                        "judgor_name," \
                        "purchase_contacts, " \
                        "contact_info, " \
                        "url," \
                        "types) values" \
                        u"(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % \
                        (result_info['p_title'],
                         pro_number,
                         result_info['p_program_name'],
                         result_info['p_program_num'],
                         result_info['p_purchase_unit_name'],
                         result_info['p_agency_orgaization_name'],
                         result_info['p_hitted_orgaization_name'],
                         result_info['p_judgor_name'],
                         result_info['p_purchase_contacts'][-1],
                         result_info['p_contact_info'][-1],
                         url,
                         'D0001')
                # print sql2

                cur.execute(sql2)
                cur.execute('commit')
                # 标题
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
                # # 中标单位(可能有多个)
                # print "中标单位 " + result_info["p_hitted_orgaization_name"]
                # 
                # # 评标委员会成员
                # print "评标委员会成员 " + result_info["p_judgor_name"]
                # 
                # # 采购项目联系人
                # print "采购项目联系人 " + result_info["p_purchase_contacts"][-1]
                # 
                # # 联系方式
                # print "联系方式 " + result_info["p_contact_info"][-1]
                # 
                # # url
                # print "url " + url

                print 'render number:' + str(commit_flag) + '/' + str(cur_result)
                # print '\n\n'
            except Exception, e:
                print str(repr(e))
                continue
    # ----------------------------------------------------------------------------------------------#


    # 关闭游标
    cur.close()

    # 提交操作
    conn.commit()

    # 关闭数据库连接
    conn.close()


# 调用测试方法
# _get_talks_deal_info(0)
