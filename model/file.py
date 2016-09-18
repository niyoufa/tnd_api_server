# -*- coding: utf-8 -*-

"""
    alter by: daemon wnag
    alter on 2016-07-14
"""

from bson.son import SON
import dhuicredit.model.model as model
import dhuicredit.model.mongo as mongo
import dhuicredit.consts as consts
import dhuicredit.libs.utils as utils

class FileModel(model.BaseModel,model.Singleton):
    __name = "dhuicredit.file"

    def __init__(self):
        model.BaseModel.__init__(self,FileModel.__name)

    def query(self,query_dict,origin=False):
        query = dict([(k,v) for (k,v) in query_dict.items() if v != '' and v != 'undefined'])
        res = self.get_coll().find_one(query)
        if origin:
            return res
        else:
            return utils.dump(res)

    def create(self,**kwargs):
        params = ['file_name','file_type','file_path','file_sort']
        file_save = dict([(k,v) for (k,v) in kwargs.items() for p in params if k == p])
        file_save['add_time'] = utils.get_now()
        file_save['download_count'] = 0
        file_save['enable_flag'] = 1
        is_exist = self.get_coll().find({"file_path":file_save['file_path']}).count()
        if is_exist == 1:
            raise ValueError(u"该文件已经存在")
        self.get_coll().save(file_save)
        return file_save

    def list(self,file_type,json_encode=False):
        files = self.get_coll().find({"enable_flag":1,"file_type":file_type}).sort("file_sort",1)
        if json_encode:
            files = utils.dump(files)
        return files

    def upload(self,upload_path,file,file_type):
        '''
        :param upload_path: 上传路径
        :param file: self.request.files['file']的格式
        :return:
        '''
        import os
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

        file_metas=file
        if file_metas == '':
            raise ValueError(u"没有上传文件")
        for meta in file_metas:
            filename = str(utils.get_local_timestamp()) + meta['filename']
            filepath = os.path.join(upload_path,filename)
            #有些文件需要已二进制的形式存储，实际中可以更改
            with open(filepath,'wb') as up:
                up.write(meta['body'])
            self.create(**{
                "file_name":filename,
                "file_type":file_type,
                "file_path":filepath.split(utils.options.root_path)[1],
                "file_sort":0
            })

    def download(self,query_dict,user_id):
        file_download = FileDownloadModel()
        file_download.create(query_dict,user_id)

class FileDownloadModel(model.BaseModel,model.Singleton):
    __name = "dhuicredit.file_download"

    def __init__(self):
        model.BaseModel.__init__(self,FileDownloadModel.__name)

    def create(self,query_dict,user_id):
        file_model = FileModel()
        file = file_model.query(query_dict,True)
        if file is None:
            raise ValueError(u"文件不存在")
        file['download_count'] += 1
        file_model.get_coll().save(file)
        file_download = {
            "file_id":file['_id'],
            "file_name":file['file_name'],
            "file_path":file['file_path'],
            "download_time":utils.get_now(),
            "user_id":user_id
        }
        self.get_coll().save(file_download)



