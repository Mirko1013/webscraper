#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 16:13
# @Author  : mirko
# @FileName: ChromeBrowser.py
# @Software: PyCharm

from WebScraper.ChromeBrowser import ChromeBrowser
from selenium.webdriver.common.by import By
from copy import deepcopy

if __name__ == '__main__':
    path = r"D:\PycharmProjects\baijia\WebScraper\chromedriver\chromedriver.exe"
    #path = r"/Users/mirko/PycharmProjects/baijia/WebScraper/chromedirver/chromedriver"
    a = ChromeBrowser(path, {})
    url = "https://author.baidu.com/home/1625877293629981"
    #
    a.browser.get(url)
    article_card = a.browser.find_element_by_css_selector("div.s-card")
    print(article_card)
    current_handle = a.browser.current_window_handle
    article_card.target = "_new"
    article_card.click()





    import time
    time.sleep(3)

    a.browser.switch_to_window(current_handle)
    a.quit()
