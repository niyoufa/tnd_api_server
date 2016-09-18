# -*- coding: utf-8 -*-

"""
    author : youfaNi
    date : 2016-08-22
"""

import json,pdb
import oauth2
import datetime
import tornado
import urllib
from tnd_api_server.handler import TokenAPIHandler
from tnd_api_server.handler import APIHandler
from tnd_api_server.app import get_options
import tnd_api_server.libs.utils as utils
import tnd_api_server.model.link as link_model
options = get_options()

class LinkListCreateHandler(APIHandler):
    model = link_model.LinkModel()

    def get(self):
        result = utils.init_response_data()
        try:
            type = self.get_argument("type","all")
            page = self.get_argument("page",1)
            page_size = self.get_argument("page_size",10)
            keyword = self.get_argument("keyword","")
            objs, pager = LinkListCreateHandler.model.search_list(type=type,page=page,page_size=page_size,keyword=keyword)
        except Exception,e:
            result = utils.reset_response_data(0, str(e))
            self.finish(result)
            return

        result["data"] = objs
        result["pager"] = pager
        self.finish(result)

    def post(self):
        result = utils.init_response_data()
        try:
            pass
        except Exception,e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

class LinkRetrieveUpdateDestroyHandler(APIHandler):
    def get(self):
        result = utils.init_response_data()
        try:
            id = self.get_argument("id")
            _id = utils.create_objectid(id)
            ret = LinkListCreateHandler.model.search({"_id":_id})
            if ret :
                result["data"] = ret
            else:
                result["data"] = {}
        except Exception,e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

    def put(self):
        result = utils.init_response_data()
        try:
            pass
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

    def delete(self):
        result = utils.init_response_data()
        try:
            ids = json.loads(self.get_argument("ids"))
            _ids = [utils.create_objectid(id) for id in ids]
            for _id in _ids:
                LinkListCreateHandler.model.delete(_id=_id)
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)


handlers = [
    (r"/api/link/list", LinkListCreateHandler),
    (r"/api/link", LinkRetrieveUpdateDestroyHandler),
]