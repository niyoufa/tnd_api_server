# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-07-14
#
from dhuicredit.handler import APIHandler
import dhuicredit.libs.utils as utils
import dhuicredit.model.model as model
import dhuicredit.model.file as file_model
import tornado.web
import os

options = utils.options

class FileDownloadHandler(tornado.web.RequestHandler):
    #文件下载
    def get(self):
        options = utils.options

        file_query = {}
        file_query['file_name'] = self.get_argument("file_name",'')
        # file_query['file_num'] = self.get_argument("file_num",'')
        file_query['file_path'] = self.get_argument("file_path",'')
        user_id = self.get_argument("user_id",'')

        query = dict([(k,v) for (k,v) in file_query.items() if v != '' and v != 'undefined'])
        query['enable_flag'] = 1

        fileModel = file_model.FileModel()
        res = fileModel.get_coll().find_one(query)

        fileModel.download(file_query,user_id)

        url = options.root_path + res['file_path']
        # url = os.path.join(options.file_download_store_url,file_path)

        filename = os.path.split(url)[1]
        self.set_header ('Content-Type', 'application/octet-stream')
        self.set_header ('Content-Disposition', 'attachment; filename='+filename)
        with open(url, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.write(data)
        self.finish()

class FileHandler(APIHandler):
    coll = ''
    model = ''

    def initialize(self):
        self.model = file_model.FileModel()
        self.coll = self.model.get_coll()

    #文件信息
    def get(self):
        result = utils.init_response_data()
        file_query = {}
        try:
            file_query['file_name'] = self.get_argument("file_name",'')
            file_query['file_num'] = self.get_argument("file_num",'')
            file_query['file_path'] = self.get_argument("file_path",'')
            file_query['enable_flag'] = 1

            result["data"] = self.model.query(file_query)
        except StandardError,e:
            result = utils.reset_response_data(0,str(e))

        self.finish(result)

    #新建文件
    def post(self):
        result = utils.init_response_data()
        file_save = {}
        try:
            file_save['file_name'] = self.get_argument("file_name",'')
            file_save['file_num'] = self.get_argument("file_num",'')
            file_save['file_sort'] = int(self.get_argument("file_sort",0))
            file_save['file_path'] = self.get_argument("file_path",'')

            res = self.model.create(**file_save)
            result["data"] = utils.dump(res)
        except StandardError,e:
            result = utils.reset_response_data(0,str(e))

        self.finish(result)

    #删除文件
    def delete(self):
        pass

    #修改文件
    def put(self):
        pass

class FileListHandler(APIHandler):
    #获取文件列表
    def get(self):
        result = utils.init_response_data()
        file_type = self.get_argument("file_type",'')
        try:
            fileModel = file_model.FileModel()
            result['data'] = fileModel.list(file_type,True)
        except StandardError,e:
            result = utils.reset_response_data(0,str(e))

        self.finish(result)

# @tornado.web.stream_request_body
class FileUploadHandler(APIHandler):
    #上传文件接口
    def post(self):
        result = utils.init_response_data()
        try:
            file_type = self.get_argument("file_type",'normal')
            upload_path=options.file_download_store_url+"%s/download/"%file_type
            file = self.request.files['file']

            fileModel = file_model.FileModel()
            fileModel.upload(upload_path,file,file_type)

        except StandardError,e:
            result = utils.reset_response_data(0,str(e))

        self.finish(result)

handlers = [(r'/api/file/download', FileDownloadHandler),
            (r'/api/file', FileHandler),
            (r'/api/file/list', FileListHandler),
            (r'/api/file/upload',FileUploadHandler)
            ]
