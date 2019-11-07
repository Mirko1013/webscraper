#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 14:41
# @Author  : mirko
# @FileName: AtomAction.py
# @Software: PyCharm

from . import RegisterActionType, Action

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException
from WebScraper.JsUtils import WINDOW_OPEN

import logging

logger = logging.getLogger(__name__)

@RegisterActionType("OpenAction")
class OpenAction(Action):
    """
        协议如下:{"url": "http://www.example.com", "in_new_tab": True or False}
    """
    def __init__(self, protocol):
        super(OpenAction, self).__init__(protocol=protocol)

    def pre_check(self, protocol):
        pass

    def do(self, driver, *args, **kwargs):
        url = self.protocol.get("url", None)
        in_new_tab = self.protocol.get("in_new_tab", False)

        try:
            logger.info("OpenAction start to load url -> {}, with open type -> {}".format(url, in_new_tab))
            if in_new_tab:
                driver.execute_script(WINDOW_OPEN.format(url, '_blank'))
            else:
                driver.execute_script(WINDOW_OPEN.format(url, '_self'))

            driver.switch_to_window(driver.window_handles[-1])
            print(driver.current_window_handle)
        except Exception:
            #TODO 捕获打开异常
            pass


    @classmethod
    def from_settings(cls, url, in_new_tab):
        return cls({"url": url, "in_new_tab": in_new_tab})

@RegisterActionType("WaitAction")
class WaitAction(Action):
    """
        协议如下:{"condition":"", "timeout": 5}
    """
    #默认最长等待时间为60s
    MAX_WAIT_TIME = 60

    def __init__(self, protocol):
        super(WaitAction, self).__init__(protocol=protocol)


    def pre_check(self, protocol):
        condition = protocol.get("condition", None)
        timeout = protocol.get("timeout", 0)

        if isinstance(condition, (str, bytes)):
            if condition: condition = eval(condition)
        elif not isinstance(condition, int) or callable(condition):
            #TODO 传入异常类型的判断条件，此处应该抛出自定义异常
            pass
        protocol["condition"] = condition
        protocol["timeout"] = self.MAX_WAIT_TIME if timeout > self.MAX_WAIT_TIME else timeout

    def do(self, driver, url, *args, **kwargs):

        condition = self.protocol.get("condition")
        timeout = self.protocol.get("timeout")

        if callable(condition):
            WebDriverWait(driver, timeout).until(condition)
        elif isinstance(condition, int):
            #TODO 此处未定义wait condition为数字时driver应该干什么，后期进行补充
            pass
            #WebDriverWait(driver, timeout).until(lambda _:)
        else:
            #应对于condition抽取为空的情况，此处等待timeout后直接执行，
            WebDriverWait(driver, timeout).until(lambda _: False)

    @classmethod
    def from_settings(cls, conditions, timeout):
        return cls({"conditions": conditions, "timeout": timeout})



@RegisterActionType("ClickAction")
class ClickAction(Action):
    """
        协议如下:{"click_path":"div.a"}
    """
    def __init__(self, protocol):
        super(ClickAction, self).__init__(protocol=protocol)

    def pre_check(self, protocol):
        if not self.protocol.get("click_path", None):
            raise NoSuchElementException


    def do(self, driver, url, *args, **kwargs):
        click_path = self.protocol.get("click_path")

        exist = True

        try:
            click_element = driver.find_element(By.CSS_SELECTOR, click_path)
        except NoSuchElementException:
            #固定等待1s
            wait = WaitAction.from_settings(None, 1)
            wait.do(driver, url)
            try:
                click_element = driver.find_element(By.CSS_SELECTOR, click_path)
            except NoSuchElementException:
                exist = False

        #拿到浏览器已打开的tab数量
        orgin_handles = len(driver.windows_handles)

        try:
            if exist:
                click_element.click()
        except ElementNotVisibleException:
            #TODO 此处应该处理元素不可见的情况，或滚动，或等待
            click_element.click()

        #页面元素完成点击，进行下一步
        if len(driver.windows_handles) > orgin_handles:
            driver.switch_to_window(driver.windows_handles[-1])


    @classmethod
    def from_settings(cls, click_paths):
        return cls({"click_path": click_paths})

@RegisterActionType("CloseAction")
class CloseAction(Action):

    def __init__(self):
        pass

    def pre_check(self, protocol):
        pass

    def do(self, **kwargs):
        pass


