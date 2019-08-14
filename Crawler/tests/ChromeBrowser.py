#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 16:13
# @Author  : mirko
# @FileName: ChromeBrowser.py
# @Software: PyCharm

from Crawler.sitemap.ChromeBrowser import ChromeBrowser

if __name__ == '__main__':
    path = r"D:\PycharmProjects\baijia\Crawler\chromedirver\chromedriver.exe"
    a = ChromeBrowser(path, None)
    a.browser.get("http://www.baidu.com")
    import time
    time.sleep(5)
    a.quit()
