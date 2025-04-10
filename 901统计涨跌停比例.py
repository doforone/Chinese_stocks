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


rrr1=[]
rrr2=[]
rrr3=[]


a="d"
for dd in ddd:
    #print(dd[0])
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0] in ddd3 and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1":
        #print(dd)
        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):  #使用不复权数据
            with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())

        if ooo!=[] and len(ooo)>5:
            uuu=[[x[0], float_000(x[6]), float_000(x[2]), float_000(x[4]), float_000(x[3]), float_000(x[5]), float(x[3])-min([float(x[4]),float(x[6])]),\
                 float_000(x[12]), float_000(x[7]), float_000(x[8]), float_000(x[10])] for x in ooo]

            if dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
                #AA=round(sum(uu[7]>=9.8 for uu in uuu if uu[0][:4]=="2023")*100/len(uuu),2)  # 普通版
                AA=sum(uu[7]>=9.8 for uu in uuu if uu[0][:4]=="2023")  # 普通版
            else:
                #AA=round(sum(uu[7]>=19.8 for uu in uuu if uu[0][:4]=="2023")*100/len(uuu),2)  # 科创板
                AA=sum(uu[7]>=19.8 for uu in uuu if uu[0][:4]=="2023")  # 科创板
            rrr1.append([dd, uuu[-1][5], AA, len(uuu)])

            if dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
                AA=round(sum(uu[7]>=9.8 for uu in uuu)*100/len(uuu),2)  # 普通版
                #AA=sum(uu[7]>=9.8 for uu in uuu)  # 普通版
            else:
                AA=round(sum(uu[7]>=19.8 for uu in uuu)*100/len(uuu),2)  # 科创板
                #AA=sum(uu[7]>=19.8 for uu in uuu)  # 科创板
            rrr2.append([dd, uuu[-1][5], AA, len(uuu)])

            if dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
                AA=round(sum(uu[7]<=-9.8 for uu in uuu)*100/len(uuu),2)  # 普通版
                #AA=sum(uu[7]<=-9.8 for uu in uuu)  # 普通版
            else:
                AA=round(sum(uu[7]<=-19.8 for uu in uuu)*100/len(uuu),2)  # 科创板
                #AA=sum(uu[7]<=-19.8 for uu in uuu)  # 科创板
            rrr3.append([dd, uuu[-1][5], AA, len(uuu)])


##print(f"\n说明：1、数据均使用不复权数据；2、T为涨停天数占比；3、E为当前收盘价在历史最低与最高中位置，最低与最高之间100等分。")
rrr1=sorted(rrr1, key=lambda x: x[2], reverse=True)
print(f"\n2023年涨停股票天数排名（前20）")
for rr in rrr1[:20]:
    #print(f"{rr[0][0]} {rr[0][1]}（{ddd2[rr[0][0]]}） {rr[1]}元")
##    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元  T:{rr[2]}%  E:{rr[3]}")
    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元  {rr[2]}天")


rrr2=sorted(rrr2, key=lambda x: x[2], reverse=True)
print(f"\n涨停比例最高排名（前20）")
for rr in rrr2[:20]:
    print(f"{rr[0][0]} {rr[0][1]}  {rr[3]}天  {rr[1]}元  {rr[2]}%")


rrr3=sorted(rrr3, key=lambda x: x[2], reverse=True)
print(f"\n跌停比例最高排名（前20）")
for rr in rrr3[:20]:
    print(f"{rr[0][0]} {rr[0][1]}  {rr[3]}天  {rr[1]}元  {rr[2]}%")


print("备注：主板按9.8%涨跌比例计算，科创板按19.8%涨跌比例计算。")
print("--end--")
