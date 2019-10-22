#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/22 9:20 PM
# @Author  : mirko
# @FileName: LinkSelector.py
# @Software: PyCharm

from . import RegisterSelectorType, Selector


@RegisterSelectorType("SelectorLink")
class LinkSelector(Selector):

    can_return_multiple_records = True
    can_have_child_selectors = True
    can_have_local_child_selectors = False
    can_create_new_jobs = True
    can_return_elements = False

    features = {
        'multiple': False,
        'delay': 0
    }

    def __init__(self, id, type, css_paths, parent_selectors, multiple, delay, **kwargs):
        super(LinkSelector, self).__init__(id, type, css_paths, parent_selectors)
        self.multiple = multiple
        self.delay = delay

    @classmethod
    def get_features(cls):
        base_features = Selector.get_features()
        base_features.update(cls.features)
        return base_features

    def will_return_multiple_records(self):
        return self.can_return_multiple_records and self.multiple
