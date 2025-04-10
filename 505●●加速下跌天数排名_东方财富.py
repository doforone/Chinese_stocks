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


with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())
    #ddd=random.sample(ddd,4000)

with open('data/行业分类2.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd2=json.loads(f.read())

with open('data/每年都有分红的股票.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd3=json.loads(f.read())

with open('data/不再更新的股票.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd4=json.loads(f.read())

f0=lambda x: 0.0 if x=="" else float(x)


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


if os.path.exists(f'data/k_line_d_东方财富_前复权/sh.000001_d.txt'):  #使用不复权数据，上证
    with open(f'data/k_line_d_东方财富_前复权/sh.000001_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo_A=json.loads(f.read())
    AA=ooo_A[0][0]
    ZZ=ooo_A[-1][0]
            

alll={}
nnn=0  # 次数累积
mmm=0  # 胜率累加
oth1=oth2=0
rrr_len=[]
rrr_AV=[]
rrr_AV_len=[]
#chongfu=0
#s = -2  # 一般为-1，不得大于-1
for s in range(-2, 0):
#for s in range(-1501,-2):
##for s in range(-1502,-3):
    print(f"****************************************({s})****************************************")
    rrr=[]
    rrr2={"A":0,"O":0,"V":0}  # s当日上涨与下跌股票数量
    rrr3={"A":0,"O":0,"V":0}  # s次日上涨与下跌股票数量
    rrr_AAVV=[]
    rrr_amount=[]  # 统计股票s及之前一段时间内的交易额，包括s日
    rrr_cap=[]  # 统计s日的市值
    rrr_turn=[]  # 统计股票s及之前一段时间内的换手率，包括s日
    
    for dd in ddd:
        if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3" and dd[0] not in ddd4:
            #print(dd)
            if dd[0] in alll.keys():
                ooo=alll[dd[0]]
            elif os.path.exists(f'data/k_line_d_东方财富_前复权/{dd[0]}_d.txt'):
                with open(f'data/k_line_d_东方财富_前复权/{dd[0]}_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                    ooo=json.loads(f.read())[-1600:]  #=============控制此处，减小内存占用
                    ooo=list([[x[0],f0(x[1]),f0(x[2]),f0(x[3]),f0(x[4]),f0(x[5]),f0(x[6]),f0(x[7]),f0(x[8]),f0(x[9]),f0(x[10])] for x in ooo])
                    alll[dd[0]]=ooo
                    
            #if ooo[0][0]!=AA or ooo[-1][0]!=ZZ:
                #continue

            if dd[0]=="sz.003043":
                print("--------===========")
        
            #if (lenn:=len(ooo))>=abs(s) and ooo[s][0]==ooo_A[s][0] and ooo[-lenn][0]==ooo_A[-lenn][0] and ooo[-1][0]==ooo_A[-1][0] and 5<=ooo[-1][2]<=50:
            if (lenn:=len(ooo))>=abs(s) and ooo[s][0]==ooo_A[s][0]:
                if s==-1:
                    #AAVV=sum([f0(x[7]) for x in ooo[s-6:]])  # 包括s日的振幅
                    #AAVV=sum([abs(f0(x[8])) for x in ooo[s-6:]])  # 包括s日的涨跌幅  ========
                    AAVV=sum([x[8] for x in ooo[s-6:]])  # 包括s日的涨跌幅
                else:
                    #AAVV=sum([f0(x[7]) for x in ooo[s-6:s+1]])  # 包括s日的振幅
                    #AAVV=sum([abs(f0(x[8])) for x in ooo[s-6:s+1]])  # 包括s日的涨跌幅  ========
                    AAVV=sum([x[8] for x in ooo[s-6:s+1]])  # 包括s日的涨跌幅
                rrr_AAVV.append([dd[0], AAVV])
                
                if s==-1:
                    amountt=sum([x[6] for x in ooo[s-7:]])  # 包括s日的交易额，统计后8日额最佳 s-7
                else:
                    amountt=sum([x[6] for x in ooo[s-7:s+1]])  # 包括s日的交易额，统计后8日额最佳 s-7
                rrr_amount.append([dd[0], amountt])

                if s==-1:
                    turnn=sum([x[10] for x in ooo[s-6:]])  # 包括s日的换手率
                else:
                    turnn=sum([x[10] for x in ooo[s-6:s+1]])  # 包括s日的换手率
                rrr_turn.append([dd[0], turnn])

                if ooo[s][10]!=0:
                    capp=ooo[s][2]*(ooo[s][5]*100/ooo[s][10])  # s日的市值
                else:
                    capp=0
                rrr_cap.append([dd[0], capp])
                
                #if (f12:=ooo[s][8])>0:  # 涨跌幅
                if (f12:=ooo[s][2]-ooo[s][1])>0:  # 收盘-开盘
                    rrr2["A"]+=1
                elif f12<0:
                    rrr2["V"]+=1
                else:
                    rrr2["O"]+=1

##                #if (f12:=ooo[s+1][8])>0:  # 涨跌幅
##                if (f12:=ooo[s+1][2]-ooo[s+1][1])>0:  # 收盘-开盘  [次日的]===============    -1502全测时使用
##                    rrr3["A"]+=1
##                elif f12<0:
##                    rrr3["V"]+=1
##                else:
##                    rrr3["O"]+=1

                n=0
                x=float("-inf")
                for oo in ooo[s::-1]:  #==========正常
                #for oo in ooo[s-1::-1]:
                    if f0(oo[1])==0:
                        continue
                    #if oo[8]<0 and oo[8]>x:  # 加速下跌  #====================正常
                    if (z21:=f0(oo[2])/f0(oo[1])-1)<0 and z21>x:  #--------------------最佳,用这个
                    #if (z21:=f0(oo[2])/f0(oo[1])-1)<0:  #--------------------连续收-开下跌
                    #if oo[8]<0:  # 连续下跌  #--------------
                        n+=1
                        #x=oo[8]  #====================正常
                        x=z21  #--------------------最佳,用这个
                        #if n>=2:
                            #break
                    else:
                        break

                try:
                    #if n>=3:  #加速下跌超过3天
                    #if n>=3 and ooo[-n+s][0]==ooo_A[-n+s][0] and ooo[-1][0]==ooo_A[-1][0]:
                    #if n>=3 and f0(ooo[-n+s-1][8])>0 and ooo[-n+s][0]==ooo_A[-n+s][0] and ooo[-1][0]==ooo_A[-1][0] and f0(ooo[s][8])<0:
                    #if n>=3 and ooo[-n+s][8]>0 and ooo[-n+s][0]==ooo_A[-n+s][0] and ooo[-1][0]==ooo_A[-1][0]:  # 第二重要
                    #if n>=3 and ooo[-n+s][0]==ooo_A[-n+s][0] and ooo[-1][0]==ooo_A[-1][0]:  # 第二重要
                    #if n>=2 and ooo[-n+s][0]==ooo_A[-n+s][0] and ooo[-1][0]==ooo_A[-1][0] and sum([1 if x[8]>0 else 0 for x in ooo[s-6:s+1]])>=4:  # 第一重要
                    if n>=2 and ooo[-n+s][0]==ooo_A[-n+s][0] and ooo[-1][0]==ooo_A[-1][0]:  # 第一重要***********
                        #and any([1 if f0(x[8])>9.8 else 0 for x in ooo[-7+s:s]]):  #====================
                    #if n>=3 and (f0(ooo[-n+s][2])/f0(ooo[-n+s][1])-1)>0:  #--------------------
                        EE=sum([abs(x[8]) for x in ooo])/lenn
                        if ooo[s+1][4]<=ooo[s+1][2]:
                            BUY=1
                        else:
                            BUY=0

                        if s<-1:
                            if ooo[s+1][1]==0:
                                CO=0
                            else:
                                CO=round(ooo[s+1][2]*100/ooo[s+1][1]-100,2)  # 按当日收盘比开盘计算收益 ===========
                                #CO=round(ooo[s+2][1]*100/ooo[s+1][1]-100,2)  # 按第二天开盘比今日开盘

                                C1=round(ooo[s+2][2]*100/ooo[s+1][1]-100,2)  # 按第二天收盘比今日开盘

##                                if ooo[s+2][1]>=ooo[s+1][2]:  # 如果第二天的开盘大于等于昨天的收盘就卖出
##                                    C1=round(ooo[s+2][1]*100/ooo[s+1][1]-100,2)  # 按第二天开盘比今日开盘
##                                else:
##                                    if ooo[s+2][3]>=ooo[s+1][2]:  #如果第二天最高点大于昨天收盘
##                                        C1=round((ooo[s+1][2])*100/ooo[s+1][1]-100,2)  # 按当日收盘比开盘计算收益
##                                    else:
##                                        C1=round(ooo[s+2][2]*100/ooo[s+1][1]-100,2)  # 按第二天收盘比今日开盘
                        else:
                            CO=0
                            
                        if dd[0] in ddd3:
                            if s<-1:
                                rrr.append([dd[0], dd[1], ddd2[dd[0]], n, ooo[s][0], ooo[s][2], ooo[s][8], 1, ooo[s+1][8], amountt, EE, capp, turnn, AAVV, BUY, CO, C1])
                            else:
                                rrr.append([dd[0], dd[1], ddd2[dd[0]], n, ooo[s][0], ooo[s][2], ooo[s][8], 1, 0, amountt, EE, capp, turnn, AAVV, BUY, 0, 0])
                        else:
                            if s<-1:
                                rrr.append([dd[0], dd[1], ddd2[dd[0]], n, ooo[s][0], ooo[s][2], ooo[s][8], 0, ooo[s+1][8], amountt, EE, capp, turnn, AAVV, BUY, CO, C1])
                            else:
                                rrr.append([dd[0], dd[1], ddd2[dd[0]], n, ooo[s][0], ooo[s][2], ooo[s][8], 0, 0, amountt, EE, capp, turnn, AAVV, BUY, 0, 0])
                except Exception as e:
                    print(e)


    print("\r\n说明：1、数据使用为不复权数据；2、当日涨跌幅度=(当日收盘-前日收盘)/前日收盘*100%；3、每年分红股票（●）为至少上市4年，最多1年没有分红（除权）的股票；4、新上市股票不定期更新。\r\n")
    print("(-10->-9: -1.428) (●-9->-8: 0.844) (●-8->-7: 0.645) (●-7->-6: 0.498) (-6->-5: -0.049) (-5->-4: -0.034) (-4->-3: -0.088) (-3->-2: -0.013) (-2->-1: -0.195) (●-1->0: 1.157)")


    if "sh.000001" in alll.keys():
        ooo=alll["sh.000001"]
    elif os.path.exists(f'data/k_line_d_东方财富_前复权/sh.000001_d.txt'):
        with open(f'data/k_line_d_东方财富_前复权/sh.000001_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
            ooo=json.loads(f.read())[-1600:]  #=============控制此处，减小内存占用
            ooo=list([[x[0],f0(x[1]),f0(x[2]),f0(x[3]),f0(x[4]),f0(x[5]),f0(x[6]),f0(x[7]),f0(x[8]),f0(x[9]),f0(x[10])] for x in ooo])
            alll[dd[0]]=ooo
    if s<-1:
        print(f"\r\n上证：{ooo[s][0]}，【{ooo[s][2]}】({ooo[s][6]/100000000:.0f}亿)，{ooo[s][8]:.2f}%    {ooo[s+1][0]}，\
【{ooo[s+1][2]}】({ooo[s+1][6]/100000000:.0f}亿)，{ooo[s+1][8]:.2f}%")
    else:
        print(f"上证：{ooo[s][0]}，【{ooo[s][2]}】({ooo[s][6]/100000000:.0f}亿)，{ooo[s][8]:.2f}%")
    #====================
    if "sz.399001" in alll.keys():
        ooo=alll["sz.399001"]
    elif os.path.exists(f'data/k_line_d_东方财富_前复权/sz.399001_d.txt'):
        with open(f'data/k_line_d_东方财富_前复权/sz.399001_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
            ooo=json.loads(f.read())[-1600:]  #=============控制此处，减小内存占用
            ooo=list([[x[0],f0(x[1]),f0(x[2]),f0(x[3]),f0(x[4]),f0(x[5]),f0(x[6]),f0(x[7]),f0(x[8]),f0(x[9]),f0(x[10])] for x in ooo])
            alll[dd[0]]=ooo
    if s<-1:
        print(f"深证：{ooo[s][0]}，【{ooo[s][2]}】({ooo[s][6]/100000000:.0f}亿)，{ooo[s][8]:.2f}%    {ooo[s+1][0]}，\
【{ooo[s+1][2]}】({ooo[s+1][6]/100000000:.0f}亿)，{ooo[s+1][8]:.2f}%")
    else:
        print(f"深证：{ooo[s][0]}，【{ooo[s][2]}】({ooo[s][6]/100000000:.0f}亿)，{ooo[s][8]:.2f}%")
    #====================
    if "sz.399006" in alll.keys():
        ooo=alll["sz.399006"]
    elif os.path.exists(f'data/k_line_d_东方财富_前复权/sz.399006_d.txt'):
        with open(f'data/k_line_d_东方财富_前复权/sz.399006_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
            ooo=json.loads(f.read())[-1600:]  #=============控制此处，减小内存占用
            ooo=list([[x[0],f0(x[1]),f0(x[2]),f0(x[3]),f0(x[4]),f0(x[5]),f0(x[6]),f0(x[7]),f0(x[8]),f0(x[9]),f0(x[10])] for x in ooo])
            alll[dd[0]]=ooo
    if s<-1:
        print(f"创业板：{ooo[s][0]}，【{ooo[s][2]}】({ooo[s][6]/100000000:.0f}亿)，{ooo[s][8]:.2f}%    {ooo[s+1][0]}，\
【{ooo[s+1][2]}】({ooo[s+1][6]/100000000:.0f}亿)，{ooo[s+1][8]:.2f}%")
    else:
        print(f"创业板：{ooo[s][0]}，【{ooo[s][2]}】({ooo[s][6]/100000000:.0f}亿)，{ooo[s][8]:.2f}%")
    #====================
    rrr_AV_len.append({"A":rrr2["A"],"V":rrr2["V"]})
    print(f"\r\n{rrr2}")
    if 1/2 <= rrr2["A"]/rrr2["V"] <= 1:
        print("●●●：1/2 <= A/V <=1/1")
    else:
        print("●●●PASS，应：1/2--1/1")
    #rrr=sorted(rrr, key=lambda x: x[6], reverse=False)  # 按跌幅排名
    #rrr=sorted(rrr, key=lambda x: x[6], reverse=True)  # 按跌幅排名


##    #--------------临时
##    rrr2={"A":0,"O":0,"V":0}
##    rrr_cap.sort(key=lambda x: x[1], reverse=True)
##    for uu in rrr_cap[:300]:
##        if (f12:=alll[uu[0]][s][8])>0:
##            rrr2["A"]+=1
##        elif f12<0:
##            rrr2["V"]+=1
##        else:
##            rrr2["O"]+=1
##    #=============临时结束


    #if rrr2["V"]/rrr2["A"]>1 :
    #if rrr2["V"]>=rrr2["A"]:
    rrr=sorted(rrr, key=lambda x: x[9], reverse=True)  # 按7日额排名,倒序 =========正常用,因为我们用钱来衡量收益,所以不用换手率
    #else:
        #rrr=sorted(rrr, key=lambda x: x[9], reverse=False)
        
    #rrr=sorted(rrr, key=lambda x: x[9], reverse=False)  # 按7日额排名
    #rrr=sorted(rrr, key=lambda x: x[13], reverse=True)  # 按7日|AAVV|排序,倒序
    #rrr=sorted(rrr, key=lambda x: x[3], reverse=True)  # 按下跌天数排名,倒序 =========
    #rrr=sorted(rrr, key=lambda x: x[12], reverse=True)  # 按换手率排名,倒序 =========
    #rrr=sorted(rrr, key=lambda x: x[12], reverse=False)  # 按换手率排名,正序 =========
    #rrr=sorted(rrr, key=lambda x: x[11], reverse=False)  # 按市值排序

    if rrr2["A"]>rrr2["V"]:
        oth1+=len(rrr)
        oth2+=1

    if rrr2["A"]<rrr2["V"]:
        rrr_len.append(len(rrr))
    
    rrr_AAVV.sort(key=lambda x: x[1], reverse=True)
    rrr_amount.sort(key=lambda x: x[1], reverse=True)
    rrr_cap.sort(key=lambda x: x[1], reverse=True)
    rrr_turn.sort(key=lambda x: x[1], reverse=True)
    print(f"共：{len(rrr_amount)}只股票，●●●：{len(rrr_amount)//5}-{len(rrr_amount)//4}")

    print("\r\n========加速下跌（每天下跌均高于前一天）========\r\n")
    nn=0
    ss=0
    ss2=0
    t_n=0

##    if (rrr2["A"]/rrr2["V"] < 3/7 or 7/3 <= rrr2["A"]/rrr2["V"]) and (rrr3["A"]/rrr3["V"] < 3/7 or 7/3 <= rrr3["A"]/rrr3["V"]):
##        chongfu+=1
        
    for rr in rrr:
    #for rr in rrr[:len(rrr)//2]:
        #if rr[7]==1 and rrr_amount.index([rr[0], rr[9]])+1<1000:  # **
        #if rrr_amount.index([rr[0], rr[9]])+1<1000:  # 7日成交额 **
        #if rrr_turn.index([rr[0], rr[12]])+1<1000:  # 7日换手率
        #if rr[7]==1:
        #if rrr_amount.index([rr[0], rr[9]])+1<1000 and rrr_turn.index([rr[0], rr[12]])+1<1000:
        #if rr[5]>=10.0 and rr[5]<=60 and 500<=rrr_amount.index([rr[0], rr[9]])+1<900:
        #if rrr_amount.index([rr[0], rr[9]])+1 < rrr_cap.index([rr[0], rr[11]])+1 and rrr_amount.index([rr[0], rr[9]])+1 < 1000:
        #if rr[1].find("ST")==-1 and rr[6]>=-5 and 10<=rr[5]<50 and rrr_cap.index([rr[0], rr[11]])+1<1000:
        #if rr[1].find("ST")==-1 and rrr_cap.index([rr[0], rr[11]])+1<1000:
        #if 1:
        #if -0.6<rr[6]<-0 and rr[1].find("ST")==-1 and 8<=rr[5]<=60:
        #if 0<=rrr_amount.index([rr[0], rr[9]])<600 and rr[1].find("ST")==-1 and 6<=rr[5]<=40 and -9<rr[6]<-0:  #7日额 ==============
        #if t_n<1 and 0<=rrr_turn.index([rr[0], rr[12]])<50 and rr[1].find("ST")==-1 and 5<=rr[5]<=50 and -9.8<rr[6]<-0 and 0<=rrr_amount.index([rr[0], rr[9]])<50:  #7日换手率
        #if 0<=rrr_amount.index([rr[0], rr[9]])<600 and rr[1].find("ST")==-1 and 6<=rr[5]<=40 and -9<rr[6]<-0 and 0<=rrr_cap.index([rr[0], rr[11]])<100:  #7日额，市值100以内不好的
        if t_n<4 and rr[1].find("ST")==-1 and 5<=rr[5]<=50 and -9.8<rr[6]<-0 and rrr_cap.index([rr[0], rr[11]])<float('inf'):  #========正常
        #if 0<=rrr_AAVV.index([rr[0], rr[13]])<600 and rr[1].find("ST")==-1 and 6<=rr[5]<=40 and -9<rr[6]<-0:
        #if t_n<4 and rr[1].find("ST")==-1 and 5<=rr[5]<=50 and -9<rr[6]<-0 and 0<=rrr_amount.index([rr[0], rr[9]])<600:
        #if t_n<20 and rr[1].find("ST")==-1 and 5<=rr[5]<=50 and -9.8<rr[6]<0:  # 平常用这个
        #if t_n<3 and rr[1].find("ST")==-1 and 6<=rr[5]<=40 and -9<rr[6]<-0 and 0<=rrr_AAVV.index([rr[0], rr[13]])<600:
            nn+=1
            ss+=rr[6]  # 当日涨跌幅
            #ss2+=rr[8]  # 下一日涨跌幅
            #if rrr_amount.index([rr[0], rr[9]])<200:
            #if rrr2["A"]<rrr2["V"]:
            if 1==1:  #=============1501测试时改为：1==2
            #if rrr3["A"]/rrr3["V"] < 3/7 or 7/3 <= rrr3["A"]/rrr3["V"]:  # -1502测试时使用 大跌大涨
                ss2+=rr[15]
            else:
                ss2+=rr[16]  # C1 按收盘价下单,次日盘中不能成交,则收盘卖出,通过计算,次日收盘成交收益最高
            t_n+=1
            if rr[0][:6]=="sh.688":
                print(f"{rr[0]} {rr[1]:　^4}({rr[2]:　^4}) 加速跌:{rr[3]}天, {rr[4]}日, 收:{rr[5]:7.2f}元, 涨:【{rr[6]:6.2f}%】,次日:【{rr[8]:6.2f}%】,\
8日额:{rrr_amount.index([rr[0], rr[9]])+1:4}, 7日换手:{rrr_turn.index([rr[0], rr[12]])+1:4} 市值:{rrr_cap.index([rr[0], rr[11]])+1:4} \
平均AV:{rr[10]:.2f}%, 7(AV):{rrr_AAVV.index([rr[0], rr[13]])+1:4} {rr[13]:6.2f} {'●' if rr[7]==1 else ''} 科创板")
            elif rr[0][:4]=="sz.3":
                print(f"{rr[0]} {rr[1]:　^4}({rr[2]:　^4}) 加速跌:{rr[3]}天, {rr[4]}日, 收:{rr[5]:7.2f}元, 涨:【{rr[6]:6.2f}%】,次日:【{rr[8]:6.2f}%】,\
8日额:{rrr_amount.index([rr[0], rr[9]])+1:4}, 7日换手:{rrr_turn.index([rr[0], rr[12]])+1:4} 市值:{rrr_cap.index([rr[0], rr[11]])+1:4} \
平均AV:{rr[10]:.2f}%, 7(AV):{rrr_AAVV.index([rr[0], rr[13]])+1:4} {rr[13]:6.2f} {'●' if rr[7]==1 else ''} 创业板")
            else:
                print(f"{rr[0]} {rr[1]:　^4}({rr[2]:　^4}) 加速跌:{rr[3]}天, {rr[4]}日, 收:{rr[5]:7.2f}元, 涨:【{rr[6]:6.2f}%】,次日:【{rr[8]:6.2f}%】,\
8日额:{rrr_amount.index([rr[0], rr[9]])+1:4}, 7日换手:{rrr_turn.index([rr[0], rr[12]])+1:4} 市值:{rrr_cap.index([rr[0], rr[11]])+1:4} \
平均AV:{rr[10]:.2f}%, 7(AV):{rrr_AAVV.index([rr[0], rr[13]])+1:4} {rr[13]:6.2f} {'●' if rr[7]==1 else ''}")

    if nn==0 or len(rrr)==0:
        print(f"\r\n以上共：{nn}条  涨跌累加：{ss:.2f}%  下一日涨跌累加：{ss2:.2f}%")
        print(f"\r\n共：{len(rrr)}条  涨跌累加：{sum([x[6] for x in rrr]):.2f}%  下一日涨跌累加：{sum([x[8] for x in rrr]):.2f}%")
    else:
        print(f"\r\n以上共：{nn}条  涨跌累加：{ss:.2f}%  下一日涨跌累加：{ss2:.2f}%  平均：{ss2/nn:.2f}%")
        #if rrr2["A"]<rrr2["V"]:  # ==============
        #if rrr2["A"]>rrr2["V"]:  # 000000000000
        #if 6/4 < rrr2["A"]/rrr2["V"] <= 7/3 or 0 < rrr2["A"]/rrr2["V"] <=4/6:
        #if 7/3 < rrr2["A"]/rrr2["V"] <= 8/2 or 0 < rrr2["A"]/rrr2["V"] <=4/6:  # ===========正常用
        if rrr2["A"]/rrr2["V"] < 3/7 or 7/3 <= rrr2["A"]/rrr2["V"]:  # 经全测,用这个参数
        #if 1:
            print("----------符合计算-----------")
            nnn+=1
            mmm+=ss2/nn
            #mmm+=ss2/4
            rrr_AV.append([mmm,rr[4]])
        print(f"共：{nnn} 天，累计平均：{mmm}")
        print(f"\r\n共：{len(rrr)}条  涨跌累加：{sum([x[6] for x in rrr]):.2f}%  下一日涨跌累加：{sum([x[8] for x in rrr]):.2f}%  平均：{sum([x[8] for x in rrr])/len(rrr):.2f}%")


##print("\033[31mHello, World!\033[0m")
##print("\033[32mHello, World!\033[0m")

##while (x:=input("输入'x'退出：")):
##    if x=="x" or x=="X":
##        print("--end--")
##        break

    
print(oth1,oth2)
print(rrr_len)
print(len(rrr_len))
print(sum(rrr_len))
print("---------------")
rrr_AV=[[round(x[0],2),x[1]] for x in rrr_AV]
print(rrr_AV)
print(len(rrr_AV))
#print(chongfu)
print("--end--")
