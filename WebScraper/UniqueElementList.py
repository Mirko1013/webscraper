#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/8 14:40
# @Author  : mirko
# @FileName: UniqueElementList.py
# @Software: PyCharm

from pyquery import PyQuery as pq
from WebScraper.Utils import get_md5
from lxml.etree import _ElementUnicodeResult

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

            element_html = pq("<div class='-scraper-element-wrapper'></div>").append(pq_object.eq(0).clone()).html()

            element_id = get_md5(element_html)

            return element_id
        #针对parent_element的html，生成uniqueness_id
        elif self.uniqueness_type == "unique_html":
            pq_object = pq(parent_element)

            #去除掉父节点下的所有文本？？？
            if pq_object[0].text:
                pq_object[0].text = None
            if pq_object[0].tail:
                pq_object[0].tail = None

            def _recursive_del_text(pq_object):
                element_node_lists = pq_object.contents().filter(lambda i, this: not isinstance(this, _ElementUnicodeResult))
                #TODO 无奈之举，没有了解tail和text的具体构造方式，粗暴赋空值实现去除所有text node的目的，可能会有bug
                for node in element_node_lists:
                    if node.tail:
                        node.tail = None
                    if node.text:
                        node.text = None

                    _recursive_del_text(pq(node))

                return element_node_lists

            _recursive_del_text(pq_object)
            element_html = pq("<div class='-scraper-element-wrapper'></div>").append(pq_object).html()
            element_id = get_md5(element_html)

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
            self.append(parent_element)
            return True


    def is_added(self, parent_element):
        element_uniquess_id = self.get_uniqueness_id(parent_element)
        return self.existed_elements.get(element_uniquess_id, False)