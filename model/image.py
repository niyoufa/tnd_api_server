# -*- coding: utf-8 -*-

"""
    alter by: HuShuLong
    alter on 2016-07-19
"""
import hashlib
import mimetypes
import os
from cStringIO import StringIO
import dhuicredit.libs.utils as utils
import time
from PIL import Image
import dhuicredit.model.model as model
from dhuicredit.libs import text_water_mark
from dhuicredit.libs.utils import get_root_path

allow_formats = set(['jpeg', 'png', 'gif'])
class ImageModel(model.BaseModel):
    __name = "dhuicredit.image"

    def __init__(self):
        model.BaseModel.__init__(self,ImageModel.__name)

    def check_image(self,files):

        for res in files:
            content = StringIO(res['body'])

            mime = Image.open(content).format.lower()
            if mime not in allow_formats:
                raise Exception("图片格式不正确！")

            if 'content_type' not in res or res['content_type'].find('/') < 1 or len(res['content_type']) > 128:
                raise Exception('文件类型错误')

            if 'filename' not in res or res['filename'] == '':
                raise Exception('文件名错误')

            if len(res['body']) > 4*1024*1024:
                raise Exception('上传图片不能大于4M')

    def upload_image(self,files):

        self.check_image(files)

        images_list = []
        for image_file in files:
            ets = mimetypes.guess_all_extensions(image_file['content_type'])
            ext = os.path.splitext(image_file['filename'])[1].lower()
            if ets and ext not in ets:
                ext = ets[0]

            md5 = hashlib.md5()
            md5.update(image_file['body'])
            key = md5.hexdigest()

            dir = ''
            url = '/static/www/upload/'
            name = time.strftime('%Y/%m/%d/')+ str(time.time()).replace('.','') + ext
            uri = get_root_path() + dir + url + name

            if not os.path.exists(os.path.dirname(uri)):
                os.makedirs(os.path.dirname(uri), mode=0777)

            with open(uri ,'wb') as f:

                im = Image.open(StringIO(image_file['body']))
                im_file = StringIO()
               # text_water_mark.text_watermark(im,'征信认证专用').save(im_file,format='png') #加水印
                im.save(im_file,format='png')
                im_data = im_file.getvalue()
                f.write(im_data)
                f.close()

            if image_file.has_key("upload_key"):
                upload_key = image_file["upload_key"]
            else:
                upload_key = "upload"

            image = {
                "file_hash":key,
                "file_base":dir,
                "file_path":url + name,
                "file_type":image_file['content_type'],
                "file_memo":image_file['filename'],
                "upload_key":upload_key,
                "file_ctms":time.time()
            }
            image_coll = self.get_coll()
            image_coll.insert_one(image)
            images_list.append(image)
        return utils.dump(images_list)