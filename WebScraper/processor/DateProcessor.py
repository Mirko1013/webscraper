#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/13 10:49
# @Author  : mirko
# @FileName: DateProcessor.py
# @Software: PyCharm

from . import RegisterProcessorType, Processor
import re

@RegisterProcessorType("DateProcessor")
class DateProcessor(Processor):

    POSSIBLE_DATE_FORMAT = {
        "%Y-%m-%d": re.compile("\d{4}-\d{1,2}-\d{1,2}"),
        "%Y/%m/%d": re.compile("\d{4}/\d{1,2}/\d{1,2}"),
        "%Y年%m月%d": re.compile("\d{4}年\d{1,2}月\d{1,2}")
    }


    def __init__(self, date_pattern):
        self.date_pattern = date_pattern
        super(DateProcessor, self).__init__()


    def pre_check(self):
        pass

    def get_settings(self):
        return self.date_pattern

    def do_process(self, data, *args, **kwargs):
        pass



    def __str__(self):
        return "---> Date pattern of DateProcessor is {0}".format(self.date_pattern)

    __repr__ = __str__