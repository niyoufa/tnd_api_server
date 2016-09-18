#-*- coding: utf8 -*-

from dhuicredit.handler import APIHandler
import dhuicredit.libs.utils as utils
import dhuicredit.model.notice as notice_model


class NoticeHandler(APIHandler):
    def post(self):
        result = utils.init_response_data()
        try:
            notice_model_obj = notice_model.NoticeModle()
            notice_coll = notice_model_obj.get_coll()

            notice_title = self.get_argument("notice_title")
            notice_context = self.get_argument("notice_context")
            editor_name = self.get_argument("editor_name")
            editor_id = self.get_argument("editor_id")
            notice_type = self.get_argument("notice_type")
            notice=({
                "notice_title":notice_title,
                "notice_context":notice_context,
                "add_time":utils.get_current_time(),
                "edit_time":utils.get_current_time(),
                "editor_name":editor_name,
                "editor_id":editor_id,
                "notice_type":notice_type,
            })
            notice_coll.insert_one(notice)
            notice["notice_id"]=utils.objectid_str(notice["_id"])
            notice_coll.save(notice)

            # result={"success":1,"data":utils.JsonEncode(notice_coll[0])}
        except Exception,e:
            result = utils.reset_response_data(0,str(e))

        self.finish(result)

    def put(self):
        try:
            notice_model_obj = notice_model.NoticeModle()
            notice_coll = notice_model_obj.get_coll()

            notice_title = self.get_argument("notice_title")
            notice_context = self.get_argument("notice_context")
            notice_type = self.get_argument("notice_type")
            notice_id = self.get_argument("notice_id")
            notice = notice_coll.find_one({"notice_id":notice_id})
            if notice == None:
                raise ValueError(u"无此公告")
            else:
                notice["notice_title"]=notice_title
                notice["notice_context"]=notice_context
                notice["notice_type"]=notice_type
                notice["edit_time"]=utils.get_current_time()
                notice_coll.save(notice)
                result={"success":1,"data":utils.JsonEncode(notice)}
        except Exception,e:
            result = utils.reset_response_data(0,str(e))

        self.finish(result)

    def delete(self):
        try:
            notice_model_obj = notice_model.NoticeModle()
            notice_coll = notice_model_obj.get_coll()
            notice_id = self.get_argument("notice_id")
            notice = notice_coll.find_one({"notice_id":notice_id})
            if notice == None:
                raise  ValueError(u"无此公告")
            notice_coll.remove(notice)
            result={"success":1,"data":utils.JsonEncode(notice)}
        except Exception,e:
            result = utils.reset_response_data(0,str(e))
        self.finish(result)

    def get(self):
        try:
            notice_model_obj = notice_model.NoticeModle()
            notice_coll = notice_model_obj.get_coll()
            notice = notice_coll.find({}).sort("edit_time",-1)
            if not notice or notice.count()==0:
                raise ValueError(u"无此公告")
            result={"success":1,"data":utils.JsonEncode(notice)}
        except Exception,e:
            result = utils.reset_response_data(0,str(e))
        self.finish(result)




handlers = [
    (r"/api/notice",NoticeHandler)
]

