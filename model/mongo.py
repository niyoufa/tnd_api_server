#coding=utf-8

"""
    author : youfaNi
    date : 2016-07-13
"""

import pymongo, pdb
from tornado.options import options as settings

client = None

class DB_CONST :
    DB_NAME = "db_name"
    COLL_NAME = "coll_name"
    COLL_HOST = "host"
    COLL_PORT = "port"
    USERNAME = "username"
    PASSWORD = "password"
    COLL_TYPE = "coll_type"

class Collections :

    # MongoDB文档配置
    __COLLECTIONS = dict(

        user = dict(
            coll_name = "user",
            db_name = settings.mongo["database"],
            username=settings.mongo["user"],
            password=settings.mongo["password"],
            host=settings.mongo["host"],
            port=settings.mongo["port"],
        ),
        oauth_clients = dict(
            coll_name = "oauth_clients",
            db_name = settings.mongo["database"],
            username=settings.mongo["user"],
            password=settings.mongo["password"],
            host=settings.mongo["host"],
            port=settings.mongo["port"],
        ),
        checkcode = dict(
            coll_name="checkcode",
            db_name=settings.mongo["database"],
            username=settings.mongo["user"],
            password=settings.mongo["password"],
            host=settings.mongo["host"],
            port=settings.mongo["port"],
        ),
        file = dict(
                coll_name = "file",
                db_name = settings.mongo["database"],
                username=settings.mongo["user"],
                password=settings.mongo["password"],
                host=settings.mongo["host"],
                port=settings.mongo["port"],
        ),
        auth = dict(
            coll_name = "auth",
            db_name=settings.mongo["database"],
            username=settings.mongo["user"],
            password=settings.mongo["password"],
            host=settings.mongo["host"],
            port=settings.mongo["port"],
        ),

        notice = dict(
            coll_name = "notice",
            db_name = settings.mongo["database"],
            username = settings.mongo["user"],
            password = settings.mongo["password"],
            host = settings.mongo["host"],
            port = settings.mongo["port"],
        ),
        image = dict(
            coll_name = "image",
            db_name=settings.mongo["database"],
            username=settings.mongo["user"],
            password=settings.mongo["password"],
            host=settings.mongo["host"],
            port=settings.mongo["port"],
        ),
        file_download = dict(
            coll_name = "file_download",
            db_name=settings.mongo["database"],
            username=settings.mongo["user"],
            password=settings.mongo["password"],
            host=settings.mongo["host"],
            port=settings.mongo["port"],
        ),
        subject = dict(
            coll_name="subject",
            db_name=settings.mongo["database"],
            username=settings.mongo["user"],
            password=settings.mongo["password"],
            host=settings.mongo["host"],
            port=settings.mongo["port"],
        ),
        link=dict(
            coll_name="link",
            db_name=settings.mongo["database"],
            username=settings.mongo["user"],
            password=settings.mongo["password"],
            host=settings.mongo["host"],
            port=settings.mongo["port"],
        ),
    )

    @classmethod
    def get_db_name(cls,table_name) :
        if cls.__COLLECTIONS.has_key(table_name):
            db_name = cls.__COLLECTIONS[table_name][DB_CONST.DB_NAME]
        else :
            db_name = ""
        return db_name

    @classmethod
    def get_coll_name(cls,table_name) :
        if cls.__COLLECTIONS.has_key(table_name):
            coll_name = cls.__COLLECTIONS[table_name][DB_CONST.COLL_NAME]
        else :
            coll_name = ""
        return coll_name

    @classmethod
    def get_coll_host(cls,table_name) :
        if cls.__COLLECTIONS.has_key(table_name):
            coll_host = cls.__COLLECTIONS[table_name][DB_CONST.COLL_HOST]
        else :
            coll_host = ""
        return coll_host
   
    @classmethod
    def get_coll_port(cls,table_name) :
        if cls.__COLLECTIONS.has_key(table_name):
            coll_port = cls.__COLLECTIONS[table_name][DB_CONST.COLL_PORT]
        else :
            coll_port = ""
        return coll_port

    @classmethod
    def get_coll_username(cls,table_name) :
        if cls.__COLLECTIONS.has_key(table_name):
            username = cls.__COLLECTIONS[table_name][DB_CONST.USERNAME]
        else :
            username = ""
        return username

    @classmethod
    def get_coll_password(cls,table_name) :
        if cls.__COLLECTIONS.has_key(table_name):
            password = cls.__COLLECTIONS[table_name][DB_CONST.PASSWORD]
        else :
            password = ""
        return password

def get_client(table_name) :
    global client
    if client:
        return client
    else :
        host = Collections.get_coll_host(table_name)
        port = Collections.get_coll_port(table_name)
        client = pymongo.MongoClient(host,port)
        return client

def get_address(table_name):
    global client
    if client :
        address = client.address
    else :
        client = get_client(table_name)
        address = client.address
    return address

def get_db_names(table_name):
    global client
    if client :
        db_names = client.database_names()
    else :
        client = get_client(table_name)
        db_names = client.database_names()
    return db_names

def get_database(table_name,**kwargs) :
    global client
    if not client :
        client = get_client(table_name)
    db_name = Collections.get_db_name(table_name)
    db = client.get_database(db_name)
    return db

def drop_db(table_name,client=None) :
    if client == None :
        client = get_client(table_name)
    db_name = Collections.get_db_name(table_name)
    client.drop_database(db_name)
    print db_name + " dropped!"

def get_coll_names(table_name) :
    db = get_database(table_name)
    coll_names = db.collection_names(include_system_collections=False)
    return coll_names

# 获取mongodb collection Note: 此处需要做性能分析
def get_coll(table_name) :
    db_name = Collections.get_db_name(table_name)
    coll_name = Collections.get_coll_name(table_name)
    username = Collections.get_coll_username(table_name)
    password = Collections.get_coll_password(table_name)
    client = get_client(table_name)
    if db_name and coll_name :
        db = client[db_name]
        if not settings.debug:
            db.authenticate(username,password)
            coll = db[coll_name]
        else :
            coll = db[coll_name]
    else :
        coll = None
        print u"集合不存在!"
        return coll
    return coll

def get_coll_db_name(table_name) :
    db_name = Collections.get_db_name(table_name)
    return db_name

def drop_coll(table_name) :
    db_name = Collections.get_db_name(table_name)
    if db_name == "" :
        print u"集合不存在!"
    else :
        try :
            db = get_database(db_name)
        except Exception ,e :
            print u"查询数据库失败" + str(e)
            return
        db.drop_collection(table_name)
        print table_name + " dropped!"
