#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 15:53
# @Author  : mirko
# @FileName: Queue.py
# @Software: PyCharm

from queue import Queue


class TaskQueue(object):


    def __init__(self):
        self.queue = Queue()



    def add(self, job):
        pass

    def canBeAdded(self, job):


    def getTaskQueueSize(self):
        return self.queue.qsize()



