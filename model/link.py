# -*- coding:utf-8 -*-

import pdb,datetime

import tnd_api_server.model.model as model
import tnd_api_server.libs.utils as utils


class LinkModel(model.BaseModel,model.Singleton):
    __name = "newbie.link"

    def __init__(self):
        model.BaseModel.__init__(self,LinkModel.__name)

    def search_list(self,page=1,page_size=10,keyword="",type="all"):
        query_params = {}
        if type != "all":
            query_params.update({
                "type":type,
            })
        if keyword != "":
            query_params.update({
                "title": {
                    "$regex":keyword,
                },
            })
        coll = self.get_coll()
        length = coll.find(query_params).count()
        pager = utils.count_page(length, page, page_size)
        cr = coll.find(query_params).sort("create_date", -1).limit(pager['page_size']).skip(pager['skip'])
        objs = [utils.dump(obj) for obj in cr]
        return objs, pager