#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 15:53
# @Author  : mirko
# @FileName: TQueue.py
# @Software: PyCharm

from queue import Queue


class TaskQueue(object):


    def __init__(self):
        self.queue = Queue()

    def add(self, job):
        #TODO 维护一个全局缓存，采用redis实现的SimHash算法或BloomFilter算法进行过滤


        if not self.isFull():
            self.queue.put(job, block=False)
            #TODO 设置已经抓取的tag
            return True
        else:
            return False

    def getTaskQueueSize(self):
        return self.queue.qsize()


    def isFull(self):
        return True if self.queue.full() else False

    def getNextJob(self):
        if not self.queue.empty():
            return self.queue.get(block=False)
        else:
            return False