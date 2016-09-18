# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-04-14
#

from suds.client import Client
from suds.transport.https import HttpAuthenticated
import pyDes
import base64

def encode(str):
    key = pyDes.des('12312312',pyDes.CBC, "12312312", pad=None,padmode=pyDes.PAD_PKCS5)
    des_data = key.encrypt(str)
    b_data = base64.b64encode(des_data)
    return b_data

def decode(secret):
    key = pyDes.des('12312312',pyDes.CBC, "12312312", pad=None,padmode=pyDes.PAD_PKCS5)
    b_secret = base64.b64decode(secret)
    des_secret = key.decrypt(b_secret)
    return des_secret

xml = '''
<?xml version="1.0" encoding="UTF-8"?>
<REQ>
<SIGN>
<USERNAME>test</USERNAME>
<PASSWORD>12345</PASSWORD>
</SIGN>
<PARMAS>
<KEY>320582199002057914</KEY>
</PARMAS>
</REQ>
'''

t = HttpAuthenticated(username='test',password='123')
test = Client('http://139.159.35.187:8080/eis/webService/BizInvestService?wsdl')

str = encode(xml)
print str
secret = test.service.postPersingleGr(str)
print decode(secret)
