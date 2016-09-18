import time
import tornado.web

class NoticeAddHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin/notice/notice_add.html')

handlers = [
    (r'/admin/notice/add',NoticeAddHandler)
]