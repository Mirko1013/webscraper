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


@RegisterSelectorType("SelectorClick")
class ClickSelector(Selector):

    can_return_multiple_records = False
    can_have_child_selectors = True
    can_have_local_child_selectors = True
    can_create_new_jobs = True
    can_return_elements = False

    features = {
        "multiple": False,
        "delay": 0,
        "actions": None
    }

    def __int__(self, id, type, css_paths, parent_selectors, multiple, delay, actions, **kwargs):
        super(ClickSelector, self).__init__(id, type, css_paths, parent_selectors)

        self.multiple = multiple
        self.delay = delay
        self.actions = actions


    @classmethod
    def get_features(cls):
        base_features = Selector.get_features()
        base_features.update(cls.features)

        return base_features

    @classmethod
    def from_settings(cls, settings):
        selector = super(ClickSelector, cls).from_settings(settings)
        selector.actions = ActionFactory.gen_actions_chain(selector.actions)

        return selector

    def will_return_multiple_records(self):
        return self.multiple and self.can_return_multiple_records

    def will_return_elements(self):
        return self.can_return_elements

    def will_return_new_jobs(self):
        return self.can_create_new_jobs

    def will_return_local_childs(self):
        return self.can_have_local_child_selectors

    def get_specific_data(self, driver, job_url, element):
        pass