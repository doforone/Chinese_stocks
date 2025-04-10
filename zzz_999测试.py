# 白点数据，运行环境Python3.8
# -*- coding: UTF-8 -*-

#### 日K线参数名称及定义 ####
##"2023-07-27,1836.00,1838.03,1854.79,1828.70,20340,3749635290.00,1.43,0.52,9.48,0.16"
##茅台日期         开盘        收盘         最高        最低        成交量（手）成交额（元）振幅% 涨跌幅% 涨跌额 流通换手率
##   0              1           2            3          4            5           6           7    8      9     10
## 振幅%=（最高-最低）/昨收；涨跌幅%=（收盘-昨收）/昨收；涨跌值=收盘-昨收

## 日期【0】  昨收【1】  开盘【2】  最低【3】  最高【4】  收盘【5】
## 振幅【6】  涨跌【7】  成交量【8】  成交额【9】  换手率【10】

##        "column": [
##            "timestamp",  # 0 时间戳
##            "volume",  # 1 成交量
##            "open",  # 2 开盘
##            "high",  # 3 最高
##            "low",  # 4 最低
##            "close",  # 5 收盘
##            "chg",  # 6 涨跌额
##            "percent",  # 7 涨跌幅%=(今收/昨收-1)*100
##            "turnoverrate",  # 8 换手率
##            "amount",  # 9 成交额
##            "volume_post",
##            "amount_post",
##            "pe",
##            "pb",
##            "ps",
##            "pcf",
##            "market_capital",
##            "balance",
##            "hold_volume_cn",
##            "hold_ratio_cn",
##            "net_volume_cn",
##            "hold_volume_hk",
##            "hold_ratio_hk",
##            "net_volume_hk"
##        ],

#ooo=list([[x[0],f0(x[1]),f0(x[2]),f0(x[3]),f0(x[4]),f0(x[5]),f0(x[6]),f0(x[7]),f0(x[8]),f0(x[9]),f0(x[10])] for x in ooo])
#ooo=[[tt_d(int(x[0]/1000)),x[2],x[5],x[3],x[4],x[1],x[9],(x[3]-x[4])*100/(x[5]-x[6]),x[7],x[6],x[8]] for x in ooo]

from urllib import request, parse
from urllib.parse import quote
import urllib.parse

import time
import datetime
import json
import base64
import hashlib
import random
import os
import io
import zipfile
import zlib

import urllib.request
import gzip

from PIL import Image, ImageDraw,ImageFont


with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

with open('data/行业分类2.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd2=json.loads(f.read())

with open('data/每年都有分红的股票.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd3=json.loads(f.read())

with open('data/不再更新的股票.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd4=json.loads(f.read())


f0=lambda x: 0.0 if x=="" else float(x)


def tt_d(x):  # 时间戳转日期
    timestamp = x  # 假设这是一个时间戳
    # 使用 fromtimestamp() 方法将时间戳转换为日期时间对象
    #date_time = datetime.datetime.fromtimestamp(timestamp)
    date_time = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
    #date_time = datetime.datetime.fromtimestamp(timestamp, tz=pytz.timezone('Asia/Shanghai'))
    # 然后可以使用 strftime() 方法将日期时间格式化为特定的日期字符串
    #formatted_date = date_time.strftime('%Y-%m-%d %H:%M:%S')
    formatted_date = date_time.strftime('%Y-%m-%d')
    return formatted_date  # 输出格式化后的日期字符串


def get_english_len(s):
    length = 0
    for ch in s:
        if '\u4e00' <= ch <= '\u9fff':
            length += 2  # 中文字符占两个字节
        else:
            length += 1  # 英文字符占一个字节
    return length


if os.path.exists(f'data/k_line_d_东方财富_后复权/sh.000001_d.txt'):  #使用不复权数据，上证
    with open(f'data/k_line_d_东方财富_后复权/sh.000001_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo_A=json.loads(f.read())
    AA=ooo_A[0][0]
    ZZ=ooo_A[-1][0]
            

alll={}
nnn=0  # 次数累积
mmm=0  # 胜率累加
oth1=oth2=0
rrr_len=[]
rrr_AV=[]
rrr_AV_len=[]
#s = -2  # 一般为-1，不得大于-1
#for s in range(-2, 0):
#for s in range(-1500,-1):

A=0
V=0
O=0
for dd in ddd:
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3" and dd[0] not in ddd4:
        if os.path.exists(f'data/k_line_d_东方财富_不复权/{dd[0]}_d.txt'):
            with open(f'data/k_line_d_东方财富_不复权/{dd[0]}_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())[-1500:]  #=============控制此处，减小内存占用
                #ooo=list([[x[0],f0(x[1]),f0(x[2]),f0(x[3]),f0(x[4]),f0(x[5]),f0(x[6]),f0(x[7]),f0(x[8]),f0(x[9]),f0(x[10])] for x in ooo])
                #ooo=[[tt_d(int(x[0]/1000)),x[2],x[5],x[3],x[4],x[1],x[9],(x[3]-x[4])*100/(x[5]-x[6]),x[7],x[6],x[8]] for x in ooo]

                for oo in ooo:
                    if oo[2]>oo[1]:
                        A+=1
                    elif oo[2]==oo[1]:
                        O+=1
                    else:
                        V+=1
                
##                #if (d:=tt_d(int(ooo[0][0]/1000))) in alll.keys():
##                if (d:=ooo[0][0]) in alll.keys():
##                    alll[d]+=1
##                else:
##                    alll[d]=1

###print(alll)
##summ=sum([x[1] for x in alll.items()])
##print(summ)
##alll=dict(sorted(alll.items(), key=lambda x: x[1]))
##for dd in alll.items():
##    print(dd)

print(f"A:{A}  O:{O}  V:{V}")
                    

