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

##ooo=[[tt_d(int(x[0]/1000)),  # 日期 0
##      x[5]-x[6],  # 前收 1
##      x[2],  # 开盘 2
##      x[4],  # 最低 3
##      x[3],  # 最高 4
##      x[5],  # 收盘 5
##      x[6],  # 涨跌额 6
##      x[7],  # 涨跌幅% 7
##      x[1],  # 成交量 8
##      x[9],  # 成交额 9
##      x[8]  # 换手率 10
##      ] for x in ooo]  # 前收与涨跌额互为印证,因为有的源数据不同,可以相互计算,相互印证,所以都保留了.


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


f0=lambda x: 0.0 if x=="" or x==None else float(x)


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


with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd1=json.loads(f.read())
    ddd12={x[0]:x[1] for x in ddd1}

with open('data/行业分类2.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd2=json.loads(f.read())

with open('data/每年都有分红的股票.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd3=json.loads(f.read())

with open('data/不再更新的股票.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd4=json.loads(f.read())


ddd={}


for dd in ddd1:
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3" and dd[0] not in ddd4:
        if os.path.exists(f'D:\\Python3.8\\香港美国英国等股市\\DATA\\雪球_前复权\\{dd[0].replace(".","")}_d.txt'):
            with open(f'D:\\Python3.8\\香港美国英国等股市\\DATA\\雪球_前复权\\{dd[0].replace(".","")}_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                uuu=json.loads(f.read())[-2100:]  #=============控制此处，减小内存占用
                uuu=[[tt_d(int(x[0]/1000)),  # 日期 0
                      x[5]-x[6],  # 前收 1
                      x[2],  # 开盘 2
                      x[4],  # 最低 3
                      x[3],  # 最高 4
                      x[5],  # 收盘 5
                      x[6],  # 涨跌额 6
                      x[7],  # 涨跌幅% 7
                      x[1],  # 成交量 8
                      x[9] if x[9]!=None else 0,  # 成交额 9
                      x[8]  # 换手率 10
                      ] for x in uuu]  # 前收与涨跌额互为印证,因为有的源数据不同,可以相互计算,相互印证,所以都保留了.
                
                for uu in uuu:
                    if uu[0] in ddd.keys():  # 日期键值
                        ddd[uu[0]][dd[0]]=uu
                    else:
                        ddd[uu[0]]={}
                        ddd[uu[0]][dd[0]]=uu
                        

ddd_data=[x for x in ddd.keys()]
ddd_data.sort()


n_day=0  # 交易天数
n_AV=0  # 收益
for i in range(-1500,-1):
    print(f"--------{i}--------{ddd_data[i]}--{len(ddd[ddd_data[i]])}")
    rrr_cap=[]  # 市值
    rrr_amount=[]  # 成交额
    
    rrr_cap=[[kk, vv[5]*((vv[8]/vv[10])*100) if vv[10]>0 else 0] for kk, vv in ddd[ddd_data[i]].items()]
    rrr_cap=sorted(rrr_cap, key=lambda x: x[1], reverse=True)
    rrr_cap2=[rr[0] for rr in rrr_cap]  # 只提取排序后的股票代码,方便后面索引位置
    
    for rr in rrr_cap:
        rrr_amount.append([rr[0],sum([ddd[ddd_data[j]][rr[0]][9] if rr[0] in ddd[ddd_data[j]].keys() else 0 for j in range(i-7,i+1)])])  # 默认是7(8日额)
    rrr_amount=sorted(rrr_amount, key=lambda x: x[1], reverse=True)
    rrr_amount2=[rr[0] for rr in rrr_amount]  # 只提取排序后的股票代码,方便后面索引位置

    AA=0
    OO=0
    VV=0
    for rr in rrr_cap:  # 此处可控制排名或用rrr_amount排名
        if ddd[ddd_data[i]][rr[0]][7]>0:
            AA+=1
        elif ddd[ddd_data[i]][rr[0]][7]==0:
            OO+=1
        else:
            VV+=1

    print(AA,OO,VV)
    #print(rrr_cap)
    #print(rrr_amount)

    rrr=[]
    for rr in rrr_cap:
        AV=float("-inf")
        n=0
        j=i
        while True:
            if AV<ddd[ddd_data[j]][rr[0]][7] if rr[0] in ddd[ddd_data[j]].keys() else float("inf")<0:
                n+=1
                AV=ddd[ddd_data[j]][rr[0]][7]
                j-=1
            else:
                break

        if n>=2 and ddd[ddd_data[j]][rr[0]][7] if rr[0] in ddd[ddd_data[j]].keys() else float("-inf")>0:
            rrr.append([rr[0],  # 股票代码
                        ddd[ddd_data[i]][rr[0]][5],  # 当日收盘价
                        ddd[ddd_data[i]][rr[0]][7],  # 当日涨跌幅%
                        ddd[ddd_data[i+1]][rr[0]][7] if rr[0] in ddd[ddd_data[i+1]].keys() else 0,  # 下一日涨跌幅%
                        rrr_amount2.index(rr[0]),  # 8日额索引
                        rrr_cap2.index(rr[0])  # 市值索引
                        ])

    if VV>=AA:
        rrr=sorted(rrr, key=lambda x: x[4], reverse=False)  # 按8日额从大到小===常用,默认False
    else:
        rrr=sorted(rrr, key=lambda x: x[4], reverse=True)  # 按8日额从小到大

    n=0
    AV=0
    for rr in rrr:
        #if n<3 and ddd12[rr[0]].find("ST")==-1 and 5<=rr[1]<=50 and -9.8<rr[2]<-0 and rr[5]<int(len(rrr_cap)/10):  #  市值300内
        if n<3 and ddd12[rr[0]].find("ST")==-1 and 5<=rr[1]<=50 and -9.8<rr[2]<-0 and rr[5]<300:  #  市值300内
            n+=1
            AV+=rr[3]
            print(ddd12[rr[0]],rr)

    if n>0:
        n_day+=1
        n_AV+=AV/n
    print(n_day,n_AV)


print("--end--")

