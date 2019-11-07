#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 15:53
# @Author  : mirko
# @FileName: Scraper.py
# @Software: PyCharm

from copy import deepcopy

class DataExtractor(object):

    def __init__(self, driver, url, sitemap, parentSelectorId, parentElement,*args, **kwargs):
        self.url = url
        self.driver = driver
        self.sitemap = sitemap
        self.parentSelectorId = parentSelectorId
        self.parentElement = parentElement


    def generateSelectorTrees(self):
        return self.__recursiveFindSelectorTrees(self.parentSelectorId, list())


    def __recursiveFindSelectorTrees(self, parentSelectorId, commonSelectorsFromParent):

        commonSelectors = commonSelectorsFromParent.copy()
        commonSelectors.extend(self.findAllCommonSelectors(parentSelectorId))

        selectorTrees = list()

        directChildSelectors = self.sitemap.getDirectChildSelectors(parentSelectorId)
        for childSelector in directChildSelectors:
            if not self.sitemap.isCommonSelector(childSelector):
                if not childSelector.will_return_local_childs(): #link等需要在新页面打开的导航节点
                    newSelectorTree = commonSelectors.copy()
                    newSelectorTree.append(childSelector)
                    selectorTrees.append(newSelectorTree)
                else:  #element等内容封装节点
                    commonSelectorsFromParent = commonSelectors.copy()
                    commonSelectorsFromParent.append(childSelector)
                    childSelectorTrees = self.__recursiveFindSelectorTrees(childSelector.__getattribute__("id"), commonSelectorsFromParent)
                    selectorTrees.extend(childSelectorTrees)

        if len(selectorTrees) == 0:
            selectorTrees.append(commonSelectors)

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

    def getSelectorTreeData(self, currentSelectorTree, parentSelectorId, parentElement, commonData):
        resultData = []

        childCommonData = self.getSelectorTreeCommonData(currentSelectorTree, parentSelectorId, parentElement)
        commonData.update(childCommonData)

        directChildSelectors = self.sitemap.getDirectChildSelectors(parentSelectorId)
        for childSelector in directChildSelectors:
            if childSelector.will_return_multiple_records():
                newCommonData = commonData.copy()
                child_records = self.getMultiSelectorData(currentSelectorTree, childSelector.__getattribute__("id"), parentElement, newCommonData)

                for record in child_records:
                    newRecord = dict()
                    newRecord.update(record)
                    resultData.append(newRecord)

        if len(resultData) == 0:
            if len(commonData.keys()) == 0:
                return list()
            else:
                resultData.append(commonData)
                return resultData
        else:
            return resultData



    def getSelectorTreeCommonData(self, currentSelectorTree, parentSelectorId, parentElement):
        commonData = dict()
        directChildSelectors = self.sitemap.getDirectChildSelectors(parentSelectorId)

        for childSelector in directChildSelectors:
            if not childSelector.will_return_multiple_records():
                currentCommonData = self.getSelectorCommonData(currentSelectorTree, childSelector.__getattribute__("id"), parentElement)
                commonData.update(currentCommonData)

        return commonData

    def getSelectorCommonData(self, currentSelectorTree, parentSelectorId, parentElement):
        selector = self.sitemap.getSelectorById(parentSelectorId)

        data = selector.get_data(self.driver, self.url, parentElement)

        if selector.can_return_elements:
            newParentElement = data[0]
            data = self.getSelectorTreeCommonData(currentSelectorTree, selector.__getattribute__("id"), newParentElement)
            return data

        return data[0]

    def getMultiSelectorData(self, currentSelectorTree, parentSelectorId, parentElement, commonData):
        resultData = []
        currentSelector = self.sitemap.getSelectorById(parentSelectorId)

        if not currentSelector.will_return_elements():
            selectorData = currentSelector.get_data(self.driver, self.url, parentElement)
            newCommonData = commonData.copy()
            for record in selectorData:
                record.update(newCommonData)
                resultData.append(record)

            return resultData

        #进入element处理逻辑
        selectorElements = currentSelector.get_data(self.driver, self.url, parentElement)

        for element in selectorElements:
            newCommonData = commonData.copy()
            childRecords = self.getSelectorTreeData(currentSelector, parentSelectorId, element, newCommonData)
            for record in childRecords:
                record.update(newCommonData)
                resultData.append(record)

        return resultData



    def getData(self):
        data_result = list()

        selectorTrees = self.generateSelectorTrees()

        for oneSelectorTree in selectorTrees:
            results = self.getSelectorTreeData(oneSelectorTree, self.parentSelectorId, self.parentElement, {})
            data_result.extend(results)

        return data_result