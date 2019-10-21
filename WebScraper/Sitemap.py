#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/10/20 9:49 PM
# @Author  : mirko
# @FileName: Sitemap.py
# @Software: PyCharm

from WebScraper.selector import *
import json

class Sitemap(object):


    def __init__(self, id, startUrl, selectorsStr):
        self.id = id
        self.startUrl = startUrl
        self.selectors = SelectorFactory.bulid_selector_tree(selectorsStr)

    def getSelectorById(self, selectorId):

        def __recursiveFind(targetId, selector, visitedSelectors):
            curSelectorId = selector.__getattribute__("id")

            if targetId == curSelectorId:
                return selector

            if len(selector.children) == 0 or curSelectorId in visitedSelectors:
                return
            else:
                visitedSelectors.append(curSelectorId)
                for childSelector in selector.children:
                    __recursiveFind(targetId, childSelector, visitedSelectors)

        return __recursiveFind(selectorId, self.selectors, list())

    def getDirectChildSelectors(self, parentSelectorId):
        parentSelector = self.getSelectorById(parentSelectorId)

        return parentSelector.children

    def isCommonSelector(self, selector):



        try:
            return selector.__getattribute__("common")
        except AttributeError:
            pass
