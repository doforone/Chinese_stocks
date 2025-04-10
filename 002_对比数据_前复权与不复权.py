import baostock as bs
import pandas as pd

import json
from PIL import Image, ImageDraw,ImageFont
import datetime
import os

with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

with open('data/行业分类2.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd2=json.loads(f.read())

with open('data/每年都有分红的股票.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd3=json.loads(f.read())

#### 日K线参数名称及定义 ####
##"2023-07-27,1836.00,1838.03,1854.79,1828.70,20340,3749635290.00,1.43,0.52,9.48,0.16"
##茅台日期         开盘        收盘         最高        最低        成交量（手）成交额（元）振幅 涨跌幅 涨跌 流通换手率
##   0              1           2            3          4            5           6           7    8      9     10

##      参数名称	参数描述	说明
## 0    date	交易所行情日期	格式：YYYY-MM-DD
## 1    code	证券代码	格式：sh.600000。sh：上海，sz：深圳
## 2    open	今开盘价格	精度：小数点后4位；单位：人民币元
## 3    high	最高价	精度：小数点后4位；单位：人民币元
## 4    low	最低价	精度：小数点后4位；单位：人民币元
## 5    close	今收盘价	精度：小数点后4位；单位：人民币元
## 6    preclose	昨日收盘价	精度：小数点后4位；单位：人民币元
## 7    volume	成交数量	单位：股
## 8    amount	成交金额	精度：小数点后4位；单位：人民币元
## 9    adjustflag	复权状态	不复权、前复权、后复权
##10    turn	换手率	精度：小数点后6位；单位：%
##11    tradestatus	交易状态	1：正常交易 0：停牌
##12    pctChg	涨跌幅（百分比）	精度：小数点后6位
##13    peTTM	滚动市盈率	精度：小数点后6位
##14    psTTM	滚动市销率	精度：小数点后6位
##15    pcfNcfTTM	滚动市现率	精度：小数点后6位
##16    pbMRQ	市净率	精度：小数点后6位
##17    isST	是否ST	1是，0否

#日期【0】  昨收【1】  开盘【2】  最低【3】  最高【4】  收盘【5】
#振幅【6】  涨跌【7】  成交量【8】  成交额【9】  换手率【10】


f0=lambda x: 0.0 if x=="" else float(x)


a="d"  #K线频率
b=5  #汇总几个
for dd in ddd:
    #if dd[0][:3]!="of." and dd[0] in ddd3 and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":  #正常使用
    #if dd[0][:3]!="of." and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":  #正常使用
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
    #if dd[0]=="sh.000001" or dd[0]=="sz.399001":
    #if 1==1:
        if dd[4]=="1" and dd[5]=="1" and dd[3]=="":  #股票  正常使用
        #if dd[4]=="2" and dd[5]=="1" and dd[3]=="":  #指数
        #if 1==1:
            #print(dd)
            pass
        else:
            continue

        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):
            pass
        else:
            continue

        ooo=uuu=[]
        
        #with open(f'data/k_line_{a}_东方财富_前复权/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
            ooo=json.loads(f.read())

        with open(f'data/k_line_{a}_东方财富_不复权/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
            uuu=json.loads(f.read())

        #if ooo[0][1]!=uuu[0][1]:
        if ooo[0][0]!=uuu[0][0]:
            print(dd)
            print(ooo[0][0],ooo[0][1],uuu[0][0],uuu[0][1])
            print("---")


print("--end--")
