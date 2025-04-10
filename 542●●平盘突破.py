# 白点数据，运行环境Python3.8（兼顾win7，win2008系统）
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

with open('data/每年都有分红的股票.txt', 'r', encoding='utf-8-sig', \
          newline='\r\n') as f:
    ddd3=json.loads(f.read())


f0=lambda x: 0.0 if x=="" else float(x)


a="d"
b=-0  # 默认为-0
AV=1.02  # 1%，2%，3%在此修改
rrr=[]
for dd in ddd:
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0] in ddd3 and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
    # 以上代码可控制选择是否分红，是否科创板
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1":
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
        ooo=[]
        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):  # 使用不复权数据
            with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())

        if ooo!=[] and len(ooo)>abs(b-2):
            uuu=[f0(x[8])/f0(x[7]) for x in ooo if f0(x[7])>0]
            for i in range(2,len(uuu)+b):
                maxx=max(uuu[-i+b:-1+b])
                minn=min(uuu[-i+b:-1+b])
                if minn>0:
                    if maxx/minn>AV:
                        if uuu[-1+b]>maxx:
                            rrr.append([dd[0], dd[1], ddd2[dd[0]], f0(ooo[-1+b][5]), i-2, ooo[0][0], f0(ooo[-1+b][12]), ooo[-1+b][0], f0(ooo[-1][5])])
                        break


rrr.sort(key=lambda x: x[4], reverse=True)
print(f"---({b})---")
print(f"区间震荡：{AV} ，最后向上突破，按震荡天数排名（前10）:")
for rr in rrr[:10]:
    #print(f"{rr[0]}  上市：{rr[5]}  {rr[1]}（{rr[2]}）  收盘：{rr[7]}  {rr[3]}元  {rr[6]}%  {rr[4]}天  {rr[8]}")
    print(f"{rr[0]}  上市：{rr[5]}  {rr[1]}  收盘：{rr[7]} 【{rr[3]}元】  {rr[6]}%  {rr[4]}天  {rr[8]}{'●' if rr[8]>rr[3] else ''}")
    #print(f"{rr[0]}（{rr[1]}）收盘：{rr[7]} 【{rr[3]}元】  {rr[6]}%  {rr[4]}天  {rr[8]}{'●' if rr[8]>rr[3] else ''}")
    #print(f"{rr[0]}（{rr[1]}）【{rr[3]}元】  {rr[6]:.2f}%  {rr[4]}天")


print("--end--")
