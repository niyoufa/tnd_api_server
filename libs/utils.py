# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-03-02
#


import os
import uuid
import random
import time
import datetime
import tnd_api_server.consts as consts
import json
import decimal
from bson.json_util import dumps,loads
from bson.objectid import ObjectId
import pymongo
import traceback
import string
import hashlib
import urllib
import xlrd
from tornado.options import options
import re
import HTMLParser
import cgi
import math
import requests
import redis
import tnd_api_server.libs.hash as hash
from tornado.httpclient import HTTPRequest
import zipfile
from concurrent import futures
import pdb
import logging

def get_root_path():
    return options.root_path

def find_modules(modules_dir):
    try:
        return [f[:-3] for f in os.listdir(modules_dir)
                if not f.startswith('_') and f.endswith('.py')]
    except OSError:
        return []

def get_order_id(origin_code=consts.ORIGIN_CODE['WEIZHAN'][0]):
    db = MongoDB()
    order_id = random.randint(10000000,99999999)
    while(db.order.find_one({"order_id":order_id}) is not None):
        order_id = random.randint(10000000,99999999)
    return origin_code+str(order_id)

def get_random_num(length,mode='string'):
    if mode == 'string':
        return ''.join([(string.ascii_letters+string.digits)[x] for x in random.sample(range(0,62),length)])
    elif mode == 'number':
        return ''.join([(string.digits)[x] for x in random.sample(range(0,10),length)])

def md5(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

def get_current_time(format_type='datetime'):
    if format_type == 'datetime':
        format = '%Y-%m-%d %H:%M:%S'
    elif format_type == 'date':
        format = '%Y-%m-%d'
    elif format_type == 'datetime2':
        format = '%Y-%m-%d %H:%M:%S.%f'
        return datetime.datetime.now().strftime(format)[:-3]
    return datetime.datetime.now().strftime(format)

def firstDayOfMonth(dt):
     return (dt+datetime.timedelta(days=-dt.day+1)).replace(hour=0,minute=0,second=0,microsecond=0)


def string_datenum(string,type='default'):
    if type == 'default':
        return int(string.replace(".",'').replace(':','').replace('-','').replace(' ',''))
    elif type == 'time':
        return int(string.replace(".",'').replace(':','').replace('-','').replace(' ','')[8:])
# get the post arguments as data way
# Victor CHENG
# 2016-01-12
def get_dhuicredit_argument(request_body, key):
    return eval(request_body.request.body)[key]

#规范sql返回的列表，使其能json序列化
def json_format_sql(lists):
    _list = []
    for list in lists:
        _l = {}
        for (k,v) in list.items():
            if isinstance(v,decimal.Decimal):
                _l[k] = str(v)
            else:
                _l[k] = v
        _list.append(_l)
    return _list

def timestamp_datetime(value,format_type='datetime'):
    if format_type == 'datetime':
        format = '%Y-%m-%d %H:%M:%S'
    elif format_type == 'date':
        format = '%Y-%m-%d'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = value + 8*60*60
    value = time.localtime(value)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt

def datetime_timestamp(dt):
     #dt为字符串
     #中间过程，一般都需要将字符串转化为时间数组
     try:
         time.strptime(dt, '%Y-%m-%d %H:%M:%S')
         ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
         #将"2012-03-28 06:53:40"转化为时间戳
         s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
     except ValueError:
         time.strptime(dt, '%Y-%m-%d')
         ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
         #将"2012-03-28 06:53:40"转化为时间戳
         s = time.mktime(time.strptime(dt, '%Y-%m-%d'))
     return int(s)

#获取UTC unix时间戳
def get_current_timestamp():
    return int(time.time()) - consts.TIME_ZONE_BEIJING*60*60

#获取本地时间戳
def get_local_timestamp(type='sec'):
    return int(time.time())

#获取当前utc时间
def get_utc_now():
    return datetime.datetime.utcnow()

#获取当前时间
def get_now():
    return datetime.datetime.now()

#sql生成器
def sql_generate(columns,type=' and ',connector=' and '):
    _sql = ''
    for (k,v) in columns.items():
        if v == '':
            sql = " "
        else:
            sql = " %s = '%s' %s "%(k,v,connector)
        _sql = _sql + sql
    if _sql.strip() == '':
        return ''
    else:
        sql = type+ _sql.rstrip('%s '%connector)
        return sql

#去除_id字段 或者转换_id为字符串形式
def JsonEncode(str,transform=False):
    if isinstance(str,pymongo.cursor.Cursor) or isinstance(str,list) or isinstance(str,pymongo.command_cursor.CommandCursor):
        result = []
        for s in str:
            if s.has_key('_id'):
                if transform == False:
                    del s['_id']
                else:
                    try:
                        s['_id'] = json.loads(dumps(s['_id']))['$oid']
                    except StandardError:
                        pass
            result.append(s)
    elif isinstance(str,dict):
        if str.has_key('_id'):
            if transform == False:
                del str['_id']
            else:
                try:
                    str['_id'] = json.loads(dumps(str['_id']))['$oid']
                except StandardError:
                    pass

        result = str
    elif str is None:
        result = None
    elif len(str) == 0:
        result = str
    return result

#根据状态的value值获取其描述
def get_status_from_value(dict,value,desc=1):
    return consts.get_status_from_value(dict,value,desc)

#获取consts的参数值
def get_consts(dict,key,index=0):
    return consts.get_consts(dict,key,index)

#日期操作
def date_operator(date,timedelta,type='datetime'):
    timestamp = datetime_timestamp(date)
    date_time = datetime.datetime.fromtimestamp(timestamp)
    days = int(timedelta)

    if type == 'datetime':
        new_date = datetime.date.strftime((date_time + datetime.timedelta(days=days)), '%Y-%m-%d %H:%M:%S')
    else:
        day = date_time.date()
        new_date = datetime.date.strftime((date_time + datetime.timedelta(days=days)).date(), '%Y-%m-%d')
    return new_date

#生成objectid
def create_objectid(str=None):
    try:
        object_id = ObjectId(str)
    except:
        object_id = ''
    return object_id

#比较函数
def compare(var1,var2,operate):
    var1 = float(var1)
    var2 = float(var2)
    operate = str(operate).upper()
    #大于等于
    if operate == 'GTE':
        result = var1 >= var2
    #大于
    elif operate == 'GT':
        result = var1 > var2
    #等于
    elif operate == 'EQ':
        result = var1 == var2
    #不等于
    elif operate == 'NE':
        result = var1 != var2
    #小于
    elif operate == 'LT':
        result = var1 < var2
    #小于等于
    elif operate == 'LTE':
        result = var1 <= var2
    return result

#将objectid 转换为string字符串
def objectid_str(objectid):
    return  json.loads(dumps(objectid))['$oid']

#获取一个可空的输入参数
def get_params(obj,key):
    result = obj.get_arguments(key)
    if len(result) == 0:
        result = ''
    else:
        result = result[0]
    return result

#格式化错误信息
def format_error():
    return traceback.format_exc()

#URL字符串格式解码
def urldecode(query):
    def str_format(string):
        return urllib.unquote(string).decode("utf-8")
    d = {}
    a = query.split('&')
    for s in a:
        if s.find('='):
            k,v = map(str_format, s.split('='))
            try:
                d[k].append(v)
            except KeyError:
                d[k] = v

    return d

#excel 读取操作
def open_excel(template_path):
    try:
        data = xlrd.open_workbook(template_path)
        return data
    except Exception,e:
        print str(e)

#excel 读取日期
def excel_date_format(cell,type='date'):
    def date_format(value):
        if value > 1000:
            return str(value)
        if value < 10:
            return '0'+str(value)
        else:
            return str(value)
    if type == 'date':
        return date_format(xlrd.xldate_as_tuple(cell,0)[0])+'-'+date_format(xlrd.xldate_as_tuple(cell,0)[1])+'-'+date_format(xlrd.xldate_as_tuple(cell,0)[2])
    elif type == 'datetime':
        return date_format(xlrd.xldate_as_tuple(cell,0)[0])+'-'+date_format(xlrd.xldate_as_tuple(cell,0)[1])+'-'+date_format(xlrd.xldate_as_tuple(cell,0)[2])+' '+date_format(xlrd.xldate_as_tuple(cell,0)[3])+':'+date_format(xlrd.xldate_as_tuple(cell,0)[4])+':'+date_format(xlrd.xldate_as_tuple(cell,0)[5])
#验证字段是否为空
def validate_none(**kwargs):
    try:
        for (k,v) in kwargs.items():
            if v is None:
                raise ValueError(u"%s is null"%k)
        return {"success":1,"return_code":"success"}
    except ValueError,e:
        return {"success":0,"return_code":str(e)}

#生成唯一id
def generate_id():
    return ObjectId()

#转化时间为数组
def date_array(str):
    try:
        result = time.strptime(str, "%Y-%m-%d %H:%M:%S")
    except StandardError,e:
        result = time.strptime(str, "%Y-%m-%d")
    return result

def array_keyto(ary, key):
    ret = {}
    for val in ary:
        ret[val[key]] = val
    return ret

def array_group(ary, key):
    ret = {}
    for val in ary:
        if val[key] not in ret:
            ret[val[key]] = []
        ret[val[key]].append(val)
    return ret

def array_field(ary, key):
    ret = []
    for val in ary:
        ret.append(val[key])
    return ret

def build_links(val, opt = ' target="_blank"'):
    exp = re.compile(
            r'('
            r'(?:http|ftp)s?://'           # http:// or https://
            r'[a-z0-9-]+(?:\.[a-z0-9-]+)*' # domain or ip...
            r'(?::\d+)?'                   # optional port
            r'(?:/[^"\'<>\s]*)?'           # optional segs
            r')', re.IGNORECASE)
    return exp.sub(r'<a href="\1"' + opt + r'>\1</a>', val)

def str_md5_hex(val):
    return hashlib.md5(val).hexdigest()

def html_decode(html):
    html_parser = HTMLParser.HTMLParser()
    return html_parser.unescape(html)

def html_encode(str):
    return cgi.escape(str)

#计算分页信息
def count_page(length,page,page_size=options.page_size,page_show=options.page_show):
    page = int(page)
    length = int(length)
    if length == 0:
        return {"enable":False,
                "page_size":page_size,
                "skip":0}
    max_page = int(math.ceil(float(length)/page_size))
    #pages_num = math.ceil(max_page/page_show)
    page_num = int(math.ceil(float(page)/page_show))
    pages = range(1,max_page+1)[((page_num-1)*page_show):(page_num*page_show)]
    skip = (page-1)*page_size
    if page >= max_page:
        has_more = False
    else:
        has_more = True
    pager={
        "page_size":page_size,
        "max_page":max_page,
        "pages":pages,
        "page_num":page_num,
        "skip":skip,
        "page":page,
        "enable":True,
        "has_more":has_more
    }
    return pager

#判断点是否在多边形内
def point_in_poly(x,y,poly):
    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

#将两个list合成字典
def list_to_dict(list1,list2):
    return dict(zip(list1[::],list2))

#发送短信
def send_msg(mobile,content):
    params = {
        "sn":"SDK-MDQ-010-00148",
        "pwd":"9FFF3D8BBCB323D89D4F24577256ABD0",
        "mobile":mobile,
        "content":content,
        "ext":16,
        "stime":"",
        "rrid":"",
        "msgfmt":""
    }

    url = "http://sdk.entinfo.cn:8061/mdsmssend.ashx"

    requests.get(url,params=params)

#生成签名
def make_sign(params):
    return hash.sign_encode(params)

#验证后台时间戳以及签名以及host
def validate_sign(id,timestamp,sign,host):
    try:
        if timestamp == '':
            raise ValueError(u"缺失时间戳")

        if get_local_timestamp() - int(timestamp) > 20*60:
            raise ValueError(u"此次请求已失效")

        if get_local_timestamp() < int(timestamp):
            raise ValueError(u"本地时间错误")

        host = host.replace("com",'').replace("www",'').replace("cn",'').replace(".",'')
        if host != options['host']:
            raise ValueError(u"请求主机错误")

        local_params = {
            "id":id,
            "timestamp":timestamp
        }
        local_sign = make_sign(urllib.urlencode(local_params))

        if local_sign != sign:
            raise ValueError('签名错误')
        result = {"success":1,"data":True,"return_code":"success"}
    except StandardError,e:
        result = {"success":0,"return_msg":format_error(),"return_code":str(e)}

    return result

#获取请求Host
def get_request_host(request):
    return request.headers.get_list('HOST')[0]
#获取请求Cookie头中的version
def get_version(request):
    cookies = request.headers.get_list('Set-Cookie')
    version = ''
    if len(cookies) != 0:
        for c in cookies:
            iters = c.split('=')
            if iters[0] == 'version':
                version = iters[1]
    return version

#计算token值
def get_token(body):
    import binascii
    secrect = "4Nyuzf2ILtElSH"
    body = "b=1&a=2&c=3"
    param_list = body.split("&")
    param_list.sort()
    body = "".join(param_list)
    body += secrect
    body = md5(body)
    body = binascii.b2a_hex(body)
    token = hashlib.sha1(body).hexdigest()
    return "admin" , token

#添加token
def add_token(func):
    def add_token_func(self,*args,**kwargs) :
        request = args[1]
        #添加token信息
        source , token = get_token(request.body)
        token_info = dict(
            source = source ,
            token = token ,
        )
        request.body += urllib.urlencode(token_info)
        func(self,*args,**kwargs)
    return add_token_func

#把object对象转化为可json序列化的字典
def convert_to_dict(obj):
    dic = {}
    if not isinstance(obj, dict):
        dic.update(obj.__dict__)
    else:
        dic = obj
    for key,value in dic.items():
        if isinstance(value,datetime.datetime):
            dic[key] = str(value)
        elif key[0] == '_':
            dic.pop(key)

    return dic


def get(url,params):
    req = HTTPRequest(url=url+'?'+params,method="GET")
    return req

def post(url,params):
    req = HTTPRequest(url=url,method="POST",headers={'Content-Type':'application/x-www-form-urlencoded'},body=params)
    return req

def zip_folder(foldername, zip_name):
    zip = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED )
    current_path = os.getcwd()
    os.chdir(foldername)
    for f in os.listdir(foldername):
        zip.write(f)
    os.chdir(current_path)
    zip.close()

def format_print_string(string,size):
    s = 0
    str_array = []
    _string = ''
    for l in list(string):
        if l >= '0' and l <= '9':
            s = s + 9
        elif l >= 'a' and l <= 'z':
            s = s + 9
        elif l >= 'A' and l <= 'Z':
            s = s + 11
        elif l >= ' ' and l <= '~':
            s = s + 4
        else:
            # if l >= u'\u4e00' and l <= u'\u9fa5':
            #     print u'中文'+l
            s = s + 15
        _string = _string + l
        if s >= size:
            str_array.append(_string)
            s = 0
            _string = ''
    if _string != '':
        str_array.append(_string)

    return str_array

def get_concurrent_pool():
    return futures.ThreadPoolExecutor(4)

# move by niyoufa
# move from app.py on 2016.07.13

def write_log(type,content):
    logging.config.fileConfig(os.path.join(options.root_path, "logging.config"))
    logger = logging.getLogger(type)
    logger.debug(content)

def MongoDB():
    #建立连接
    client  = pymongo.MongoClient(options.mongo["host"],options.mongo["port"])
    db = client[options.mongo["database"]]
    if not options.debug:
        db.authenticate(options.mongo["user"],options.mongo["password"])
    return db

def Redis():
    pool = redis.ConnectionPool(host=options.redis['host'],
                             port=options.redis['port'],
                             db=options.redis['db'])
    db = redis.StrictRedis(connection_pool=pool)
    return db

def init_response_data():
    result = {"success":1,"return_code":"success","error_msg":"","data":{}}
    return result

def reset_response_data(code,e=None):
    print format_error()
    result = init_response_data()
    if code == 1:
        result["return_code"] = "success"
    elif code == -1:
        result["return_code"] = "token invalidate"
    else :
        result["return_code"] = e or "error"
    result["success"] = code
    result["error_msg"] = format_error()

    return result

def dump(str):
    result = None
    if isinstance(str,pymongo.cursor.Cursor) or isinstance(str,list) or isinstance(str,pymongo.command_cursor.CommandCursor):
        result = []
        for _s in str:
            if type(_s) == type({}):
                s = {}
                for (k,v) in _s.items():
                    if type(v) == type(ObjectId()):
                        s[k] = json.loads(dumps(v))['$oid']
                    elif type(v) == type(datetime.datetime.utcnow()):
                        s[k] = v.strftime("%Y-%m-%d %H:%M:%S.%f")
                    else:
                        s[k] = v
            else:
                s = _s
            result.append(s)
    elif isinstance(str,dict):
        for (k,v) in str.items():
            if type(v) == type(ObjectId()):
                str[k] = json.loads(dumps(v))['$oid']
            elif type(v) == type(datetime.datetime.utcnow()):
                str[k] = v.strftime("%Y-%m-%d %H:%M:%S.%f")
        result = str
    elif str is None:
        result = None
    elif len(str) == 0:
        result = str
    return result

def check_code(checkcode_coll,str,code,type="mobile"):
    if type == "mobile":
        checkcode = checkcode_coll.find_one({"mobile":str,"enable_flag":True})
        # 验证码的有效时间
        if checkcode:
            if code.upper() != checkcode["code"].upper():
                raise Exception("手机验证码错误！")
            elif checkcode["create_date"] <= datetime.datetime.now() - datetime.timedelta(minutes=30):
                raise Exception("手机验证码过期！")
            checkcode["enable_flag"] = False
            checkcode_coll.save(checkcode)
        else:
            raise Exception("获取手机验证码失败")
    elif type == "email":
        checkcode = checkcode_coll.find_one({"email": str,"enable_flag":True})
        if checkcode:
            if code.upper() != checkcode["code"].upper():
                raise Exception("邮箱验证码错误！")
            elif checkcode["create_date"] <= datetime.datetime.now() - datetime.timedelta(hours=30):
                raise Exception("邮箱验证码过期！")
            checkcode["enable_flag"] = False
            checkcode_coll.save(checkcode)
        else:
            raise Exception("获取邮箱验证码失败")
    else:
        raise Exception("验证码类型错误！")

    # TODO 发送验证码
