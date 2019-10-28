#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 15:52
# @Author  : mirko
# @FileName: ChromeBrowser.py
# @Software: PyCharm

from selenium import webdriver
from WebScraper.JsUtils import *
from WebScraper.DataExtractor import DataExtractor

from lxml import etree
from lxml.cssselect import CSSSelector

import threading
import logging

logger = logging.getLogger(__name__)

class ChromeBrowser(object):

    _instance_lock = threading.Lock()

    def __init__(self, path, options, **kwargs):
        self.browser = webdriver.Chrome(executable_path=path, chrome_options=options)

    def quit(self):
        self.browser.quit()

    def __new__(cls, *args, **kwargs):
        if not hasattr(ChromeBrowser, "_instance"):
            with ChromeBrowser._instance_lock:
                if not hasattr(ChromeBrowser, "_instance"):
                    ChromeBrowser._instance = object.__new__(cls)
        return ChromeBrowser._instance


    def loadUrl(self, url):
        logger.info("Start to load url: {0}".format(url))
        self.browser.execute_script(WINDOW_OPEN.format(url, '_self'))

    def getResponse(self, url, fail=False):

        pass


    def fetchData(self, url, sitemap, parentSelectorId):

        self.loadUrl(url=url)
        #对当前请求进行封装
        response = etree.HTML(self.browser.page_source)


        #print(etree.tostring(response))
        #response = etree.parse(self.browser.page_source, etree.HTMLParser())

        dataExtractor = DataExtractor(self, sitemap, parentSelectorId, response)
        results = dataExtractor.getData()
