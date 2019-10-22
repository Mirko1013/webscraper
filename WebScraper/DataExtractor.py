#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 15:53
# @Author  : mirko
# @FileName: Scraper.py
# @Software: PyCharm

from copy import deepcopy

class DataExtractor(object):

    def __init__(self, browser, sitemap, parentSelectorId, *args, **kwargs):
        self.browser = browser
        self.sitemap = sitemap
        self.parentSelectorId = parentSelectorId

    def generateSelectorTrees(self):
        return self.__recursiveFindSelectorTrees(self.parentSelectorId, list())


    def __recursiveFindSelectorTrees(self, parentSelectorId, commonSelectorsFromParent):

        commonSelectors = commonSelectorsFromParent.copy()
        commonSelectors.extend(self.findAllCommonSelectors(parentSelectorId))
        #commonSelectors = commonSelectorsFromParent.copy().extend(self.findAllCommonSelectors(parentSelectorId))
        #print(parentSelectorId, self.findAllCommonSelectors(parentSelectorId), commonSelectorsFromParent, commonSelectors)
        selectorTrees = list()

        directChildSelectors = self.sitemap.getDirectChildSelectors(parentSelectorId)
        for childSelector in directChildSelectors:
            if not self.sitemap.isCommonSelector(childSelector):
                print(childSelector.__getattribute__("id"))
                if not childSelector.can_have_local_child(): #link等需要在新页面打开的导航节点
                    newSelectorTree = commonSelectors.copy()
                    newSelectorTree.append(childSelector)
                    selectorTrees.append(newSelectorTree)
                else:  #element等内容封装节点
                    commonSelectorsFromParent = commonSelectors.copy()
                    commonSelectorsFromParent.append(childSelector)
                    childSelectorTrees = self.__recursiveFindSelectorTrees(childSelector.__getattribute__("id"), commonSelectorsFromParent)
                    selectorTrees.append(childSelectorTrees)

        if len(selectorTrees) == 0:
            return list(commonSelectors)
        else:
            return selectorTrees

    def findAllCommonSelectors(self, parentSelectorId):
        commonSelectors = list()
        #拿到parentSelector的直接子节点
        directChildSelectors = self.sitemap.getDirectChildSelectors(parentSelectorId)

        for childSelector in directChildSelectors:
            if self.sitemap.isCommonSelector(childSelector):
                commonSelectors.append(childSelector)
                #由common selector的特征决定，所有子节点均为common类型
                self.sitemap.getAllChildSelectors(childSelector.__getattribute__("id"))

        return commonSelectors

    def getData(self):
        selectorTrees = self.generateSelectorTrees()


