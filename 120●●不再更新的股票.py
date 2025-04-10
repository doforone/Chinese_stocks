# 白点数据，运行环境Python3.8
# -*- coding: UTF-8 -*-

from urllib import request, parse
from urllib.parse import quote
import urllib.parse

import json
import datetime
import os
import time


##参数名称	参数描述
##code	证券代码
##code_name	证券名称
##ipoDate	上市日期
##outDate	退市日期
##type	证券类型，其中1：股票，2：指数，3：其它，4：可转债，5：ETF
##status	上市状态，其中1：上市，0：退市


#### 日K线参数名称及定义 ####
##"2023-07-27,1836.00,1838.03,1854.79,1828.70,20340,3749635290.00,1.43,0.52,9.48,0.16"
##茅台日期         开盘        收盘         最高        最低        成交量（手）成交额（元）振幅 涨跌幅 涨跌 流通换手率


with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())


rrr=[]
for dd in reversed(ddd):
    if (dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3") or \
       dd[0]=="sh.000001" or dd[0]=="sz.399001" or dd[0]=="sz.399006":
        print(dd[0])

        #=================
        ooo=[]
        if os.path.exists(f'data/k_line_d_东方财富/{dd[0]}_d.txt'):
            with open(f'data/k_line_d_东方财富/{dd[0]}_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())
            if ooo==[]:
                rrr.append(dd[0])
            else:
                t_str=(datetime.datetime.strptime(ooo[-1][0],'%Y-%m-%d')+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                if t_str=="2023-09-05":  #---------------这个日期为延后一天的
                    continue  #---------------
                else:
                    rrr.append(dd[0])
        else:
            rrr.append(dd[0])
        #==================
        
print(rrr)

with open(f'data/不再更新的股票.txt', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(json.dumps(rrr, indent=4, ensure_ascii=False)+"\r\n")


print("--end--")
