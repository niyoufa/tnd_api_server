# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-06-07
#

from dhuicredit.handler import APIHandler
import dhuicredit.libs.utils as utils
import os
import commands

class SystemOperationHandler(APIHandler):
    def get(self, *args, **kwargs):
        result = utils.init_response_data()
        method = self.get_argument("method",'')
        try:
            if method == 'deploy':
                # subprocess.call('sh /root/credit_deploy.sh',shell=True)
                (status, output) = commands.getstatusoutput('sh /root/credit_deploy.sh')
                result['data'] = output
                result['res'] = status
            if method == 'reset':
                # subprocess.call('sh /root/credit_deploy.sh',shell=True)
                (status, output) = commands.getstatusoutput('sh /root/credit_reset.sh')
                result['data'] = output
                result['res'] = status
        except StandardError,e:
            result = utils.reset_response_data(0,str(e))

        self.finish(result)

handlers = [(r'/api/system/operation', SystemOperationHandler),
            ]