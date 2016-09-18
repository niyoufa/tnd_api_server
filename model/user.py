# -*- coding: utf-8 -*-

"""
    author : youfaNi
    date : 2016-07-13
"""

from dhuicredit.app import get_options
import dhuicredit.model.model as model
import dhuicredit.model.Redis as Redis
import dhuicredit.model.mongo as mongo
import dhuicredit.consts as consts
import dhuicredit.libs.utils as utils
from bson.son import SON
import pdb

class UserModel(model.BaseModel,model.Singleton):
    __name = "dhuicredit.user"

    def __init__(self):
        model.BaseModel.__init__(self,UserModel.__name)

    def get_token_uid(self,token):
        redis_tool = Redis.RedisTool()
        uid = redis_tool.get(token)
        return uid

    def save_token_uid(self,token,uid):
        redis_tool = Redis.RedisTool()
        if not redis_tool.get(token):
            redis_tool.set(token,uid)
        else:
            pass

    def is_exist(self,mobile=None,email=None):
        user_coll = self.get_coll()
        if mobile:
            user = user_coll.find_one({
                "mobile":mobile,
            })
        elif email :
            user = user_coll.find_one({
                "email":email
            })
        else:
            return False
        if user :
            return True
        else:
            return False

