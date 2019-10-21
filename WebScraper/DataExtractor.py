#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 15:53
# @Author  : mirko
# @FileName: DataExtractor.py
# @Software: PyCharm

class DataExtractor(object):

    def __init__(self, browser, sitemap, parentSelectorId, *args, **kwargs):
        self.browser = browser
        self.sitemap = sitemap
        self.parentSelectorId = parentSelectorId

    def generateSelectorTrees(self):
        return self.__recursiveFindSelectorTrees(self.parentSelectorId, list())


    def __recursiveFindSelectorTrees(self, parentSelectorId, commonSelectorsFromParent):
        commonSelectors = commonSelectorsFromParent.extend(self.findAllCommonSelectors(parentSelectorId))


    def findAllCommonSelectors(self, parentSelectorId):
        pass


    def getData(self):
        pass


