#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/13 14:09
# @Author  : mirko
# @FileName: CustomConditions.py
# @Software: PyCharm

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from WebScraper.JsUtils import DOCUMENT_STATUS

import re

class page_loaded(object):
    """根据传入的状态list，判断当前页面是否完成了加载"""
    def __init__(self, re_exp):
        """
        根据传入的re_exp进行判断，如果为None或空字符串，则给状态数组赋默认值["complete", "loaded", "interactive"]
        :param re_exp:
        """
        if not re_exp or re_exp =="":
            self.re_exp = ["complete", "interactive"]
        else:
            self.re_exp = re_exp

    def __call__(self, driver, *args, **kwargs):
        status = driver.execute_script(DOCUMENT_STATUS)
        print(status, type(status))

        return True if status in self.re_exp else False
