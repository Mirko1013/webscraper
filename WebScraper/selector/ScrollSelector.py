#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/15 15:33
# @Author  : mirko
# @FileName: ScrollSelector.py
# @Software: PyCharm

from . import RegisterSelectorType, Selector
from WebScraper.Utils import setInterval
from selenium.webdriver.common.by import By
from WebScraper.action import ActionFactory

import time

@RegisterSelectorType("SelectorScroll")
class ScrollSelector(Selector):

    can_return_multiple_records = True
    can_have_child_selectors = True
    can_have_local_child_selectors = True
    can_create_new_jobs = False
    can_return_elements = True

    features = {
        "multiple": False,
        "delay": 0,
        "scroll_type": "N"
    }


    def __init__(self, id, type, css_paths, parent_selectors, multiple, delay, scroll_type, **kwargs):
        super(ScrollSelector, self).__init__(id, type, css_paths, parent_selectors)

        self.multiple = multiple
        self.delay = 0 if delay == "" else delay
        self.action = ActionFactory.create_action("ScrollAction").from_settings(scroll_type)

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

    def get_specific_data(self, browser, job_url, parentElement):
        driver = browser.driver

        found_elements = self.get_data_elements(driver, job_url, parentElement)
        pre_len = len(found_elements)

        time_step = float(self.delay)
        next_scroll_time = time.time()

        def scroll_func(stop_event, *args, **kwargs):
            nonlocal found_elements
            nonlocal next_scroll_time
            nonlocal time_step
            nonlocal pre_len

            now = time.time()

            if now < next_scroll_time:
                return

            #切换至当前窗口
            data_handle = browser.get_urm_handle(job_url)
            driver.switch_to_window(data_handle)

            #卷动
            scroll_percent = self.action.do(browser, job_url)
            print("ScrollSelector滚动至百分比:{}".format(scroll_percent))
            parent_element = driver.find_element(By.TAG_NAME, "html").get_attribute("outerHTML")
            found_elements = self.get_data_elements(driver, job_url, parent_element)

            cur_len = len(found_elements)

            if cur_len > pre_len or scroll_percent < 100:
                pre_len = cur_len
                next_scroll_time = now + time_step
            else:
                stop_event.set()

        setInterval(1, scroll_func)

        return found_elements
