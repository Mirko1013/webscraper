#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 15:52
# @Author  : mirko
# @FileName: ChromeBrowser.py
# @Software: PyCharm

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from WebScraper.JsUtils import *
from WebScraper.DataExtractor import DataExtractor
from WebScraper.action import ActionFactory
from WebScraper.action.AtomAction import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from lxml import etree
from lxml.cssselect import CSSSelector
from pyquery import PyQuery as pq
from WebScraper.Utils import get_md5

import threading
import logging

logger = logging.getLogger(__name__)

class ChromeBrowser(object):

    #单例锁
    _instance_lock = threading.Lock()

    def __init__(self, path, options, desired_capabilities, **kwargs):
        self.options = self.chrome_options(options, desired_capabilities)
        self.rainbow= dict()
        self.driver = webdriver.Chrome(executable_path=path, chrome_options=self.options)

        #设置页面加载超时，默认60s，用以防止极端情况下，driver陷入无限等待
        self.driver.set_page_load_timeout(60)
        self.driver.set_script_timeout(60)


        assert len(self.driver.window_handles) == 1
        self.update_urm_handle(self.driver.current_url, self.driver.current_window_handle)

    def chrome_options(self, options, desired_capabilities):
        default_options = Options()
        #TODO 此处用户配置和默认配置处理的有问题，后期完善，先凑合
        for option in options:
            default_options.add_argument(option)

        #手机浏览器配置
        # emulation = {
        #     'deviceName': 'iPhone 6 Plus'
        # }
        #
        # default_options.add_experimental_option("mobileEmulation", emulation)

        #default_options.add_argument('--headless')
        default_options.add_argument('--disable-gpu')
        default_options.add_argument('--no-sandbox')
        default_options.add_argument('blink-settings=imageEnabled=false')
        default_options.add_argument('--disable-plugins')


        #desired_capabilities和options的主要区别在于前者自定义，后者封装更为可读
        #desired_capabilities = DesiredCapabilities.CHROME

        for key, value in desired_capabilities.items():
            default_options.capabilities[key] = value

        #开启默认配置，更改当前web driver的pageLoadStrategy为eager
        #Keyword	Page load strategy state	Document readiness state(document.readyState)
        #"none"	            none	                    无对应
        #"eager"	        eager	                "interactive"
        #"normal"	        normal	                  "complete"
        default_options.capabilities["pageLoadStrategy"] = "eager"

        return default_options


    def quit(self):
        self.driver.quit()

    def __new__(cls, *args, **kwargs):
        if not hasattr(ChromeBrowser, "_instance"):
            with ChromeBrowser._instance_lock:
                if not hasattr(ChromeBrowser, "_instance"):
                    ChromeBrowser._instance = object.__new__(cls)
        return ChromeBrowser._instance


    def loadUrl(self, url):
        logger.info("Start to load url: {0}".format(url))
        self.driver.execute_script(WINDOW_OPEN.format(url, '_self'))


    def get_urm_handle(self, url):
        """
        传入url，返回彩虹表中维护对于该url_key的handle
        :param url:
        :return:
        """
        return self.rainbow.get(get_md5(url), None)


    def update_urm_handle(self, url, handle):
        """
        传入url和handle(类型为str)，判断url_key是否在彩虹表中。如在，更新，否则添加
        :param url:
        :param handle:
        :return:
        """
        url_key = get_md5(url)

        if not url_key in self.rainbow.keys():
            self.rainbow[url_key] = handle
        else:
            url_key[url_key] = handle


    def fetchData(self, url, sitemap, parentSelectorId):
        #打开页面
        open_action = ActionFactory.create_action("OpenAction").from_settings(url=url, in_new_tab=True).do(self)

        #等待页面元素加载完成，默认轮询document的readyState，["complete", "interactive"]
        #loading / 正在加载，表示 document 仍在加载。
        #interactive / 可交互，文档已被解析，"正在加载"状态结束，但是诸如图像，样式表和框架之类的子资源仍在加载。
        #complete / 完成，文档和所有子资源已完成加载。表示 load 状态的事件即将被触发。
        page_loaded_action = ActionFactory.create_action("WaitAction").from_settings(condition="page_loaded(None)", timeout=30).do(self, None)
        #wait_click = ActionFactory.create_action("WaitAction").from_settings(condition="page_loaded([\"complete\"])", timeout=10).do(self, None)
        #ajax_loaded_action = ActionFactory.create_action("WaitAction").from_settings(condition="ajax_loaded_complete(\"jQuery\")", timeout=30).do(self, None)

        #解耦合，灵活等待，避开使用driver.page_source属性来获取网页的html元素
        parent_element = self.driver.find_element(By.TAG_NAME, "html").get_attribute("outerHTML")

        #进入数据抽取逻辑
        dataExtractor = DataExtractor(self, url, sitemap, parentSelectorId, parent_element)
        results = dataExtractor.getData()

        return results