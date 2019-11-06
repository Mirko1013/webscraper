#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 10:44
# @Author  : mirko
# @FileName: AttributeSelector.py
# @Software: PyCharm

from . import Selector, RegisterSelectorType
from pyquery import PyQuery as pq

@RegisterSelectorType("SelectorAttribute")
class AttributeSelector(Selector):

    can_return_multiple_records = True
    can_have_child_selectors = True
    can_have_local_child_selectors = False
    can_create_new_jobs = True
    can_return_elements = False

    features = {
        "multiple": False,
        "delay": 0,
        "create_new_jobs": False,
        "extract_attribute": ""
    }


    def __init__(self, id, type, css_paths, parent_selectors, multiple, delay, create_new_jobs, extract_attribute, **kwargs):
        super(AttributeSelector, self).__init__(id, type, css_paths, parent_selectors)
        self.multiple = multiple
        self.delay = delay
        self.create_new_jobs = create_new_jobs
        self.extract_attribute = extract_attribute
        #TODO 在这里可能还需要指定新Job Url等的生成方式

    @classmethod
    def get_features(cls):
        base_features = Selector.get_features()
        base_features.update(cls.features)

        return base_features

    def will_return_multiple_records(self):
        return self.can_return_multiple_records and self.multiple

    def will_return_local_childs(self):
        return self.can_have_local_child_selectors

    def will_return_new_jobs(self):
        return self.can_create_new_jobs and self.create_new_jobs

    def will_return_elements(self):
        return self.can_return_elements


    def get_specific_data(self, parentElement):
        resultData = list()
        elements = self.get_data_elements(parentElement)

        if not self.multiple and len(elements) == 0:
            data = dict()
            data[self.id] = None
            resultData.append(data)

            return resultData

        for element in elements:
            pq_object = pq(element)
            data = dict()

            #对于可以产生新Job的元素，经由element中指定attribute抽取出新url
            if self.will_return_new_jobs():
                data[self.id] = pq_object.attr(self.extract_attribute)
                data["_followSelectorId"] = self.id
                data[str(self.id) + "-href"] = pq_object.attr(self.extract_attribute)
                data["_follow"] = pq_object.attr(self.extract_attribute)

                resultData.append(data)

            #对于仅需抽取的元素，直接抽取，用属性值作为结果
            else:
                data[self.id] = pq_object.attr(self.extract_attribute)
                resultData.append(data)

        return resultData