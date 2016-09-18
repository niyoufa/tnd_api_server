# -*- coding: utf-8 -*-

"""
    alter by: youfaNi
    alter on 2016-07-14
"""
import json,pdb
import oauth2
import datetime
import tornado
import urllib
from dhuicredit.handler import TokenAPIHandler
from dhuicredit.handler import APIHandler
from dhuicredit.app import get_options
import dhuicredit.libs.utils as utils
import dhuicredit.model.checkcode as checkcode_model
import dhuicredit.model.user as user_model
import dhuicredit.handlers.oauth as oauth

# log = log_model.LogModel()

class MobileCheckCode(APIHandler):
    # @log.write_log
    def get(self):
        # log_model = log_model.LogModel()
        # log_model.write_log(self.request)
        result = utils.init_response_data()
        checkcode_model_obj = checkcode_model.CheckCode()
        checkcode_coll = checkcode_model_obj.get_coll()
        try:
            mobile = self.get_argument("mobile")

            curr_time = datetime.datetime.now()
            if checkcode_coll.find({"mobile":mobile,"enable_flag":True}).count() > 0:
                # 验证码请求限制 每小时限制5条
                if checkcode_coll.find({"mobile":mobile,
                        "create_date":{
                            "$gte":curr_time - datetime.timedelta(hours=1),
                            "$lte":curr_time + datetime.timedelta(hours=1),
                        }
                    }).count() >= 5:
                    raise Exception("验证码请求限制，每小时限制5条！")

                cr = checkcode_coll.find({"mobile":mobile,"enable_flag":True})
                for checkcode in cr:
                    checkcode["enable_flag"] = False
                    checkcode_coll.save(checkcode)
            else:
                pass
            random_code = utils.get_random_num(6,mode="number")
            checkcode_coll.insert_one({
                "mobile":mobile,
                "enable_flag":True,
                "create_date":curr_time,
                "type":"mobile",
                "code":random_code,
            })
            result["code"] = random_code
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

class EmailCheckCode(APIHandler):
    def get(self):
        result = utils.init_response_data()
        checkcode_model_obj = checkcode_model.CheckCode()
        checkcode_coll = checkcode_model_obj.get_coll()
        try:
            email = self.get_argument("email")

            curr_time = datetime.datetime.now()
            if checkcode_coll.find({"email": email, "enable_flag": True}).count() > 0:
                # 验证码请求限制 每天限制5条
                if checkcode_coll.find({"email": email,
                                        "create_date": {
                                            "$gte": curr_time - datetime.timedelta(hours=1),
                                            "$lte": curr_time + datetime.timedelta(hours=1),
                                        }
                                        }).count() >= 5:
                    raise Exception("验证码请求限制，每小时限制5条！")

                cr = checkcode_coll.find({"email": email, "enable_flag": True})
                for checkcode in cr:
                    checkcode["enable_flag"] = False
                    checkcode_coll.save(checkcode)
            else:
                pass
            random_code = utils.get_random_num(6,mode="number")
            checkcode_coll.insert_one({
                "email": email,
                "enable_flag": True,
                "create_date": curr_time,
                "type": "email",
                "code": random_code,
            })
            result["code"] = random_code
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)


handlers = [
    (r"/api/checkcode/mobile", MobileCheckCode),
    (r"/api/checkcode/email", EmailCheckCode),
]
