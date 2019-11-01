#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 11:34
# @Author  : mirko
# @FileName: __init__.py.py
# @Software: PyCharm

from WebScraper.Utils import arg2iter

class RegisterActionType(object):

    action_type = {}

    def __init__(self, type):
        self._type = type

    def __call__(self, cls, *args, **kwargs):
        if not self.action_type.__contains__(self._type):
            self.action_type[self._type] = cls

        return cls

class ActionFactory(object):

    __action_type = RegisterActionType.action_type

    @classmethod
    def create_action(cls, type):

        if cls.__action_type.__contains__(type):
            return cls.__action_type[type]
        else:
            raise NotImplementedError()

    @classmethod
    def gen_actions_chain(cls, actions, **kwargs):

        actions_chain = list()

        for action in arg2iter(actions):
            for action_type, options in action.items():
                action_class = ActionFactory.create_action(action_type)
                action_instance = action_class(options, **kwargs)
                actions_chain.append(action_instance)

        return actions_chain

class Action(object):

    def __init__(self, protocol):
        self.pre_check(protocol)
        self.protocol = protocol


    def pre_check(self, protocol):
        raise NotImplementedError()

    def do(self, **kwargs):
        raise NotImplementedError()