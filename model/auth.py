# -*- coding: utf-8 -*-

"""
    author : youfaNi
    date : 2016-07-15
"""

import pdb
from dhuicredit.app import get_options
import dhuicredit.model.model as model
import dhuicredit.model.mongo as mongo
import dhuicredit.consts as consts
import dhuicredit.libs.utils as utils
from bson.son import SON

class AuthModel(model.BaseModel,model.Singleton):
    __name = "dhuicredit.auth"

    def __init__(self):
        model.BaseModel.__init__(self,AuthModel.__name)

    def check_format(self,id_card):
        id_card = id_card[0:-1]
        identity_card = IdentityCard()
        return identity_card.check(id_card)

    def check_validate(self,id_card):
        identity_card = IdentityCard()
        return identity_card.calculate(id_card)

#身份验证
class IdentityCard(model.Singleton):
    def __init__( self ):
        self.__Wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        self.__Ti = ['1', '0', 'x', '9', '8', '7', '6', '5', '4', '3', '2']
    def check( self, code ):
        if (len(code) != 17):
            print "必须为17位的字符"
            return False
        return True

    def calculate( self, code ):
        sum = 0
        for i in range(17):
            sum += int(code[i])*self.__Wi[i]
        return self.__Ti[sum%11] == code[-1]