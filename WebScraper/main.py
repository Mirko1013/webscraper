#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/16 11:09 AM
# @Author  : mirko
# @FileName: main.py
# @Software: PyCharm

from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.common.by import By


if __name__ == '__main__':
    #
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