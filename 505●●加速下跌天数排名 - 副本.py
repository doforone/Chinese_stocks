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


def get_english_len(s):
    length = 0
    for ch in s:
        if '\u4e00' <= ch <= '\u9fff':
            length += 2  # 中文字符占两个字节
        else:
            length += 1  # 英文字符占一个字节
    return length


a="d"
rrr=[]
s = -2  # 一般为-1，不得大于-1
rrr2={"A":0,"O":0,"V":0}  # s当日上涨与下跌股票数量
rrr_amount=[]  # 统计股票s及之前一段时间内的交易额，包括s日
rrr_cap=[]  # 统计s日的市值
rrr_turn=[]  # 统计股票s及之前一段时间内的换手率，包括s日

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

            if (lenn:=len(ooo))>=abs(s):
                if s==-1:
                    amountt=sum([float_000(x[8]) for x in ooo[s-6:]])  # 包括s日的交易额
                else:
                    amountt=sum([float_000(x[8]) for x in ooo[s-6:s+1]])  # 包括s日的交易额
                rrr_amount.append([dd[0], amountt])

                if s==-1:
                    turnn=sum([float_000(x[10]) for x in ooo[s-6:]])  # 包括s日的换手率
                else:
                    turnn=sum([float_000(x[10]) for x in ooo[s-6:s+1]])  # 包括s日的换手率
                rrr_turn.append([dd[0], turnn])

                if float_000(ooo[s][10])!=0:
                    capp=float_000(ooo[s][5])*(float_000(ooo[s][7])*100/float_000(ooo[s][10]))  # s日的市值
                else:
                    capp=0
                rrr_cap.append([dd[0], capp])
                
                if (f12:=float_000(ooo[s][12]))>0:
                    rrr2["A"]+=1
                elif f12<0:
                    rrr2["V"]+=1
                else:
                    rrr2["O"]+=1
                    
                n=0
                x=-1000
                for oo in ooo[s::-1]:
                    if float_000(oo[12])<0 and float_000(oo[12])>x:
                        n+=1
                        x=float_000(oo[12])
                    else:
                        break

                #if n>=3:  #加速下跌超过3天
                if n>=3 and float_000(ooo[-n+s][12])>0:
                    EE=sum([abs(float_000(x[12])) for x in ooo])/lenn
                    if dd[0] in ddd3:
                        if s<-1:
                            rrr.append([dd[0], dd[1], ddd2[dd[0]], n, ooo[s][0], float_000(ooo[s][5]), float_000(ooo[s][12]), 1, float_000(ooo[s+1][12]), amountt, EE, capp, turnn])
                        else:
                            rrr.append([dd[0], dd[1], ddd2[dd[0]], n, ooo[s][0], float_000(ooo[s][5]), float_000(ooo[s][12]), 1, 0, amountt, EE, capp, turnn])
                    else:
                        if s<-1:
                            rrr.append([dd[0], dd[1], ddd2[dd[0]], n, ooo[s][0], float_000(ooo[s][5]), float_000(ooo[s][12]), 0, float_000(ooo[s+1][12]), amountt, EE, capp, turnn])
                        else:
                            rrr.append([dd[0], dd[1], ddd2[dd[0]], n, ooo[s][0], float_000(ooo[s][5]), float_000(ooo[s][12]), 0, 0, amountt, EE, capp, turnn])


print("说明：1、数据使用为不复权数据；2、当日涨跌幅度=(当日收盘-前日收盘)/前日收盘*100%；3、每年分红股票（●）为至少上市4年，最多1年没有分红（除权）的股票；4、新上市股票不定期更新。\r\n")


if os.path.exists(f'data/k_line_{a}/sh.000001_{a}.txt'):  #使用不复权数据，上证
    with open(f'data/k_line_{a}/sh.000001_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo=json.loads(f.read())
    if s<-1:
        print(f"上证：{ooo[s][0]}，【{ooo[s][5]}】，{float_000(ooo[s][12]):.2f}%    {ooo[s+1][0]}，【{ooo[s+1][5]}】，{float_000(ooo[s+1][12]):.2f}%")
    else:
        print(f"上证：{ooo[s][0]}，【{ooo[s][5]}】，{float_000(ooo[s][12]):.2f}%")
#====================
if os.path.exists(f'data/k_line_{a}/sz.399001_{a}.txt'):  #使用不复权数据，深证
    with open(f'data/k_line_{a}/sz.399001_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo=json.loads(f.read())
    if s<-1:
        print(f"深证：{ooo[s][0]}，【{ooo[s][5]}】，{float_000(ooo[s][12]):.2f}%    {ooo[s+1][0]}，【{ooo[s+1][5]}】，{float_000(ooo[s+1][12]):.2f}%")
    else:
        print(f"深证：{ooo[s][0]}，【{ooo[s][5]}】，{float_000(ooo[s][12]):.2f}%")
#====================
if os.path.exists(f'data/k_line_{a}/sz.399006_{a}.txt'):  #使用不复权数据，创业板
    with open(f'data/k_line_{a}/sz.399006_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo=json.loads(f.read())
    if s<-1:
        print(f"创业板：{ooo[s][0]}，【{ooo[s][5]}】，{float_000(ooo[s][12]):.2f}%    {ooo[s+1][0]}，【{ooo[s+1][5]}】，{float_000(ooo[s+1][12]):.2f}%")
    else:
        print(f"创业板：{ooo[s][0]}，【{ooo[s][5]}】，{float_000(ooo[s][12]):.2f}%")
#====================
    
print(f"\r\n{rrr2}")
rrr=sorted(rrr, key=lambda x: x[6], reverse=False)

rrr_amount.sort(key=lambda x: x[1], reverse=True)
rrr_cap.sort(key=lambda x: x[1], reverse=True)
rrr_turn.sort(key=lambda x: x[1], reverse=True)
print(f"共：{len(rrr_amount)}只股票")

print("\r\n========加速下跌（每天下跌均高于前一天）========\r\n")
nn=0
ss=0
ss2=0
for rr in rrr:
#for rr in rrr[:len(rrr)//2]:
    #if rr[7]==1 and rrr_amount.index([rr[0], rr[9]])+1<1000:  # **
    #if rrr_amount.index([rr[0], rr[9]])+1<1000:  # 7日成交额 **
    #if rrr_turn.index([rr[0], rr[12]])+1<1000:  # 7日换手率
    #if rr[7]==1:
    #if rrr_amount.index([rr[0], rr[9]])+1<1000 and rrr_turn.index([rr[0], rr[12]])+1<1000:
    if 1:
        nn+=1
        ss+=rr[6]
        ss2+=rr[8]
        if rr[0][:6]=="sh.688":
            print(f"{rr[0]} {rr[1]:　^4}（{rr[2]:　^4}） 加速下跌：{rr[3]}天，截止：{rr[4]}，收盘：{rr[5]:7.2f}元，涨跌：【{rr[6]:8.4f}%】，下一日：【{rr[8]:8.4f}%】  \
7日额：{rrr_amount.index([rr[0], rr[9]])+1:4}  7日换手：{rrr_turn.index([rr[0], rr[12]])+1:4}  市值：{rrr_cap.index([rr[0], rr[11]])+1:4}  \
平均AV：{rr[10]:.2f}%  {'●' if rr[7]==1 else ''}  科创板")
        elif rr[0][:4]=="sz.3":
            print(f"{rr[0]} {rr[1]:　^4}（{rr[2]:　^4}） 加速下跌：{rr[3]}天，截止：{rr[4]}，收盘：{rr[5]:7.2f}元，涨跌：【{rr[6]:8.4f}%】，下一日：【{rr[8]:8.4f}%】  \
7日额：{rrr_amount.index([rr[0], rr[9]])+1:4}  7日换手：{rrr_turn.index([rr[0], rr[12]])+1:4}  市值：{rrr_cap.index([rr[0], rr[11]])+1:4}  \
平均AV：{rr[10]:.2f}%  {'●' if rr[7]==1 else ''}  创业板")
        else:
            print(f"{rr[0]} {rr[1]:　^4}（{rr[2]:　^4}） 加速下跌：{rr[3]}天，截止：{rr[4]}，收盘：{rr[5]:7.2f}元，涨跌：【{rr[6]:8.4f}%】，下一日：【{rr[8]:8.4f}%】  \
7日额：{rrr_amount.index([rr[0], rr[9]])+1:4}  7日换手：{rrr_turn.index([rr[0], rr[12]])+1:4}  市值：{rrr_cap.index([rr[0], rr[11]])+1:4}  \
平均AV：{rr[10]:.2f}%  {'●' if rr[7]==1 else ''}")

print(f"\r\n以上共：{nn}条  涨跌累加：{ss:.2f}%  下一日涨跌累加：{ss2:.2f}%  平均：{ss2/nn:.2f}%")
print(f"\r\n共：{len(rrr)}条  涨跌累加：{sum([x[6] for x in rrr]):.2f}%  下一日涨跌累加：{sum([x[8] for x in rrr]):.2f}%  平均：{sum([x[8] for x in rrr])/len(rrr):.2f}")


##print("\033[31mHello, World!\033[0m")
##print("\033[32mHello, World!\033[0m")
##
##while (x:=input("输入X退出：")):
##    if x=="x" or x=="X":
##        print("--end--")
##        break

print("--end--")
