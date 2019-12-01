#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 14:41
# @Author  : mirko
# @FileName: AtomAction.py
# @Software: PyCharm

from . import RegisterActionType, Action, ActionFactory

from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException
from WebScraper.JsUtils import WINDOW_OPEN
from WebScraper.action.CustomConditions import *
from WebScraper.JsUtils import TRIGGER_ELEMENT_CLICK, GET_ITEM_CSS_PATH, SCROLL_TO_BOTTOM

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

    def do(self, browser, *args, **kwargs):
        driver = browser.driver
        url = self.protocol.get("url", None)
        in_new_tab = self.protocol.get("in_new_tab", False)

        try:
            logger.info("OpenAction start to load url -> {}, with open type -> {}".format(url, in_new_tab))
            cur_handle_num = len(driver.window_handles)

            #首先看一下driver的当前url，判断chrome browser是否刚刚完成初始化，此时无论任何url都应在当前tab中打开
            driver_current_url = driver.current_url
            if driver_current_url == "data:,":
                driver.execute_script(WINDOW_OPEN.format(url, '_self'))
                assert len(driver.window_handles) == 1
                browser.update_urm_handle(driver.current_url, driver.current_window_handle)
                return

            if in_new_tab:
                driver.execute_script(WINDOW_OPEN.format(url, '_blank'))
                assert len(driver.window_handles) - cur_handle_num == 1

            else:
                driver.execute_script(WINDOW_OPEN.format(url, '_self'))
                assert len(driver.window_handles) - cur_handle_num == 0

            #更新browser中urm的映射关系
            browser.update_urm_handle(url, driver.window_handles[-1])
            #强制driver切换至当前handle
            driver.switch_to_window(driver.window_handles[-1])

        except TimeoutError as e:
            logger.info("Selenium failed to open the url, caused by:{}".format(e))

            #网络状况不允许在默认60s完成基本html content的加载，直接停止Job执行，关闭driver
            browser.quit()

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

    def do(self, browser, url, *args, **kwargs):
        driver = browser.driver

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
    def from_settings(cls, condition, timeout):
        return cls({"condition": condition, "timeout": timeout})



@RegisterActionType("ClickAction")
class ClickAction(Action):
    """
        协议如下:{"click_path":"div.a"}
    """
    def __init__(self, protocol):
        super(ClickAction, self).__init__(protocol=protocol)

    def pre_check(self, protocol):
        pass


    def get_click_elements(self, driver, url, *args, **kwargs):
        """
        传入浏览器driver，根据协议中的click_path字段，返回全部可点击元素的css_path（唯一）
        :param driver:
        :param url:
        :param args:
        :param kwargs:
        :return:
        """
        result_css_path = list()

        click_path = self.protocol.get("click_path")
        click_elements = driver.find_elements(By.CSS_SELECTOR, click_path)

        for single_click_element in click_elements:
            cur_path = driver.execute_script(GET_ITEM_CSS_PATH, single_click_element)
            result_css_path.append(cur_path)


        if not hasattr(self, "waiting_elements"):
            self.__setattr__("waiting_elements", result_css_path)

        #driver.execute_script(LISTEN_ELEMENT_STATE)

        #return result_css_path
        #return click_elements
    def do(self, browser, url, *args, **kwargs):
        driver = browser.driver

        if not hasattr(self, "waiting_elements"):
            raise AttributeError

        #拿到浏览器已打开的tab数量
        orgin_handles = len(driver.window_handles)

        try:
            #等待click event进入监听状态
            # wait_click = ActionFactory.create_action("WaitAction").from_settings(condition="page_loaded([\"complete\"])", timeout=30)
            # wait_click.do(browser, None)

            current_click_element = self.waiting_elements.pop(0)

            driver.execute_async_script(TRIGGER_ELEMENT_CLICK, current_click_element)

            #click产生了新页面，不允许
            assert len(driver.window_handles) == orgin_handles

            # # 等待页面加载完成
            # wait_click = ActionFactory.create_action("WaitAction").from_settings(condition="page_loaded([\"complete\"])", timeout=30)
            # wait_click.do(browser, None)
            #等待ajax返回

            # wait_ajax = ActionFactory.create_action("WaitAction").from_settings(condition="ajax_loaded_complete(\"jQuery\")", timeout=30)
            # wait_ajax.do(browser, None)

            # wait_ajax = ActionFactory.create_action("WaitAction").from_settings(
            #     None, timeout=5)
            # wait_ajax.do(browser, None)

        except Exception:
            import traceback
            traceback.print_exc()

    @classmethod
    def from_settings(cls, click_path, click_uniqueness_type, click_type, discard_initial_elements):
        return cls({"click_path": click_path, "click_uniqueness_type": click_uniqueness_type, "click_type": click_type, "discard_initial_elements": discard_initial_elements})


@RegisterActionType("ScrollAction")
class ScrollAction(Action):
    """
        协议如下:{"scroll_type":"N/integer"}
    """
    def __init__(self, protocol):
        super(ScrollAction, self).__init__(protocol=protocol)

    def pre_check(self, protocol):
        pass

    def do(self, browser, url,  **kwargs):
        driver = browser.driver

        try:

            result = driver.execute_async_script(SCROLL_TO_BOTTOM)
            print(result)
        except Exception:
            import traceback
            traceback.print_exc()


    @classmethod
    def from_settings(cls, scroll_type):
        return cls({"scroll_type": scroll_type})


@RegisterActionType("CloseAction")
class CloseAction(Action):

    def __init__(self, protocol):
        super(CloseAction, self).__init__(protocol=protocol)

    def pre_check(self, protocol):
        pass

    def do(self, browser, url, **kwargs):
        driver = browser.driver
        data_handle = browser.get_urm_handle(url)
        driver.switch_to_window(data_handle)
        driver.close()

    @classmethod
    def from_settings(cls, dummy):
        return cls({"dummy": dummy})

