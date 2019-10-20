#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 15:53
# @Author  : mirko
# @FileName: Job.py
# @Software: PyCharm

class Job(object):

    def __init__(self, url, parentSelectorId, scraper, parentJob, baseData):
        if parentJob:
            self.url = parentJob.url + url
        else:
            self.url = url

        self.parentSelectorId = parentSelectorId
        self.scraper = scraper
        self.dataItems = list()
        self.baseData = baseData if baseData else dict()


    def execute(self, browser):
        sitemap = self.scraper.sitemap
        results = browser.fetchData(self.url, sitemap, self.parentSelectorId)

        #TODO 对results进行处理，合并入dataItems

    def getResults(self):
        return self.dataItems