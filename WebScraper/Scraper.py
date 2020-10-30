#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 15:53
# @Author  : mirko
# @FileName: Scraper.py
# @Software: PyCharm

from WebScraper.Job import Job
from WebScraper.TaskQueue import TaskQueue
from WebScraper.ChromeBrowser import ChromeBrowser
from WebScraper.action import ActionFactory
from WebScraper.Utils import request_fingerprint
from WebScraper.DBmanager import MongoDB


import logging

logger = logging.getLogger(__name__)

class Scraper(object):

    def __init__(self, queue, sitemap, browser, post_process_hook=None, *args, **kwargs):
        self.queue = queue
        self.sitemap = sitemap
        self.browser = browser
        self.post_process = post_process_hook

        self.results_writer = None
        #MongoDB(host="140.143.240.248", port=27017, username="zhouhuan", password="zh19620522", db="TEST")
        self.results_list = list()
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
        return self.results_writer

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
                #写入database handle的数据，一条record对应于一条finger print，作为后续的判重主键
                record["finger_print"] = request_fingerprint(job.url)

                if "_follow" in record.keys():
                    del record["_follow"]
                    del record["_followSelectorId"]

                #针对单一record的后处理hook func
                if self.post_process:
                    self.post_process(record)

                self.results_list.append(record)
                query = {'finger_print': record['finger_print']}
                doc = {'$set': record}
                #self.results_writer.insert_or_update(query, doc, collection="baijia")
        #close_action = ActionFactory.create_action("CloseAction").from_settings("NULL")
        #close_action.do(self.browser, job.url)
        #TODO 对job返回的数据进行处理，同时递归调用_run()

        self._run()

