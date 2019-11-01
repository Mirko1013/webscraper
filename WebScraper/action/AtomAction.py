#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 14:41
# @Author  : mirko
# @FileName: AtomAction.py
# @Software: PyCharm

from . import RegisterActionType, Action

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.common.by import By


@RegisterActionType("OpenAction")
class OpenAction(Action):

    def __init__(self):
        pass

    def pre_check(self, protocol):
        pass

    def do(self, **kwargs):
        pass

@RegisterActionType("WaitAction")
class WaitAction(Action):
    """
        协议如下:{"conditions":"", "timeout": 5}
    """
    def __init__(self, protocol):
        super(WaitAction, self).__init__(protocol)


    def pre_check(self, protocol):
        pass

    def do(self, **kwargs):
        pass

@RegisterActionType("ClickAction")
class ClickAction(Action):

    def __init__(self):
        pass

    def pre_check(self, protocol):
        pass

    def do(self, **kwargs):
        pass

@RegisterActionType("CloseAction")
class CloseAction(Action):

    def __init__(self):
        pass

    def pre_check(self, protocol):
        pass

    def do(self, **kwargs):
        pass


