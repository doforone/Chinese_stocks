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

for dd in ddd:
    #print(dd[0])
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0] in ddd3 and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1":
        #print(dd)
        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):
            with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())

        if ooo!=[]:
            uuu=[[x[0], float_000(x[6]), float_000(x[2]), float_000(x[4]), float_000(x[3]), float_000(x[5]), float(x[3])-min([float(x[4]),float(x[6])]),\
                 float_000(x[12]), float_000(x[7]), float_000(x[8]), float_000(x[10])] for x in ooo]

            n=0
            for uu in uuu[::-1]:
                if uu[7]<0:
                    n+=1
                else:
                    break

            if n>=3:
                if dd[0] in ddd3:
                    rrr.append([dd[0], dd[1], ddd2[dd[0]], n, uuu[-1][0], uuu[-1][5], 1])
                else:
                    rrr.append([dd[0], dd[1], ddd2[dd[0]], n, uuu[-1][0], uuu[-1][5], 0])


print("说明：1、数据使用为不复权数据；2、当日涨跌幅度=(当日收盘-前日收盘)/前日收盘*100%；3、每年分红股票（●）为至少上市4年，最多1年没有分红（除权）的股票；4、新上市股票不定期更新。\r\n")
rrr=sorted(rrr, key=lambda x: x[3])
print("========连续下跌超过3天，按天数排名（前50）========\r\n")

for rr in rrr[::-1][:50]:
    if rr[0][:6]=="sh.688":
        print(f"{rr[0]} {rr[1]}（{rr[2]}） 连续下跌：{rr[3]}天，数据截止：{rr[4]}，收盘价：{rr[5]}元  {'●' if rr[6]==1 else ''}  科创板")
    elif rr[0][:4]=="sz.3":
        print(f"{rr[0]} {rr[1]}（{rr[2]}） 连续下跌：{rr[3]}天，数据截止：{rr[4]}，收盘价：{rr[5]}元  {'●' if rr[6]==1 else ''}  创业板")
    else:
        print(f"{rr[0]} {rr[1]}（{rr[2]}） 连续下跌：{rr[3]}天，数据截止：{rr[4]}，收盘价：{rr[5]}元  {'●' if rr[6]==1 else ''}")

print("......")
print(f"共：{len(rrr)}")
print("--end--")
