# coding: utf-8
# xsy
# 2016.3.22

import xlrd
import sys
import requests

reload(sys)
sys.setdefaultencoding( "utf-8" )

data =xlrd.open_workbook('malls.xlsx')

table = data.sheets()[0]

nrows = table.nrows
ncols = table.ncols

def list_to_dict(list1,list2):
    return dict(zip(list1[::],list2))

for i in range(0,nrows):
    row = table.row_values(i)
    if i == 0:
        columns = row
    else:
        items = list_to_dict(columns,row)

        url ='https://dhuicredit.com/api/malls'
        data = {
                    "mall_num":"",
                    "mall_name":items[u'店名'],
                    "province":items[u'省份'],
                    "city":items[u'城市'],
                    "area":items[u'区'],
                    "address":items[u'地址'],
                }
        res = requests.post(url,data=data)
        print res.json()
