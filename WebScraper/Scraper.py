#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 15:53
# @Author  : mirko
# @FileName: Scraper.py
# @Software: PyCharm

from WebScraper.Job import Job
from WebScraper.TQueue import TaskQueue
from WebScraper.ChromeBrowser import ChromeBrowser

import logging

logger = logging.getLogger(__name__)

class Scraper(object):

    def __init__(self, queue, sitemap, browser, *args, **kwargs):
        self.queue = queue
        self.sitemap = sitemap
        self.browser = browser

        #TODO 数据库存放相关的句柄


    def initFirstJob(self):
        startUrl = self.sitemap.__getattribute__("startUrl")

        rootJob = Job(url=startUrl, parentSelectorId="_root", scraper=self, parentJob=None, baseData=None)

        if not self.queue.isFull():
            self.queue.add(rootJob)
        else:
            raise RuntimeError("任务队列异常，Scraper初始化终止.")

    def run(self):

        self.initFirstJob()

        #TODO 初始化数据库写入实例

        self._run()


    def record_can_have_child_jobs(self, record):
        if "_follow" not in record.keys():
            return False

        followSelectorId = record.get("_followSelectorId")
        selector = self.sitemap.getSelectorById(followSelectorId)
        if hasattr(selector, "children") and len(selector.children) == 0:
            return False
        else:
            return True

    def _run(self):
        scrapedRecords = list()


        job = self.queue.getNextJob()

        if not job:
            logger.info("数据抓取已完成...")
            return

        job.execute(browser=self.browser)

        results = job.getResults()



        for record in results:
            if self.record_can_have_child_jobs(record):
                follow_url = record.get("_follow")
                follow_selector = record.get("_followSelectorId")
                del record["_follow"]
                del record["_followSelectorId"]

                new_job = Job(url=follow_url, parentSelectorId=follow_selector, scraper=self, parentJob=job, baseData=record)

                if not self.queue.isFull():
                    self.queue.add(new_job)
            else:
                if "_follow" in record.keys():
                    del record["_follow"]
                    del record["_followSelectorId"]
                scrapedRecords.append(record)




        #TODO 对job返回的数据进行处理，同时递归调用_run()

        self._run()

