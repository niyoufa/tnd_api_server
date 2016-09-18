# -*- coding: utf-8 -*-

"""
    author : youfaNi
    date : 2016-07-13
"""

from bson.son import SON
from dhuicredit.app import get_options
import dhuicredit.model.model as model
import dhuicredit.model.mongo as mongo
import dhuicredit.consts as consts
import dhuicredit.libs.utils as utils

class OauthModel(model.BaseModel,model.Singleton):
    __name = "dhuicredit.oauth_clients"

    def __init__(self):
        model.BaseModel.__init__(self,OauthModel.__name)