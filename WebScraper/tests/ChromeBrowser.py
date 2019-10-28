#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 16:13
# @Author  : mirko
# @FileName: ChromeBrowser.py
# @Software: PyCharm

from WebScraper.ChromeBrowser import ChromeBrowser

if __name__ == '__main__':
    #path = r"D:\PycharmProjects\baijia\WebScraper\chromedriver\chromedriver.exe"
    path = r"/Users/mirko/PycharmProjects/baijia/WebScraper/chromedirver/chromedriver"
    a = ChromeBrowser(path, None)
    a.fetchData("http://www.baidu.com", None, None)
    import time
    time.sleep(5)
    a.quit()
