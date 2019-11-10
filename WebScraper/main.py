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


if __name__ == '__main__':
    #测试setInterval的多线程实现
    #
    # inter = setInterval(0.5, action, "你可长点心把 ")
    # print('just after setInterval -> time : {:.1f}s'.format(time.time() - start_time))
    #
    # t = threading.Timer(5, inter.cancel)
    # t.start()
    div_str = """<div class="container">
  Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed 
  do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
  <br /><br />
  Ut enim ad minim veniam, quis nostrud exercitation ullamco 
  laboris nisi ut aliquip ex ea commodo consequat.<div>lalalalalaal</div>
  <br /><br />
  Duis aute irure dolor in reprehenderit in voluptate velit 
  esse cillum dolore eu fugiat nulla pariatur.</div>"""

    uq = UniqueElementList("unique_html")

    uq.get_uniqueness_id(pq(div_str))
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