#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/10/31 9:17 PM
# @Author  : mirko
# @FileName: ClickSelector.py
# @Software: PyCharm

from . import RegisterSelectorType, Selector
from WebScraper.action import ActionFactory
from WebScraper.Utils import setInterval
from pyquery import PyQuery as pq
from WebScraper.UniqueElementList import UniqueElementList

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

    def __int__(self, id, type, css_paths, parent_selectors, multiple, delay, actions, **kwargs):
        super(ClickSelector, self).__init__(id, type, css_paths, parent_selectors)

        self.multiple = multiple
        self.delay = delay
        self.actions = ActionFactory.create_action("ClickAction").from_settings(**actions)


    @classmethod
    def get_features(cls):
        base_features = Selector.get_features()
        base_features.update(cls.features)

        return base_features

    # @classmethod
    # def from_settings(cls, settings):
    #     selector = super(ClickSelector, cls).from_settings(settings)
    #     selector.actions = ActionFactory.gen_actions_chain(selector.actions)

    #   return selector

    def will_return_multiple_records(self):
        return self.multiple and self.can_return_multiple_records

    def will_return_elements(self):
        return self.can_return_elements

    def will_return_new_jobs(self):
        return self.can_create_new_jobs

    def will_return_local_childs(self):
        return self.can_have_local_child_selectors

    def get_click_elements(self, driver, job_url, parentElement):
        click_css_path = self.actions.protocol.get("click_path")
        driver

    def get_specific_data(self, driver, job_url, parentElement):
        found_elements = UniqueElementList("unique_html_text")
        done_click_elements = UniqueElementList(self.actions.protocol.get("click_uniqueness_type"))
        #拿到需要进行点击的元素
        click_elements = self.actions.get_click_elements(driver, job_url)


        initial_elements = self.get_data_elements(driver, job_url, parentElement)
        for element in initial_elements:
            found_elements.push(element)

        if self.actions.protocol.get("discard_initial_elements"):
            found_elements = UniqueElementList("unique_text")

        if len(click_elements) == 0:
            return found_elements

        current_click_element = click_elements[0]
        current_click_element.click()
        next_click_time = time.time() + self.delay

        def action():
            elements_to_click = list()
            for element in click_elements:
                if not done_click_elements.is_added(element):
                    elements_to_click.append(element)

            now = time.time()

            if time < next_click_time:
                return

            data_elements = self.get_data_elements(driver, job_url, parentElement)

            add_some_element = False
            for item in data_elements:
                added = found_elements.push(item)
                if added:
                    add_some_element = True

            if not add_some_element:
                done_click_elements.push(current_click_element)

            if len(click_elements) == 0:
                inter.cancel()
                return found_elements
            else:
                current_click_element = click_elements[0]
                if (self.actions.protocol.get("click_type")):
                    done_click_elements.push(current_click_element)

                current_click_element.click()
                next_click_time = now + self.delay


        inter = setInterval(0.5, action)

        return found_elements