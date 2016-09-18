# coding: utf-8
# xsy
# 2016.3.22


import xlrd
import urllib
import urllib2
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )

data =xlrd.open_workbook(r'D:\sku.xls')

table = data.sheets()[0]

nrows = table.nrows

ncols = table.ncols

for i in range(1,nrows):
    row = table.row_values(i)
    attrs = [{'cost':row[8],'shop_price':row[9],'attr_name':row[10],'market_price':row[11],'attr_id':row[12]}]
    p = {'id':row[0],'goods_name':row[1],'favorite':int(row[2]),'sales':int(row[3]),'is_hot':int(row[5]),'is_new':int(row[6]),'on_sale_flag':int((row[7])),'attrs':attrs,'goods_img':row[13],'specs':row[14],'unit':row[15],'sku':row[16],'goods_desc':row[17],'good_thumb':row[18],'goods_brief':row[19]}

    print(p)

    url ='https://banana.meiguoyouxian.com:8001/api/goods'
    post_data = urllib.urlencode(p)

    req = urllib2.urlopen(url,post_data)

    conttent = req.read()

    print(conttent)