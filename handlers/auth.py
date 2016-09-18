# -*- coding: utf-8 -*-

"""
    author : youfaNi
    date : 2016-07-13
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
import dhuicredit.model.user as user_model
import dhuicredit.model.auth as auth_model
import dhuicredit.model.image as image_model
import dhuicredit.model.oauth as oauth_model
import dhuicredit.model.checkcode as checkcode_model
import dhuicredit.handlers.oauth as oauth
options = get_options()

class AuthPersonHandler(TokenAPIHandler):
    def post(self):
        result = utils.init_response_data()
        user_model_obj = user_model.UserModel()
        auth_model_obj = auth_model.AuthModel()
        image_model_obj = image_model.ImageModel()
        try:
            name = self.get_argument("name")
            id_card = self.get_argument("id_card")
            files = self.request.files
            [front_photo] = files.get("front_photo",[""])
            [back_photo] = files.get("back_photo",[""])
            [hand_photo] = files.get("hand_photo",[""])
            [promise_photo] = files.get("promise_photo",[""])
            access_token = self.get_argument("access_token")


            if name == "":
                raise Exception("请输入用户真实姓名！")
            elif id_card == "":
                raise Exception("请输入身份证号！")
            elif not auth_model_obj.check_format(id_card):
                raise Exception("身份证格式错误！")
            elif not auth_model_obj.check_validate(id_card):
                raise Exception("身份证无效！")
            elif front_photo == "":
                raise Exception("请输入身份证正面照！")
            elif back_photo == "":
                raise Exception("请输入身份证反面照！")
            elif hand_photo == "":
                raise Exception("请输入手持身份证照片！")
            elif promise_photo == "":
                raise Exception("请输入承诺书照片！")

            front_photo["upload_key"] = "front_photo"
            back_photo["upload_key"] = "back_photo"
            hand_photo["upload_key"] = "hand_photo"
            promise_photo["upload_key"] = "promise_photo"

            image_list = [front_photo,back_photo,hand_photo,promise_photo]
            image_info_list = image_model_obj.upload_image(image_list)
            photo_url_dict = {}
            for image_info in image_info_list:
                photo_url_dict[image_info["upload_key"]] = image_info["file_path"]

            uid = user_model_obj.get_token_uid(access_token)
            if not uid :
                raise Exception("redis 已过期！")
            status = options["auth_status"]["committed"]
            comments = ""
            edit_status = options.edit_status["edit"]
            type = options.auth_type["person"]
            auth_obj = {
                    'name':name,
                    'id_card':id_card,
                    'front_photo':photo_url_dict["front_photo"],
                    'back_photo':photo_url_dict["back_photo"],
                    'hand_photo':photo_url_dict["hand_photo"],
                    'promise_photo':photo_url_dict["promise_photo"],
                    'uid':uid,
                    'status':status,
                    'comments':comments,
                    'edit_status':edit_status,
                    'type':type,
                }
            auth_coll = auth_model_obj.get_coll()
            if auth_coll.find({'uid':uid,'type':type}).count() > 0:
                temp_auth_obj = auth_coll.find_one({'uid':uid,'type':type})
                auth_obj["_id"] = temp_auth_obj["_id"]
                auth_coll.save(auth_obj)
            else:
                auth_coll.insert_one(auth_obj)
        except Exception, e:
            result = utils.reset_response_data(0, str(e))
            self.finish(result)
            return

        self.finish(result)

    def get(self):
        result = utils.init_response_data()
        user_model_obj = user_model.UserModel()
        auth_model_obj = auth_model.AuthModel()
        try:
            access_token = self.get_argument("access_token")
            uid = user_model_obj.get_token_uid(access_token)
            if not uid:
                raise Exception("redis 已过期！")
            auth_coll = auth_model_obj.get_coll()
            auth_obj = auth_coll.find_one({'uid':uid,'type':options["auth_type"]["person"]})
            if not auth_obj:
                raise Exception("还未提交个人用户实名认证信息")
            else:
                result["data"] = utils.dump(auth_obj)
        except Exception, e:
            result = utils.reset_response_data(0, str(e))
            self.finish(result)
            return

        self.finish(result)


class AuthEnterpriseHandler(TokenAPIHandler):
    def post(self):
        result = utils.init_response_data()
        user_model_obj = user_model.UserModel()
        auth_model_obj = auth_model.AuthModel()
        image_model_obj = image_model.ImageModel()
        try:
            name = self.get_argument("name")
            org_id = self.get_argument("org_id")
            reg_addr = self.get_argument("reg_addr")
            work_addr = self.get_argument("work_addr")
            files = self.request.files
            [front_photo] = files.get("front_photo",[""])
            [back_photo] = files.get("back_photo",[""])
            [business_licence] = files.get("business_licence",[""])
            [promise_photo] = files.get("promise_photo",[""])
            access_token = self.get_argument("access_token")

            if name == "":
                raise Exception("请输入企业名称！")
            elif org_id == "":
                raise Exception("请输入组织机构代码！")
            elif reg_addr == "":
                raise Exception("请输入公司注册地址！")
            elif work_addr == "":
                raise Exception("请输入公司办公地址！")
            elif business_licence == "":
                raise Exception("请输入营业执照！")
            elif front_photo == "":
                raise Exception("请输入法人身份证正面照！")
            elif back_photo == "":
                raise Exception("请输入法人身份证反面照！")
            elif promise_photo == "":
                raise Exception("请输入承诺书签名照！")

            front_photo["upload_key"] = "front_photo"
            back_photo["upload_key"] = "back_photo"
            business_licence["upload_key"] = "business_licence"
            promise_photo["upload_key"] = "promise_photo"

            image_list = [front_photo, back_photo, business_licence, promise_photo]
            image_info_list = image_model_obj.upload_image(image_list)
            photo_url_dict = {}
            for image_info in image_info_list:
                photo_url_dict[image_info["upload_key"]] = image_info["file_path"]

            uid = user_model_obj.get_token_uid(access_token)
            if not uid:
                raise Exception("redis 已过期！")
            status = options["auth_status"]["committed"]
            comments = ""
            edit_status = options.edit_status["edit"]
            type = options.auth_type["company"]
            auth_obj = {
                'name': name,
                'org_id': org_id,
                'reg_addr':reg_addr,
                'work_addr':work_addr,
                'front_photo': photo_url_dict["front_photo"],
                'back_photo': photo_url_dict["back_photo"],
                'business_licence': photo_url_dict["business_licence"],
                'promise_photo': photo_url_dict["promise_photo"],
                'uid': uid,
                'status': status,
                'comments': comments,
                'edit_status': edit_status,
                'type' : type,
            }
            auth_coll = auth_model_obj.get_coll()
            if auth_coll.find({'uid':uid,'type':type}).count() > 0:
                temp_auth_obj = auth_coll.find_one({'uid':uid,'type':type})
                auth_obj["_id"] = temp_auth_obj["_id"]
                auth_coll.save(auth_obj)
            else:
                auth_coll.insert_one(auth_obj)
        except Exception, e:
            result = utils.reset_response_data(0, str(e))
            self.finish(result)
            return

        self.finish(result)

    def get(self):
        result = utils.init_response_data()
        user_model_obj = user_model.UserModel()
        auth_model_obj = auth_model.AuthModel()
        try:
            access_token = self.get_argument("access_token")
            uid = user_model_obj.get_token_uid(access_token)
            if not uid:
                raise Exception("redis 已过期！")
            auth_coll = auth_model_obj.get_coll()
            auth_obj = auth_coll.find_one({'uid': uid, 'type': options["auth_type"]["company"]})
            if not auth_obj:
                raise Exception("还未提交企业用户实名认证信息")
            else:
                result["data"] = utils.dump(auth_obj)
        except Exception, e:
            result = utils.reset_response_data(0, str(e))
            self.finish(result)
            return

        self.finish(result)

class AuthCheckHandler(APIHandler):
    def post(self):
        result = utils.init_response_data()
        auth_model_obj = auth_model.AuthModel()
        try:
            auth_id = self.get_argument("auth_id")
            status = self.get_argument("status")

            auth_coll = auth_model_obj.get_coll()

            if auth_id == "":
                raise Exception("auth_id 不可为空")
            elif auth_coll.find({"_id": utils.create_objectid(auth_id)}).count() == 0:
                raise Exception("实名认证信息不存在！")
            elif status not in options["auth_status"].keys():
                raise Exception("认证状态错误 KeyError：%s" % status)

            auth_obj = auth_coll.find_one({"_id": utils.create_objectid(auth_id)})
            auth_obj["status"] = options.auth_status[status]
            if status in ["checking", "pass"]:
                auth_obj["edit_status"] = options.edit_status["noedit"]
            elif status in ["nopass"]:
                auth_obj["edit_status"] = options.edit_status["edit"]
            else:
                raise Exception("操作限制 %s" % status)

            auth_coll.save(auth_obj)

        except Exception, e:
            result = utils.reset_response_data(0, str(e))
            self.finish(result)
            return

        self.finish(result)

class AuthListHandler(APIHandler):
    def get(self):
        result = utils.init_response_data()
        auth_model_obj = auth_model.AuthModel()
        try:
            type = self.get_argument("type")
            page = self.get_argument("page", 1)
            page_size = self.get_argument("page_size", 10)

            auth_coll = auth_model_obj.get_coll()

            if not type in options["auth_type"].keys():
                raise Exception("auth type error : %s" % type)

            start = (int(page) - 1) * int(page_size)
            end = int(page) * int(page_size)
            cr = auth_coll.find({"type": options["auth_type"][type]})[start:end]
            auth_obj_list = [utils.dump(auth_obj) for auth_obj in cr]
            result["data"] = auth_obj_list

        except Exception, e:
            result = utils.reset_response_data(0, str(e))
            self.finish(result)
            return

        self.finish(result)

handlers = [
    (r"/api/auth/person", AuthPersonHandler,dict(provider=oauth.init_oauth())),
    (r"/api/auth/company", AuthEnterpriseHandler,dict(provider=oauth.init_oauth())),
    (r"/api/auth/check", AuthCheckHandler),
    (r"/api/auth/list", AuthListHandler),
]