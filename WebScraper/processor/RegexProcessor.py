#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/13 10:46
# @Author  : mirko
# @FileName: RegexProcessor.py
# @Software: PyCharm

from . import RegisterProcessorType, Processor
import re


class DataExtractNull(Exception):
    pass

@RegisterProcessorType("RegexProcessor")
class RegexProcessor(Processor):

    def __init__(self, regex):
        self.regex = regex
        self.pattern = re.compile(self.regex)

        super(RegexProcessor, self).__init__()

    def pre_check(self):
        pass

    def get_settings(self):
        return self.regex

    def do_process(self, data, *args, **kwargs):
        lst = self.pattern.findall(data)

        if not lst or len(lst) == 0:
            raise DataExtractNull()

        #结果集中有多个str，直接拼接
        return "".join(lst)

    def __str__(self):
        return "---> Pattern string of RegexProcessor is: {0}".format(self.regex)

    __repr__ = __str__
