#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 9:07 AM
# @Author  : mirko
# @FileName: __init__.py.py
# @Software: PyCharm


from Crawler.sitemap.selector import SelectorFactory, Selector
from Crawler.sitemap.selector import ElementSelector
from Crawler.sitemap.ChromeBrowser import *

class SelectorList(object):

    Array = list()

    def __init__(self, selector_json_str):

        for item in selector_json_str:
            new_selector = SelectorFactory.create_selector(type=item.get("type")).from_settings(**item)

            if not self.have_selector(new_selector):
                self.Array.append(new_selector)


    def have_selector(self, current_selector):

        if not isinstance(current_selector, Selector):
            raise TypeError("Accept wrong type object, not a kind of selector.")

        for _selector in self.Array:
            if current_selector.__getattribute__("id") == _selector.id:
                return True

        return False


    def get_all_child_selectors(self, parent_selector_id):

        result_selectors_list = list()

        def rescursive_find_selectors(parent_selector_id, result_selectors_list):

            pass

root_config = {
      "id": "_root",
      "type": "SelectorElement",
      "parentSelectors": [
        "_root"
      ],
      "selector": "div.thumbnail",
      "multiple": True,
      "delay": 0
    }



class SelectorTree(object):

    created_selectors_id = list()

    def __init__(self, selector_json_str):

        root_selector = SelectorFactory.create_selector(type="SelectorElement").from_settings()


class Sitemap(object):

    def __init__(self, _id, startUrl, selectors):
        self._id = _id
        self.startUrl = startUrl
        self.selectors = SelectorList(selectors)



