# -*- coding: utf-8 -*-

"""
    author : youfaNi
    date : 2016-07-13
"""

import pdb, datetime
import tnd_api_server.model.mongo as mongo
import tnd_api_server.libs.utils as utils

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

class BaseModel(object):

    def __init__(self,name):
        self.__name = name

    def coll_name(self):
        return self.__name.split(".")[1]

    def db_name(self):
        return self.__name.split(".")[0]

    def get_coll(self):
        coll_name = self.coll_name()
        coll = mongo.get_coll(coll_name)
        return coll

    def create(self, **obj):
        coll = self.get_coll()
        curr_time = datetime.datetime.now()
        obj["create_date"] = str(curr_time)
        ret = coll.insert_one(obj)
        return ret

    def search(self, query_params):
        coll = self.get_coll()
        ret = coll.find_one(query_params)
        ret = utils.dump(ret)
        return ret

    def update(self, query_params, update_params):
        coll = self.get_coll()
        obj = coll.find_one(query_params)
        if obj:
            update_params.update({
                "create_date": obj["create_date"],
            })
            ret = coll.save(update_params)

    def delete(self, **query_params):
        coll = self.get_coll()
        ret = coll.remove(query_params)
        return ret