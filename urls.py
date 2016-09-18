# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-03-02
#


try:
    import importlib
except:
    from tnd_api_server.libs import importlib

import pdb
from tornado.options import options
from tornado.web import url
from tnd_api_server.handler import APIErrorHandler

handlers = []
ui_modules = {}

# the module names in handlers folder

# TODO 写一个函数自动获取该list值
handler_names = ["subject","link"]

handler_admin_names=[]

def _generate_handler_patterns(root_module, handler_names, prefix=options.app_url_prefix):
    for name in handler_names:
        module = importlib.import_module(".%s" % name, root_module)
        module_hanlders = getattr(module, "handlers", None)
        if module_hanlders:
            _handlers = []
            for handler in module_hanlders:
                try:
                    patten = r"%s%s" % (prefix, handler[0])
                    if len(handler) == 2:
                        _handlers.append((patten,
                                          handler[1]))
                    elif len(handler) == 3:
                        _handlers.append(url(patten,
                                             handler[1],
                                             {"provider":handler[2]})
                                         )
                    else:
                        pass
                except IndexError:
                    pass

            handlers.extend(_handlers)

_generate_handler_patterns("tnd_api_server.handlers", handler_names)
_generate_handler_patterns("tnd_api_server.handlers.admin", handler_admin_names)

# Override Tornado default ErrorHandler
handlers.append((r".*", APIErrorHandler))
