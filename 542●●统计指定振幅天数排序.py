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


f0=lambda x: 0.0 if x=="" else float(x)


with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

with open('data/行业分类2.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd2=json.loads(f.read())

with open('data/每年都有分红的股票.txt', 'r', encoding='utf-8-sig', \
          newline='\r\n') as f:
    ddd3=json.loads(f.read())

a="d"
AV=1.02  # 1%，2%，3%在此修改
rrr=[]
rrr_amount=[]  # 统计股票s及之前一段时间内的交易额，包括s日
rrr_cap=[]  # 统计s日的市值
rrr_turn=[]  # 统计股票s及之前一段时间内的换手率，包括s日
    
for dd in ddd:
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0] in ddd3 and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
    # 以上代码可控制选择是否分红，是否科创板
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":

        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):  # 使用不复权数据
            with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())

        if ooo!=[]:
            if len(ooo)>=7+5:  # 5为上市前5日没有涨跌幅限制
                amountt=sum([f0(x[8]) for x in ooo[-7:]])  # 前7日交易额
                rrr_amount.append([dd[0], amountt])

                turnn=sum([f0(x[10]) for x in ooo[-7:]])  # 前7日换手率
                rrr_turn.append([dd[0], turnn])

                if f0(ooo[-1][10])!=0:
                    capp=f0(ooo[-1][5])*(f0(ooo[-1][7])*100/f0(ooo[-1][10]))  # 当日的市值
                else:
                    capp=0
                rrr_cap.append([dd[0], capp])

            uuu=[f0(x[8])/f0(x[7]) for x in ooo if f0(x[7])>0]
            for i in range(1,len(uuu)):
                if max(uuu[-i:])/min(uuu[-i:])>AV:
                    rrr.append([dd[0], dd[1], ddd2[dd[0]], f0(ooo[-1][5]), i, ooo[0][0], f0(ooo[-1][12]), amountt, turnn, capp])
                    break


rrr_amount.sort(key=lambda x: x[1], reverse=True)
rrr_cap.sort(key=lambda x: x[1], reverse=True)
rrr_turn.sort(key=lambda x: x[1], reverse=True)

print(f"区间震荡：{AV} ，按天数排名（前50）------------:")
rrr2=sorted(rrr, key=lambda x: x[4], reverse=True)

for rr in rrr2[:50]:
    print(f"{rr[0]}  上市日期：{rr[5]}  {rr[1]:　^4}（{rr[2]:　^4}）  {rr[3]:>7.2f}元  {rr[6]:>6.2f}%  {rr[4]:>2}天  \
7日额：{rrr_amount.index([rr[0], rr[7]])+1:4}  7日换手：{rrr_turn.index([rr[0], rr[8]])+1:4}  市值：{rrr_cap.index([rr[0], rr[9]])+1:4}")

print("--end--")
