#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/28 8:55
# @Author  : mirko
# @FileName: DBmanager.py
# @Software: PyCharm
import pymongo


class MongoDB(object):

    def __init__(self, host, port, username, password, db):
        try:
            self.mongodb_client = pymongo.MongoClient(host=host, port=port)
            #先通过admin认证连接mongodb
            self.mongodb_client["admin"].authenticate(name=username, password=password, mechanism="SCRAM-SHA-1")
            #切换db
            self.db_connection = self.mongodb_client[db]
        except Exception as e:
            import traceback
            traceback.print_exc()



    def insert_or_update(self, query, doc, collection):
        coll = self.db_connection[collection]
        try:
            #.update_one({'link_url': item['link_url']}, {'$set': dict(item)}, upsert=True)
            coll.update_one(query, doc, upsert=True)
            #.update(query, doc, upsert=True)
        except Exception as e:
            pass




    def close(self):
        try:
            self.db_connection.close()
            self.mongodb_client.close()
        except Exception as e:
            import traceback
            traceback.print_exc()


class RedisDB(object):
    def __init__(self):
        pass


class SQLiteDB(object):

    def __init__(self):
        pass


class MysqlDB(object):

    def __init__(self):
        pass