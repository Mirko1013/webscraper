#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/13 14:09
# @Author  : mirko
# @FileName: CustomConditions.py
# @Software: PyCharm

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from WebScraper.JsUtils import DOCUMENT_STATUS, JQUERY_AJAX_STATUS
import re

class page_loaded(object):
    """根据传入的状态list，判断当前页面是否完成了加载"""
    def __init__(self, re_exp):
        """
        根据传入的re_exp进行判断，如果为None或空字符串，则给状态数组赋默认值["complete", "interactive"]
        :param re_exp:
        """
        if not re_exp or re_exp =="":
            self.re_exp = ["complete", "interactive"]
        else:
            self.re_exp = re_exp

    def __call__(self, driver, *args, **kwargs):
        status = driver.execute_script(DOCUMENT_STATUS)
        #print("Wait for page load completed, current status is --> {}".format(status))

        return True if status in self.re_exp else False


class ajax_loaded_complete(object):
    """现阶段仅支持用jquery实现的ajax等待"""
    def __init__(self, type):
        """
        传入ajax请求的实现方法，如jQuery、AngularJS等
        :param type:
        """
        #TODO ajax请求类型，后续需要对此进行补充
        self.type = type

    def __call__(self, driver, *args, **kwargs):
        if self.type == "jQuery":
            status = driver.execute_script(JQUERY_AJAX_STATUS)
            #print("Wait for ajax response completed, current status is --> {}".format(status))
            return True if status else False
        else:
            return True