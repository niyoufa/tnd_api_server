# -*- coding: utf-8 -*-

"""
    alter by: youfaNi
    alter on 2016-07-13
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
import dhuicredit.model.mongo as mongo
import dhuicredit.model.user as user_model
import dhuicredit.model.oauth as oauth_model
import dhuicredit.model.checkcode as checkcode_model
import dhuicredit.handlers.oauth as oauth

options = get_options()

class UserSignUpHandler(APIHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        result = utils.init_response_data()
        try:
            user_model_obj = user_model.UserModel()
            user_coll = user_model_obj.get_coll()
            oauth_model_obj = oauth_model.OauthModel()
            oauth_coll = oauth_model_obj.get_coll()
            checkcode_model_obj = checkcode_model.CheckCode()
            checkcode_coll = checkcode_model_obj.get_coll()

            mobile = self.get_argument("mobile")
            mobile_code = self.get_argument("mobile_code")
            password = self.get_argument("password")
            re_password = self.get_argument("re_password")
            email = self.get_argument("email")
            email_code = self.get_argument("email_code")
            invitation_code = self.get_argument("invitation_code")

            if mobile == "":
                raise Exception("请输入手机号!")
            elif user_coll.find_one({'mobile': mobile}):
                raise Exception("手机号已注册用户！")
            elif mobile_code == "":
                raise Exception("请输入手机验证码")
            elif password == "":
                raise Exception("请输入密码!")
            elif re_password == "":
                raise Exception("请确认密码！")
            elif password != re_password:
                raise Exception("两次密码输入不一致！")
            elif email == "":
                raise Exception("请输入邮箱！")
            elif user_coll.find_one({"email":email}):
                raise Exception("邮箱已注册用户")
            elif email_code == "":
                raise Exception("请输入邮箱验证码")
            invitation_mobile = ""
            if invitation_code != "" and invitation_code != "undefined":
                invitator = user_coll.find_one({
                    "mobile":invitation_code,
                })
                if not invitator:
                    raise Exception("邀请人不存在")
                else :
                    invitation_mobile = invitator["mobile"]

            # 检查手机验证码
            utils.check_code(checkcode_coll, mobile, mobile_code)
            # 检查邮箱验证码
            utils.check_code(checkcode_coll, email, email_code, type="email")

            create_date = datetime.datetime.now()
            write_date =""
            login_date = ""
            headimgurl = ""
            nickname = ""
            active = 0
            sex = 0
            city = ""
            address = ""
            privilege = 0
            province = ""

            user_coll.insert_one({
                'mobile':mobile,
                'password':password,
                'email':email,
                'invitation_mobile':invitation_mobile,
                'create_date':create_date,
                'write_date':write_date,
                'login_date':login_date,
                'headimgurl':headimgurl,
                'nickname':nickname,
                'active':active,
                'sex':sex,
                'city':city,
                'address':address,
                'privilege':privilege,
                'province':province,
            })
            oauth_coll.insert_one({'identifier': mobile,
                             'secret': password,
                             'redirect_uris': [],
                             'authorized_grants': [oauth2.grant.ClientCredentialsGrant.grant_type]})

            params = {
                'login': mobile,
                'password': password,
            }
            body = urllib.urlencode(params)
            client = tornado.httpclient.AsyncHTTPClient()
            response = yield tornado.gen.Task(
                client.fetch,
                options.server_addr + "/api/user/signin",
                method='POST',
                body=body)
            response_body = json.loads(response.body)
            if response_body.has_key("error"):
                result = utils.reset_response_data(0,response_body["error"] + response_body["error_description"])
                self.finish(result)
                return

            result["data"] = response_body["response"]["data"]
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

class UserSignInHandler(APIHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        result = utils.init_response_data()
        user_model_obj = user_model.UserModel()
        user_coll = user_model_obj.get_coll()
        try:
            login = self.get_argument("login")
            password = self.get_argument("password")
            if login == "":
                raise Exception("请输入用户名!")
            elif user_coll.find({"mobile":login}).count() == 0 \
                              and user_coll.find({"email":login}).count() == 0:
                raise Exception("手机或邮箱不存在！")
            elif password == "":
                raise Exception("请输入密码!")

            user = user_coll.find_one({"mobile":login}) or user_coll.find_one({"email":login})

            user["login_date"] = datetime.datetime.now()
            user_coll.save(user)

            params = {
                'client_id':user["mobile"],
                'client_secret':password,
                'grant_type':'client_credentials',
            }
            body = urllib.urlencode(params)
            client = tornado.httpclient.AsyncHTTPClient()
            response = yield tornado.gen.Task(
                client.fetch,
                  options.server_addr+"/token",
                  method='POST',
                  body=body)
            response_body = json.loads(response.body)
            try:
                access_token = response_body["access_token"]
            except Exception ,e:
                result = utils.reset_response_data(-1, str(e) + \
                                                   response_body["error"]+" "+\
                                                   response_body["error_description"]+\
                                                   " or password error!")
                self.finish(result)
                return
            user["_id"] = str(user["_id"])

            # 存储 token-uid
            user_model_obj.save_token_uid(access_token, user["_id"])

            user["create_date"] = str(user["create_date"]).split(".")[0]
            user["login_date"] = str(user["login_date"]).split(".")[0]
            del user["password"]
            result["data"] = user
            result["data"]["access_token"] = access_token
        except Exception, e:
            result = utils.reset_response_data(0, str(e))
        self.finish(result)


class UserHandler(TokenAPIHandler):
    def get(self):
        result = utils.init_response_data()
        user_model_obj = user_model.UserModel()
        user_coll = user_model_obj.get_coll()
        try:
            access_token = self.get_argument("access_token")
            uid = user_model_obj.get_token_uid(access_token)
            user = user_coll.find_one({'_id':utils.create_objectid(uid)})
            if user:
                user["_id"] = str(user["_id"])
                del user["password"]
                user = utils.dump(user)
                result["data"] = user
            else:
                try:
                    raise Exception(u"用户不存在")
                except Exception,e:
                    result = utils.reset_response_data(1, u"用户不存在")
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

class UserPasswordReBack(APIHandler):
    def post(self):
        result = utils.init_response_data()
        user_model_obj = user_model.UserModel()
        user_coll = user_model_obj.get_coll()
        checkcode_model_obj = checkcode_model.CheckCode()
        checkcode_coll = checkcode_model_obj.get_coll()
        db = mongo.get_database("oauth_clients")
        oauth_clients_coll = db["oauth_clients"]
        try:
            mobile = self.get_argument("mobile")
            mobile_code = self.get_argument("mobile_code")
            new_password = self.get_argument("new_password")
            re_new_password = self.get_argument("re_new_password")

            if mobile == "":
                raise Exception("请输入手机号!")
            elif user_coll.find({"mobile":mobile}).count() == 0:
                raise Exception("用户不存在")
            elif mobile_code == "":
                raise Exception("请输入手机验证码")
            elif new_password != re_new_password:
                raise Exception("两次输入的密码不一致")

            # 检查手机验证码
            utils.check_code(checkcode_coll, mobile, mobile_code)

            user = user_coll.find_one({"mobile":mobile})
            if not user :
                raise Exception("用户不存在")

            oauth_clients_obj = oauth_clients_coll.find_one({
                "secret": user["password"],
                "identifier":user["mobile"],
            })
            oauth_clients_obj["secret"] = new_password
            user["password"] = new_password
            oauth_clients_coll.save(oauth_clients_obj)
            user_coll.save(user)
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

class UserExistInfo(APIHandler):
    def get(self):
        result = utils.init_response_data()
        user_model_obj = user_model.UserModel()
        try:
            user_coll = user_model_obj.get_coll()
            mobile = self.get_argument("mobile")
            user = user_coll.find_one({
                "mobile":mobile,
            })
            if user_model_obj.is_exist(mobile) :
                result["data"]["is_exist"] = int(True)
            else:
                result["data"]["is_exist"] = int(False)
        except Exception,e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)


handlers = [
                (r"/api/user/signup", UserSignUpHandler),
                (r"/api/user/signin", UserSignInHandler),
                (r"/api/user", UserHandler,dict(provider=oauth.init_oauth())),
                (r"/api/user/password/reback", UserPasswordReBack),
                (r"/api/user/exist/info", UserExistInfo),
            ]
