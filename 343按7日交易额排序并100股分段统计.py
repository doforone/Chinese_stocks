# 白点数据，运行环境Python3.8
# -*- coding: UTF-8 -*-

#### 日K线参数名称及定义 ####
##       参数名称	参数描述	说明
##  0    date	交易所行情日期	格式：YYYY-MM-DD
##  1    code	证券代码	格式：sh.600000。sh：上海，sz：深圳
##  2    open	今开盘价格	精度：小数点后4位；单位：人民币元
##  3    high	最高价	精度：小数点后4位；单位：人民币元
##  4    low	最低价	精度：小数点后4位；单位：人民币元
##  5    close	今收盘价	精度：小数点后4位；单位：人民币元
##  6    preclose	昨日收盘价	精度：小数点后4位；单位：人民币元
##  7    volume	成交数量	单位：股
##  8    amount	成交金额	精度：小数点后4位；单位：人民币元
##  9    adjustflag	复权状态	不复权、前复权、后复权
## 10    turn	换手率	精度：小数点后6位；单位：%
## 11    tradestatus	交易状态	1：正常交易 0：停牌
## 12    pctChg	涨跌幅（百分比）	精度：小数点后6位
## 13    peTTM	滚动市盈率	精度：小数点后6位
## 14    psTTM	滚动市销率	精度：小数点后6位
## 15    pcfNcfTTM	滚动市现率	精度：小数点后6位
## 16    pbMRQ	市净率	精度：小数点后6位
## 17    isST	是否ST	1是，0否

## 日期【0】  昨收【1】  开盘【2】  最低【3】  最高【4】  收盘【5】
## 振幅【6】  涨跌【7】  成交量【8】  成交额【9】  换手率【10】


import json
import os
from PIL import Image, ImageDraw,ImageFont

import random

with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

with open('data/行业分类2.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd2=json.loads(f.read())

with open('data/每年都有分红的股票.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd3=json.loads(f.read())

def float_000(a):
    return 0.0 if a=="" else float(a)

a="d"
rrr=[]
s=-59  # 不能大于-1

for dd in ddd:
    #print(dd[0])
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0] in ddd3 and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1":
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0] not in ddd3 and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
        #print(dd)
        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):
            with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())

            if len(ooo)>abs(s-7):
                amountt=sum([float_000(x[8]) for x in ooo[s-7:s]])
                AV=(float_000(ooo[s-1][5])-float_000(ooo[s-7][2]))*100/float_000(ooo[s-7][2])
                rrr.append([dd[0], dd[1], ddd2[dd[0]], ooo[-1][0], amountt, AV])


rrr.sort(key=lambda x: x[4], reverse=True)

AV=0
for rr in rrr[:300]:
    AV+=rr[5]
    print(f"{rr[0]} {rr[1]}（{rr[2]}） 数据截止：{rr[3]}  7日额：{int(rr[4]/10000):,}万  7日涨跌：{rr[5]:.2f}%")

print(f"涨跌总计：{AV:.2f}%")

rrr2=[]
n=0
AV=0
for rr in rrr:
    if n<100:
        n+=1
        AV+=rr[5]
    else:
        rrr2.append(AV)
        n=0
        AV=0

for rr in rrr2:
    print(f"{rr:10.2f}")

##print("\033[31mHello, World!\033[0m")
##print("\033[32mHello, World!\033[0m")
##
##while (x:=input("输入X退出：")):
##    if x=="x" or x=="X":
##        print("--end--")
##        break

print("--end--")
