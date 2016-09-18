# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-03-02
#

from tornado.options import options

def get_status_from_value(dict,value,desc=1):
    for d,x in dict.items():
        if x[0] == value:
            return x[desc]

def get_consts(dict,key,index=0):
    return dict[key][index]

CATEGORY_AMERICAS = "Americas"
CATEGORY_EUROPE = "Europe"
CATEGORY_ASIA = "Asia"
CATEGORYS = (CATEGORY_AMERICAS, CATEGORY_EUROPE, CATEGORY_ASIA)

SUBSCRIBE_STATUS_ON = "on"
SUBSCRIBE_STATUS_OFF = "off"

###订单状态

ORDER_STATUS = {
    #待支付 等待付款
    'WAITING_PAYMENT':[0,'待支付'],
    #服务中 正常状态
    'NORMAL':[1,'服务中'],
    #已取消
    'CANCELED':[2,'已取消'],
    #已完成
    'COMPLETED':[3,'已完成'],
    #退款中
    'REFUNDING':[4,'退款中'],
    #已关闭
    'CLOSED':[5,'已关闭'],
    #一元夺宝已中奖
    'INDIANA_WINNER':[6,'已中奖'],
    #一元夺宝未中奖
    'INDIANA_LOSER':[7,'未中奖']
}

###发货状态
SHIPPING_STATUS = {
    #未发货
    'WAITING':[1,'未发货'],
    #已发货 进行中
    'PROCESSING':[10,'进行中'],
    #已完成
    'COMPLETED':[20,'已完成'],
    #已取消
    'CANCELED':[30,'已取消']
}

###支付方式
PAY_NAME = {
    #微信支付
    'WEIXIN':["weixin",'微信支付'],
    #支付宝支付
    'ALIPAY':["alipay",'支付宝支付']
}

###支付状态
PAY_STATUS = {
    #未支付
    "WAITING":[1,"未支付"],
    #已支付
    'PAYED':[2,'已支付'],
    #货到付款
    'COD':[3,'东汇豆支付'],
    #东汇豆支付
    'DHUIDOU':[4,'东汇豆支付'],
    #部分支付
    'PART':[5,'部分支付']
}

###来源
ORIGIN_CODE = {
    #微站（自己开发的）
    'WEIZHAN':['WZ','微站'],
    #有赞
    'YOUZAN':['YZ','有赞'],
    #APP
    'APP':['AP','APP'],
    #B端APP
    'APB':['APB','B端APP'],
}

###配送类型
DELIVERY_TYPE = {
    #周套餐
    'WEEK':['0','周套餐'],
    #月套餐
    'MONTH':['20','1个月'],
    #季套餐
    'SEASON':["21",'3个月'],
    #半年套餐
    'HALF-YEAR':["22",'6个月']
}

###红包规则类型
RULE_TYPE = {
    #满减红包
    "FIX":['RULE_FIX','满减红包'],
    #百分比红包
    "PERCENT":['RULE_PERCENT','折扣'],
    #随机红包
    "RANDOM":['RULE_RANDOM','随机红包']
}

###付款类型
PAY_TYPE = {
    "COD":['cod','货到付款'],
    "weixin":['weixin','微信支付'],
    "alipay":['alipay','支付宝'],
    "dhuidou":['dhuidou','东汇豆']
}

###发票类型
INVOICE_TYPE = {
    "PERSONAL":['personal','个人'],
    "ENTERPRISE":['enterprise','企业']
}

###企业类型
ENTERPRISE_TYPE = {
    "AIRONG":[1,'爱融用户'],
    "LITTERBEE":[2,"小蜜蜂团队"]
}

###秒杀商品状态
SECKILL_GOODS_STATUS = {
    "NOT_START":[0,'耐心等待'],
    "PROCESSING":[1,'秒杀'],
    "NOT_GRAP":[2,'已抢完'],
    "SECKILL_END":[3,"活动结束"],
    "SECKILL_SUCCESS":[4,"抢购成功"],
}

###主页模块location类型列表
MAIN_MODULE_LOCATION_LIST = ['#01','#02','#03','#04']

###时区
TIME_ZONE_BEIJING = 8

###修改送货时间提前的天数
MODIFY_SHIPPING_DAYS = 2

###能够修改的最大次数
MODIFY_MAX_COUNTS = 1

###快递100相关参数
#授权key
KUAIDI100_KEY = "NoCeSxdp4156"
#订阅url
KUAIDI100_SUBSCRIBE_URL = "http://www.kuaidi100.com/poll"
#K快递100 送货状态
KUAIDI100_STATE = {
    "ON_WAY":[0,'在途中'],
    "RECEIVED":[1,'已揽收'],
    "PROBLEM":[2,'疑难'],
    "SIGNED":[3,'已签收']
}

LOCALES = ("en", "zh_CN", "zh_TW")
