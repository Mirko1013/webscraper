#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/10/31 9:17 PM
# @Author  : mirko
# @FileName: ClickSelector.py
# @Software: PyCharm

from . import Selector, RegisterSelectorType
from WebScraper.action import ActionFactory
from WebScraper.Utils import setInterval
from pyquery import PyQuery as pq
from WebScraper.UniqueElementList import UniqueElementList
from WebScraper.JsUtils import GET_ITEM_CSS_PATH, TRIGGER_ELEMENT_CLICK


from selenium.webdriver.common.by import By

import time

@RegisterSelectorType("SelectorClick")
class ClickSelector(Selector):

    can_return_multiple_records = True
    can_have_child_selectors = True
    can_have_local_child_selectors = True
    can_create_new_jobs = False
    can_return_elements = True

    features = {
        "multiple": False,
        "delay": 0,
        "actions": None
    }

    def __init__(self, id, type, css_paths, parent_selectors, multiple, delay, actions, **kwargs):
        super(ClickSelector, self).__init__(id, type, css_paths, parent_selectors)

        self.multiple = multiple
        self.delay = 0 if delay == "" else delay
        self.actions = ActionFactory.create_action("ClickAction").from_settings(**actions)


    @classmethod
    def get_features(cls):
        base_features = Selector.get_features()
        base_features.update(cls.features)
        return base_features


    def will_return_multiple_records(self):
        return self.multiple and self.can_return_multiple_records

    def will_return_elements(self):
        return self.can_return_elements

    def will_return_new_jobs(self):
        return self.can_create_new_jobs

    def will_return_local_childs(self):
        return self.can_have_local_child_selectors

    # def get_click_elements(self, driver, job_url, parentElement):
    #     click_css_path = self.actions.protocol.get("click_path")
    #
    # def get_item_css_path(self, driver, element):
    #     return driver.execute_script(GET_ITEM_CSS_PATH, element)
    #
    #
    # def trigger_element_click(self):
    #     pass
    #
    #

    def get_specific_data(self, browser, job_url, parentElement):
        driver = browser.driver

        found_elements = UniqueElementList("unique_html_text")

        #更新actions实例，拿到需要进行点击的元素路径，以list形式存放waiting_elements（唯一的css路径）
        self.actions.get_click_elements(driver, job_url)

        initial_elements = self.get_data_elements(driver, job_url, parentElement)

        for element in initial_elements:
            found_elements.push(element)

        if self.actions.protocol.get("discard_initial_elements"):
            found_elements = UniqueElementList("unique_text")

        if len(self.actions.waiting_elements) == 0:
            return found_elements

        time_step = float(self.delay)

        next_click_time = time.time()

        def click_func(stop_event, *args, **kwargs):
            nonlocal time_step
            nonlocal next_click_time

            now = time.time()

            if now < next_click_time:
                return

            # 切换至当前窗口
            data_handle = browser.get_urm_handle(job_url)
            driver.switch_to_window(data_handle)

            # 点击
            self.actions.do(browser, job_url)
            print("==========================================done click=====================================")

            parent_element = driver.find_element(By.TAG_NAME, "html").get_attribute("outerHTML")
            data_elements = self.get_data_elements(driver, job_url, parent_element)

            add_some_element = False
            for item in data_elements:
                added = found_elements.push(item)

                a = pq(item)
                print("------>{0}<------\n".format(a.text()))

                if added:
                    add_some_element = True

            print("新增元素:{0}".format(add_some_element))

            if len(self.actions.waiting_elements) == 0:
                stop_event.set()
            else:
                next_click_time = now + time_step

        inter = setInterval(1, click_func)

        return found_elements



    # def get_specific_data(self, browser, job_url, parentElement):
    #     driver = browser.driver
    #
    #     found_elements = UniqueElementList("unique_html_text")
    #     done_click_elements = UniqueElementList(self.actions.protocol.get("click_uniqueness_type"))
    #
    #
    #     #更新actions实例，拿到需要进行点击的元素路径，以list形式存放waiting_elements（唯一的css路径）
    #     self.actions.get_click_elements(driver, job_url)
    #
    #     initial_elements = self.get_data_elements(driver, job_url, parentElement)
    #
    #     for element in initial_elements:
    #         found_elements.push(element)
    #
    #     if self.actions.protocol.get("discard_initial_elements"):
    #         found_elements = UniqueElementList("unique_text")
    #
    #     if len(self.actions.waiting_elements) == 0:
    #         return found_elements
    #
    #     time_step = float(self.delay)
    #     next_click_time = time.time()
    #
    #     def click_func(stop_event, *args, **kwargs):
    #         nonlocal  time_step
    #         nonlocal next_click_time
    #
    #         now = time.time()
    #
    #         if now < next_click_time:
    #             return
    #
    #         #切换至当前窗口
    #         data_handle = browser.get_urm_handle(job_url)
    #         driver.switch_to_window(data_handle)
    #
    #         #点击
    #         self.actions.do(browser, job_url)
    #
    #         parent_element = self.driver.find_element(By.TAG_NAME, "html").get_attribute("outerHTML")
    #         data_elements = self.get_data_elements(driver, job_url, parent_element)
    #
    #         add_some_element = False
    #         for item in data_elements:
    #             added = found_elements.push(item)
    #             if added:
    #                 add_some_element = True
    #
    #
    #         if len(self.actions.waiting_elements) == 0:
    #             stop_event.set()
    #             #return found_elements
    #         else:
    #             #self.actions.do(browser, job_url)
    #             next_click_time = now + time_step
    #
    #
    #
    #     inter = setInterval(1, click_func)
    #
    #     return found_elements
    #
    #
    #     def action(stop_event, *args, **kwargs):
    #         nonlocal next_click_time
    #         # nonlocal current_click_element
    #         nonlocal time_step
    #
    #         #elements_to_click = list()
    #
    #         #切换至当前窗口
    #         data_handle = browser.get_urm_handle(job_url)
    #         driver.switch_to_window(data_handle)
    #
    #         #print(done_click_elements)
    #         # for element in click_elements:
    #         #     html_element = element.get_attribute("outerHTML")
    #         #     if not done_click_elements.is_added(html_element):
    #         #         elements_to_click.append(element)
    #
    #         now = time.time()
    #         #print(elements_to_click)
    #         if now < next_click_time:
    #             return
    #
    #         data_elements = self.get_data_elements(driver, job_url, driver.page_source)
    #
    #         add_some_element = False
    #         for item in data_elements:
    #             added = found_elements.push(item)
    #             if added:
    #                 add_some_element = True
    #
    #         # if not add_some_element:
    #         #     done_click_elements.push(current_click_element.get_attribute("outerHTML"))
    #
    #         if len(self.actions.waiting_elements) == 0:
    #             #inter.cancel()
    #             stop_event.set()
    #             return found_elements
    #         else:
    #             # current_click_element = elements_to_click[0]
    #             # #print(current_click_element.get_attribute("outerHTML"))
    #             # if (self.actions.protocol.get("click_type") == "click_once"):
    #             #     done_click_elements.push(current_click_element.get_attribute("outerHTML"))
    #             #
    #             # current_click_element.click()
    #
    #             self.actions.do(browser, job_url)
    #             next_click_time = time.time() + time_step
    #
    #
    #     inter = setInterval(1, action)
    #
    #     return found_elements