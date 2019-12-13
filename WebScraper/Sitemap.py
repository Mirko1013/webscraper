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
from WebScraper.selector.AttributeSelector import AttributeSelector
from WebScraper.selector.ClickSelector import ClickSelector
from WebScraper.selector.ScrollSelector import ScrollSelector

from WebScraper.processor.RegexProcessor import RegexProcessor


import logging
import json

logger = logging.getLogger(__name__)

class Sitemap(object):


    def __init__(self, id, startUrl, selectorsStr):
        self.id = id
        self.startUrl = startUrl
        self.selectors = SelectorFactory.bulid_selector_tree(selectorsStr)


    def getSelectorById(self, selectorId):

        def _recursive_find(selector, _selector_id):
            if selector.__getattribute__("id") == _selector_id:
                return selector

            if selector.children:
                for child_selector in selector.children:
                    found = _recursive_find(child_selector, _selector_id)
                    if found:
                        return found

            else:
                return None

        return _recursive_find(self.selectors, selectorId)


    # def getSelectorById(self, selectorId):
    #
    #     def _recursiveFind(targetId, selector, visitedSelectors):
    #
    #         if not selector:
    #             return None
    #
    #         curSelectorId = selector.__getattribute__("id")
    #
    #         if targetId == curSelectorId:
    #             return selector
    #
    #         if curSelectorId in visitedSelectors:
    #             return None
    #
    #         visitedSelectors.append(curSelectorId)
    #
    #         for childSelector in selector.children:
    #             if _recursiveFind(targetId, childSelector, visitedSelectors):
    #                 return _recursiveFind(targetId, childSelector, visitedSelectors)
    #
    #     return _recursiveFind(selectorId, self.selectors, list())
    #

    def getDirectChildSelectors(self, parentSelectorId):
        parentSelector = self.getSelectorById(parentSelectorId)

        return parentSelector.children


    def getAllChildSelectors(self, parentSelectorId):
        #结果集合
        childSelectors = list()

        parentSelector = self.getSelectorById(parentSelectorId)

        def _recursiveFind(selector, visitedSelectors):

            if not selector or selector.__getattribute__("id") in visitedSelectors:
                return

            childSelectors.append(selector)
            visitedSelectors.append(selector.__getattribute__("id") )

            for childSelector in selector.children:
                _recursiveFind(childSelector, visitedSelectors)



        _recursiveFind(parentSelector, list())

        return childSelectors

    def setCommonTag(self, selectorId):

        parentSelector = self.getSelectorById(selectorId)

        def _recursiveFind(selector, visitedSelectors):
            if not selector or selector.__getattribute__("id") in visitedSelectors:
                return

            tag = True


            for childSelector in selector.children:
                _recursiveFind(childSelector, visitedSelectors)
                tag = tag & childSelector.__getattribute__("common")


            if selector.will_return_multiple_records():
                tag = False

            if selector.will_return_new_jobs() and len(selector.children) > 0:
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