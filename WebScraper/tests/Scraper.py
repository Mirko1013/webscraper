#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/10/22 16:10
# @Author  : mirko
# @FileName: Scraper.py
# @Software: PyCharm

from WebScraper.Sitemap import Sitemap
from WebScraper.TQueue import TaskQueue
from WebScraper.ChromeBrowser import ChromeBrowser
from WebScraper.Scraper import Scraper


import json

def main():
    path= r"D:\PycharmProjects\baijia\WebScraper\chromedriver\chromedriver.exe"
    #path = r"/Users/mirko/PycharmProjects/baijia/WebScraper/chromedirver/chromedriver"

    with open("../../test_baijia.json", encoding="utf-8") as f:
       json_sitemap = json.load(f)
    sitemap = Sitemap(json_sitemap.get("_id"), json_sitemap.get("startUrl"), json_sitemap.get("selectors"))
    queue = TaskQueue()
    browser = ChromeBrowser(path, list())

    scraper = Scraper(queue, sitemap, browser)
    # a=sitemap.getSelectorById("_root")
    # b=sitemap.getSelectorById("items")
    # c=sitemap.getSelectorById("link")
    # d=sitemap.getSelectorById("title")
    # e=sitemap.getSelectorById("reviews")
    # f=sitemap.getSelectorById("intro")
    # print("lalal")
    data = scraper.run()
    print("圆满完成任务！")

if __name__ == '__main__':
    main()

