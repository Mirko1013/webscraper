#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/10/20 9:49 PM
# @Author  : mirko
# @FileName: Sitemap.py
# @Software: PyCharm

from WebScraper.selector import SelectorFactory
from WebScraper.selector.TextSelector import TextSelector
from WebScraper.selector.LinkSelector import LinkSelector
from WebScraper.selector.ElementSelector import ElementSelector

import logging
import json

logger = logging.getLogger(__name__)

class Sitemap(object):


    def __init__(self, id, startUrl, selectorsStr):
        self.id = id
        self.startUrl = startUrl
        self.selectors = SelectorFactory.bulid_selector_tree(selectorsStr)

    def getSelectorById(self, selectorId):

        resultSelector = None

        def _recursiveFind(targetId, selector, visitedSelectors, targetSelector):
            curSelectorId = selector.__getattribute__("id")

            if targetId == curSelectorId:
                targetSelector = selector
                return

            visitedSelectors.append(curSelectorId)

            if len(selector.children) == 0 or curSelectorId in visitedSelectors:
                return

            for childSelector in selector.children:
                _recursiveFind(targetId, childSelector, visitedSelectors, targetSelector)

        _recursiveFind(selectorId, self.selectors, list(), resultSelector)

        print(resultSelector)
        return resultSelector

    def getDirectChildSelectors(self, parentSelectorId):
        parentSelector = self.getSelectorById(parentSelectorId)

        return parentSelector.children


    def getAllChildSelectors(self, parentSelectorId):
        #结果集合
        childSelectors = list()

        parentSelector = self.getSelectorById(parentSelectorId)

        def _recursiveFind(selector, visitedSelectors):

            if len(selector.children) == 0 or selector.__getattribute__("id") in visitedSelectors:
                return

            for childSelector in selector.children:
                childSelectors.append(childSelector)
                visitedSelectors.append(childSelector.__getattribute__("id"))
                _recursiveFind(childSelector, visitedSelectors)



        _recursiveFind(parentSelector, list())

        return childSelectors

    def setCommonTag(self, selectorId):

        parentSelector = self.getSelectorById(selectorId)

        def _recursiveFind(selector, visitedSelectors):
            if not selector or selector.__getattribute__("id") in visitedSelectors:
                return

            tag = True

            if len(selector.children) > 0:
                for childSelector in selector.children:
                    _recursiveFind(childSelector, visitedSelectors)
                    tag = tag & childSelector.__getattribute__("common")


            if selector.will_return_multiple_records():
                tag = False

            if selector.can_create_new_jobs and len(selector.children) > 0:
                tag = False

            visitedSelectors.append(selector.__getattribute__("id"))
            selector.__setattr__("common", tag)

        _recursiveFind(parentSelector, list())

    def isCommonSelector(self, selector):
        try:
            return selector.__getattribute__("common")
        except AttributeError:
            self.setCommonTag("_root")
            return selector.__getattribute__("common")