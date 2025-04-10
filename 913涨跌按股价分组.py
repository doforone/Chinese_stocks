# 白点数据，运行环境Python3.8（兼顾win7及win2008系统）
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


with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

with open('data/行业分类2.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd2=json.loads(f.read())


f0=lambda x: 0.0 if x=="" else float(x)


rrr={}
a="d"
for dd in ddd:
    ooo=[]
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1":  # 统计科创板
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":  # 不统计科创板
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3" and dd[1][0]=="中":  # 中字头
        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):
            with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())

        if ooo!=[]:
            for oo in ooo[:-50:-1]:
                key=f0(oo[6])//5
                rrr.setdefault(key, [0, 0])
                if f0(oo[12])>0:
                    #rrr[key][0]+=1
                    rrr[key][0]+=f0(oo[12])
                elif f0(oo[12])<0:
                    #rrr[key][1]+=1
                    rrr[key][1]+=f0(oo[12])


rrr2=sorted(rrr.items(), key=lambda x: x[0])
print(f"股票统计总数：{len(rrr)}")
for rr in rrr2:
    print(f"{int(rr[0]*5):>4}——{int((rr[0]+1)*5):>4}元：  上涨：{rr[1][0]}  下跌：{rr[1][1]}  上涨与下跌之比：{rr[1][0]/rr[1][1] if rr[1][1]!=0 else 0:.2f}")


print("--end--")
