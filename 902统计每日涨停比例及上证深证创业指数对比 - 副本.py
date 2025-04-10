# 白点数据，运行环境Python3.8
# -*- coding: UTF-8 -*-

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


def float_000(a):
    return 0.0 if a=="" else float(a)


rrr={}
a="d"
for dd in ddd:
    #print(dd[0])
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0] in ddd3 and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1":
        #print(dd)
        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):  #使用不复权数据
            with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())

        if ooo!=[] and len(ooo)>=200:  # 因为最低取10天的
            for oo in ooo[-200:]:
                if oo[0] not in rrr.keys():
                    rrr[oo[0]]={"A":0, "O":0, "V":0}
                if float_000(oo[12])>0:
                    rrr[oo[0]]["A"]+=1
                elif float_000(oo[12])==0:
                    rrr[oo[0]]["O"]+=1
                else:
                    rrr[oo[0]]["V"]+=1
                    

if os.path.exists(f'data/k_line_{a}/sh.000001_{a}.txt'):  #使用不复权数据
    with open(f'data/k_line_{a}/sh.000001_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo=json.loads(f.read())

if ooo!=[] and len(ooo)>=200:  # 因为最低取10天的
    for oo in ooo[-200:]:
        rrr[oo[0]]["sh.000001"]=float_000(oo[12])
#====================

if os.path.exists(f'data/k_line_{a}/sz.399001_{a}.txt'):  #使用不复权数据
    with open(f'data/k_line_{a}/sz.399001_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo=json.loads(f.read())

if ooo!=[] and len(ooo)>=200:  # 因为最低取10天的
    for oo in ooo[-200:]:
        rrr[oo[0]]["sz.399001"]=float_000(oo[12])
#====================

if os.path.exists(f'data/k_line_{a}/sz.399006_{a}.txt'):  #使用不复权数据
    with open(f'data/k_line_{a}/sz.399006_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo=json.loads(f.read())

if ooo!=[] and len(ooo)>=200:  # 因为最低取10天的
    for oo in ooo[-200:]:
        rrr[oo[0]]["sz.399006"]=float_000(oo[12])


rrr1=sorted(rrr.items(), key=lambda x: x[0], reverse=True)

print(f"上涨  平盘  下跌 {'上证'.rjust(5)} {'深证'.rjust(5)} {'创业板'.rjust(4)}")
n=0
for rr in rrr1[:200]:
    s=rr[0].split("-")
    datee=f"{s[0]}年{int(s[1])}月{s[2]}日"
    if n%10==0:
        print(datee)
    n+=1
    print(f"{str(rr[1]['A']).rjust(4)}  {str(rr[1]['O']).rjust(4)}  {str(rr[1]['V']).rjust(4)} \
{(str(round(rr[1]['sh.000001'],2))+'%').rjust(7)} {(str(round(rr[1]['sz.399001'],2))+'%').rjust(7)} {(str(round(rr[1]['sz.399006'],2))+'%').rjust(7)}")

print(f"上涨  平盘  下跌 {'上证'.rjust(5)} {'深证'.rjust(5)} {'创业板'.rjust(4)}")

print("--end--")
