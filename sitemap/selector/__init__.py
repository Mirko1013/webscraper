#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 9:07 AM
# @Author  : mirko
# @FileName: __init__.py.py
# @Software: PyCharm

import abc


class RegisterSelectorType(object):

    selector_type = {}

    def __init__(self, type):
        self._type = type

    def __call__(self, cls, *args, **kwargs):

        if not self.selector_type.__contains__(self._type):
            self.selector_type[self._type] = cls

        return cls


class SelectorFactory(object):

    __selector_type = RegisterSelectorType.selector_type

    @classmethod
    def create_selector(cls, type):

        if cls.__selector_type.__contains__(type):
            return cls.__selector_type[type]()
        else:
            raise NotImplementedError()

    @classmethod
    def bulid_selector_tree(cls, _json_selectors):
        """
        构筑一棵json字符串表示的selector tree
        :param _json_selectors:
        :return: 各种selector实例组成的selector tree,根节点为root
        """
        root_selector = Selector('_root', None, None, None)

        def build(p_selector, selectors, created_selector):
            parent_selector_id = p_selector.id   #拿到父节点的id

            for selector in selectors:
                if parent_selector_id  in selector.get("parentSelectors"):
                    current_selector_id = selector.get("id")  # 拿到当前节点的id
                    if current_selector_id in created_selector.keys():
                        child_selector = created_selector[current_selector_id]
                    else:
                        new_selector = SelectorFactory.create_selector(selector.get("type"))

                    if p_selector.children:
                        p_selector.children.append()
                    else:
                        p_selector.children = [created_selector[current_selector_id], ]


            return p_selector


        return build(root_selector, _json_selectors, {})

class Selector(object):
    can_return_multiple_records = False     #能否返回多条记录
    can_have_child_selectors = False        #能有拥有孩子节点
    can_have_local_child_selectors = False  #能否在当前页面拥有孩子节点
    can_create_new_jobs = False             #能否产生新的任务
    can_return_elements = False             #返回元素

    features = {
        'id': '',
        'type': None,
        'css_paths': '',
        'parent_selectors': []
    }

    @classmethod
    def get_features(cls):
        return cls.features.copy()

    @classmethod
    def from_settings(cls, settings):
        #取得每个selecotr的特征值列表
        features = cls.get_features()

        #对于features不存在，settings中存在的值，删去
        for key in settings.keys():
            if key not in features.keys():
                del settings[key]

        #对于features存在，但settings不存在的值，赋予默认值
        for key, value in features:
            if key not in settings.keys():
                settings[key] = value

        #生成实例
        selector = cls(**settings)

        return selector

    def __init__(self, id, type, css_paths, parent_selectors, **kwargs):
        """
        :param id:
        :param type:
        :param css_paths:
        :param parent_selectors:
        :param kwargs:
        """
        self.id = id
        self.type = type
        self.css_paths = css_paths
        self.parent_selectors = parent_selectors
        self.children = []



    def will_return_multiple_records(self):
        raise NotImplementedError()

    def get_data(self):
        pass



