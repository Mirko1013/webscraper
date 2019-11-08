#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/8 14:40
# @Author  : mirko
# @FileName: UniqueElementList.py
# @Software: PyCharm

from pyquery import PyQuery as pq
from WebScraper.Utils import get_md5


class UniquenessTypeNotImplementedError(Exception):
    pass


class UniqueElementList(list):

    def __init__(self, uniqueness_type):
        super(UniqueElementList, self).__init__()

        self.uniqueness_type = uniqueness_type
        self.existed_elements = dict()

    def get_uniqueness_id(self, parent_element):
        #针对parent_element的text，生成uniqueness_id，原则上入参为单个html元素
        if self.uniqueness_type == "unique_text":
            pq_object = pq(parent_element)
            text = pq_object.text()
            element_id = get_md5(text)

            return element_id
        #针对parent_element的html和text，生成uniqueness_id
        elif self.uniqueness_type =="unique_html_text":
            pq_object = pq(parent_element)
            html_text = pq_object.eq(0).copy().html()
            element_id = get_md5(html_text)

            return element_id
        #针对parent_element的html，生成uniqueness_id
        elif self.uniqueness_type == "unique_html":
            pq_object = pq(parent_element)
            html = pq_object.copy()

            def _recursive_remove_text(pq_html):
                a = pq_html.contents()
                a.filter(lambda x: True if x.nodeType == 3 else _recursive_remove_text(x)).remove()

            _recursive_remove_text(pq_object)

            print(pq_object.html())
            element_id = get_md5(html)

            return element_id
        #针对parent_element的css_selector，生成uniquness_id
        elif self.uniqueness_type == "unique_css_selector":
            pass
        else:
            raise UniquenessTypeNotImplementedError()



    def push(self, parent_element):
        if self.is_added(parent_element):
            return False
        else:
            element_uniqueness_id = self.get_uniqueness_id(parent_element)
            self.existed_elements[element_uniqueness_id] = True
            self.append(parent_element.copy())
            return True


    def is_added(self, parent_element):
        element_uniquess_id = self.get_uniqueness_id(parent_element)
        return self.existed_elements.get(element_uniquess_id, False)