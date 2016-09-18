# -*- coding: utf-8 -*-
#
# @author: HuShuLong
# Created on 2016-07-18
#

import tornado.web
import dhuicredit.libs.utils as utils
import dhuicredit.model.image as image_model

class UploadImageHandler(tornado.web.RequestHandler):
    def check_xsrf_cookie(self):
        return True

    def get(self):
        pass

    def post(self):
        result = utils.init_response_data()
        image_model_obj = image_model.ImageModel()
        try:
            request_files = self.request.files
            if request_files.has_key("files"):
                files = request_files["files"]
            else:
                raise Exception("没有上传文件")
            data = image_model_obj.upload_image(files)
            result['data'] = data
        except Exception, e:
            result = utils.reset_response_data(0, str(e))
        self.finish(result)

handlers = [
    (r'/api/image',UploadImageHandler),
]



