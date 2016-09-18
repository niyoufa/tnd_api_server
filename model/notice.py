# -*- coding:utf-8 -*-

import dhuicredit.model.model as model
import dhuicredit.libs.utils as utils

class NoticeModle(model.BaseModel,model.Singleton):
    __name = "dhuicredit.notice"

    def __init__(self):
        model.BaseModel.__init__(self,NoticeModle.__name)

    def find_one_by_id(self,notice_id=None):
        notice_coll = self.get_coll()
        if notice_id:
            notice = notice_coll.find_one({"_id":utils.create_objectid(notice_id)})
        return notice
            