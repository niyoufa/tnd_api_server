# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-04-26
#

import sys
import requests

function = sys.argv[1]

#18点档
if function == 'daily1':
    requests.get("https://www.dhuicredit.com/api/report/airong/sales")
    # requests.get("https://www.dhuicredit.com/api/report/order/dhuidou?report_hour=18")

    requests.get("https://www.dhuicredit.com/api/report/order?report_name=order_normal&param_name=normal&report_china_name=常购订单详情")
    requests.get("https://www.dhuicredit.com/api/report/order?report_name=order_limit&param_name=limit&report_china_name=特别定制订单详情")
    requests.get("https://www.dhuicredit.com/api/report/order?report_name=order_todayspecial&param_name=today_special&report_china_name=今日特价订单详情")
    requests.get("https://www.dhuicredit.com/api/report/order?report_name=order_goldbean&param_name=goldbean&report_china_name=东汇豆充值订单详情")
    requests.get("https://www.dhuicredit.com/api/report/order?report_name=order_profit&param_name=profit&report_china_name=余额充值订单详情")

#12点档
elif function == 'daily2':
    requests.get("https://www.dhuicredit.com/api/report/order/dhuidou")
    requests.get("https://www.dhuicredit.com/api/report/dhuidou/withdraws")
    requests.get("https://www.dhuicredit.com/api/report/dhuidou/commission")
    requests.get("https://www.dhuicredit.com/api/report/order")
    requests.get("https://www.dhuicredit.com/api/report/user/inviter?table_name=litterbee_user")

    # requests.get("https://www.dhuicredit.com/api/report/dhuidou/inout?start_time=2016-05-01")

    # requests.get("https://www.dhuicredit.com/api/report/order/dhuidou?report_hour=00&email_list=nj.xuchunlin@donghuicredit.com,&start_time=2016-01-01")
    # requests.get("https://www.dhuicredit.com/api/report/order?report_hour=00&email_list=nj.xuchunlin@donghuicredit.com,&start_time=2016-01-01")
    # requests.get("https://www.dhuicredit.com/api/report/dhuidou/withdraws?report_hour=00&email_list=nj.xuchunlin@donghuicredit.com,&start_time=2016-01-01")
    # requests.get("https://www.dhuicredit.com/api/report/airong/sales?report_hour=00&email_list=nj.xuchunlin@donghuicredit.com,&start_time=2016-01-01")
    # requests.get("https://www.dhuicredit.com/api/report/dhuidou/commission?report_hour=00&email_list=nj.xuchunlin@donghuicredit.com,&start_time=2016-01-01")

    requests.get("https://www.dhuicredit.com/api/report/order?report_name=order_luckybag&is_luckybag=福袋&report_china_name=福袋订单详情")

#23点档
elif function == 'daily3':
    requests.get("https://www.dhuicredit.com/api/dhuidou/flowcost")
    requests.get("https://www.dhuicredit.com/api/report/order?report_name=order_seckill&param_name=seckill&report_china_name=秒拍订单详情")
    requests.get("https://www.dhuicredit.com/api/report/order?start_time=2016-01-01&report_name=order_seckill&param_name=seckill&report_china_name=秒拍订单详情")

