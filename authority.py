# -*- coding: utf-8 -*-

"""
    author : youfaNi
    date : 2016-07-18
"""

import pdb
import tornado
from dhuicredit.app import get_options
from dhuicredit.urls import handlers
import dhuicredit.model.model as model
import dhuicredit.model.mongo as mongo
import dhuicredit.consts as consts
import dhuicredit.libs.utils as utils
from bson.son import SON

class AuthorityModel(model.BaseModel,model.Singleton):
    __name = "dhuicredit.authority"
    help = "用户权限管理"

    def __init__(self):
        model.BaseModel.__init__(self,AuthorityModel.__name)
        self.scope_manifest = [
            ("default",("font-api",["font-api"])),
            ("all",("font-api",["font-api","back-api","system-api"])),
        ]
        self.scope_api_dict = {
            "font-api":[
                "/api/user",
            ]
        }

    def parse(self):
        pass

    def process(self,request,access):
        request_path = request.path
        scopes = access["scopes"]
        available_api_list = self.get_scopes_api_list(scopes)
        if request_path in available_api_list or "font-api" in scopes:
            pass
        else:
            raise Exception("访问受限")

    def get_scopes(self):
        scope_manifest = self.scope_manifest
        scopes = {}
        for scope in self.scope_manifest:
            scopes[scope[0]] = scope[1]
        return scopes

    def get_api_list(self):
        global handlers
        api_list = []
        for handler in handlers:
            if isinstance(handler,tornado.web.URLSpec):
                api_list.append(handler._path)
            else:
                api_list.append(handler[0])
        return api_list

    def get_scopes_api_list(self,scopes):
        api_list = []
        for scope in scopes:
            if self.scope_api_dict.has_key(scope):
                api_list.extend(self.scope_api_dict[scope])
        return list(set(api_list))

authority = AuthorityModel()