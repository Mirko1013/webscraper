#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 15:53
# @Author  : mirko
# @FileName: Job.py
# @Software: PyCharm

class Job(object):

    def __init__(self, url, parentSelector, scraper, parentJob, baseData):
        if not parentJob:
            self.url = parentJob.url + url
        else:
            self.url = url

        self.parentSelector = parentSelector
        self.scraper = scraper
        self.dataItems = list()
        self.baseData = baseData if baseData else dict()


    def execute(self, browser):
        sitemap = self.scraper.sitemap
        results = browser.fetchData(self.url, sitemap, self.parentSelector)

    def getResults(self):
        return self.dataItems