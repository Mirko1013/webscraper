#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/16 11:09 AM
# @Author  : mirko
# @FileName: main.py
# @Software: PyCharm

from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.common.by import By
from WebScraper.Utils import setInterval
import threading
import time
from WebScraper.Utils import get_md5
start_time = time.time()
from WebScraper.UniqueElementList import UniqueElementList
from pyquery import PyQuery as pq
def action(echo):
    print("{}action ! -> time: {:.1f}s".format(echo, time.time() - start_time))
from WebScraper.processor.RegexProcessor import RegexProcessor

import requests
from bs4 import BeautifulSoup,NavigableString, Tag

import xlrd, xlwt

def main():
    work_book = xlrd.open_workbook(r"C:\Users\Mirko\Downloads\QKL.xlsx")
    #拿表
    table = work_book.sheets()[0]
    #拿URL信息
    info_list = table.col_values(-3)

    # for i, item in enumerate(info_list):

    def process_url(src):
        import re
        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        regex = re.compile(pattern)
        # print(item)
        res = regex.findall(src)
        return res

    def process_name(src):
        import re
        pattern = r'(CVE-\d{4}-\d+)'
        regex = re.compile(pattern)
        # print(item)
        res = regex.search(src)
        if res:
            return res.group()

    res = []
    for i in range(0, table.nrows):
        row_list = table.row_values(i)

        #for item in row_list:
        if row_list[3] and row_list[5] and row_list[-3]:
            #list记录原文件信息
            #col1：漏洞名称
            #col2：应用分类
            #col3：修复建议
            #col4：序号
            #col5：危险程度
            tmp_record = (process_name(row_list[3]), row_list[5], process_url(row_list[-3]), row_list[1], row_list[2])
            res.append(list(tmp_record))

        # #for item in row_list:
        # if row_list[4] and row_list[6] and row_list[-1]:
        #     #list记录原文件信息
        #     #col1：漏洞名称
        #     #col2：应用分类
        #     #col3：修复建议
        #     #col4：序号
        #     #col5：危险程度
        #     tmp_record = (process_name(row_list[4]), row_list[6], process_url(row_list[-1]), row_list[2], row_list[3])
        #     res.append(list(tmp_record))

    #计数器
    counter = 0
    #对预处理后的结果进行遍历，这一步中去对应url提取修复建议


    info =[]
    advlist = []


    for item in res:

        if item[1] == "MySQL":
            counter += 1

            tinfo = []
            advice = []

            print("当前正在处理:第{0}条......".format(counter))

            #修复建议中的链接不止一条时，不处理
            #if (len(item[2]) < 2):
            advice = crawl(item[2][0], item[0])

            tinfo.append(item[4])
            tinfo.append(item[3])
            tinfo.append(item[0])
            tinfo.append(item[1])
            tinfo.append("\n".join([x for x in item[2]]))


            # print("漏洞编号:"+item[0]+",漏洞类型:"+item[1]+",漏洞修复链接:"+"\n".join([x for x in item[2]])+"\n")
            # print("修复建议.{0}\n".format(advice))
            print("-------------------------------------------------------")

            advlist.append(advice)
            info.append(tinfo)

    print("统计MySQL的漏洞数中为:{0}".format(counter))

    write_xls(info, advlist)




def crawl(url, text):

    resList = []

    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")

    res = soup.find_all(text=text)

    #在找到的标签中继续搜
    for tag in res:
        #root_tag = tag.parent.parent
        root_tag = tag.find_parents("tr")

        root_tag = root_tag[0]
        tlist =[]

        for child in root_tag.children:
            if isinstance(child, NavigableString):
                continue
            if isinstance(child, Tag):
                if not child.text.isspace():
                    tlist.append(child.text.strip().replace("\n", "").replace("\r", "").replace("\t", ""))
        resList.append(tlist)

    return resList


def write_xls(olist, alist):

    assert len(olist) == len(alist)

    workbook = xlwt.Workbook(encoding="utf-8")
    xlsheet = workbook.add_sheet("漏洞梳理表", cell_overwrite_ok=True)

    table_head=["危险程度", "原文件序号", "漏洞编号", "漏洞类型", "修复链接"]

    table_head2 = ["CVE#", "产品", "组件", "协议", "有无身份验证的远程利用", "Base Score", "Attack Vector",\
                 "Attack Complex", "Privs Req\'d", "User Interact", "Scope", "Confidentiality", "Integrity", "Availability",\
                   "受影响的支持版本"]

    style = xlwt.XFStyle()
    pattern = xlwt.Pattern()

    pattern.pattern = pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 0x28
    style.pattern = pattern

    font = xlwt.Font()  # 为样式创建字体
    font.name = 'Times New Roman'
    font.bold = True  # 黑体

    #font.underline = True  # 下划线
    #font.italic = True  # 斜体字
    style.font = font  # 设定样式

    #维护全局index
    index = 0
    headlen = len(table_head)
    head2len = len(table_head2)

    for row, oitem in enumerate(olist):
        for i in range(headlen):
            xlsheet.write(index, i, table_head[i], style)
        index += 1

        for i in range(headlen):
            xlsheet.write(index, i, oitem[i])

        index += 1

        for i in range(head2len):
            xlsheet.write(index, i, table_head2[i], style)

        index += 1

        for item in alist[row]:

            for i in range(head2len):
                xlsheet.write(index, i, item[i])
            index += 1

        index += 2
    # table_head2= ["CVE#", "Product", "Component", "Protocol", "Remote Exploit without Auth.?", "Base Score", "Attack Vector", \
    #              "Attack Complex", "Privs Req\'d", "User Interact", "Scope", "Confidentiality", "Integrity", "Availability", \
    #              "Supported Versions Affected", "Notes"]




    workbook.save("reslut.xls")

if __name__ == '__main__':
    main()
    # import re
    # str = "发布时间：12-06"
    #
    # pattern = re.compile("\\d{1,2}-\\d{1,2}")
    # lst = pattern.findall(str)
    # print(lst)
    # #测试setInterval的多线程实现
    #
    # inter = setInterval(0.5, action, "你可长点心把 ")
    # print('just after setInterval -> time : {:.1f}s'.format(time.time() - start_time))
    #
    # t = threading.Timer(5, inter.cancel)
    # t.start()
  #   div_str = """<div class="container">
  # Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed
  # do eiusmod tempor incidi<div class='test'>abc<div>a<div>abcd</div>bcd</div>d</div>dunt ut labore et dolore magna aliqua.
  # <br /><br />
  # Ut enim ad minim veniam, quis nostrud exercitation ullamco
  # laboris nisi ut aliquip ex ea commodo consequat.<div>lalalalalaal<div>abcd</div></div>
  # <br /><br />
  # Duis aute irure dolor in reprehenderit in voluptate velit
  # esse cillum dolore eu fugiat nulla pariatur.</div>"""
  #
  #   uq = UniqueElementList("unique_text")
  #
  #   uq.get_uniqueness_id(pq(div_str))
    # os.environ["PATH"] += ":" + os.path.abspath("./webdriver")
    #
    # options = Options()
    # driver = webdriver.Chrome(chrome_options=options)
    # driver.get("http://www.baidu.com")
    # driver.quit()



    # with open("WebScraper.json", encoding="utf-8") as f:
    #     sitemap_json = json.load(f)
    #
    # sitemap = Sitemap(sitemap_json.get("_id"), sitemap_json.get("startUrl"), sitemap_json.get("selectors"))
    # print("end")
    #
    # restr = r"(,|\".*?\"|\'.*?\'|\(.*?\))"
    # str = "div.jumbotron h1"
    # print(str.split(restr))
    #
    # d = pq("<html>a</html>")
    # print(type(d))
    #
    # dd = d("html")[0]
    # print(type(pq(dd)))
    # a = dict()
    # a["1"] = 1
    # a["2"] = 2
    # print(a)
    # b = list()
    # b.append(a)
    # print(b)

#     import re
#
#     regex = re.compile(r"(https?://)?([a-z0-9\-.]+\.[a-z0-9\-]+(:\d+)?|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?)?(/[^?]*/|/)?([^?]*)?(\?.*)?")
#    # url = "http://www.runoob.com:80/html/html-tutorial.html?a=2"
# #url = "/"
#     url = "?a=1"
#
#     result = regex.match(url)
#     a = result.groups()
#     print(result.group(1))

    # a = list()
#     # b = [1,2,3,4,5]
#     # c = list(b)
#     # print(b)

    #
    #
    # a = "presence_of_element_located((By.TAG_NAME, \"title\"))"
    #
    # b = eval(a)
    # print(callable(1))
    # print("done")