# -*- coding: utf-8 -*-

"""
    author : youfaNi
    date : 2016-07-14
"""

import pdb
from dhuicredit.app import get_options
import dhuicredit.model.model as model
import dhuicredit.model.mongo as mongo
import dhuicredit.consts as consts
import dhuicredit.libs.utils as utils
from bson.son import SON

class CheckCode(model.BaseModel,model.Singleton):
    __name = "dhuicredit.checkcode"

    def __init__(self):
        model.BaseModel.__init__(self,CheckCode.__name)


