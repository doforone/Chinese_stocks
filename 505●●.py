# 白点数据，运行环境Python3.8
# -*- coding: UTF-8 -*-

#### 日K线参数名称及定义 ####
##"2023-07-27,1836.00,1838.03,1854.79,1828.70,20340,3749635290.00,1.43,0.52,9.48,0.16"
##茅台日期         开盘        收盘         最高        最低        成交量（手）成交额（元）振幅 涨跌幅 涨跌 流通换手率
##   0              1           2            3          4            5           6           7    8      9     10

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


f0=lambda x: 0.0 if x=="" else float(x)


def get_english_len(s):
    length = 0
    for ch in s:
        if '\u4e00' <= ch <= '\u9fff':
            length += 2  # 中文字符占两个字节
        else:
            length += 1  # 英文字符占一个字节
    return length


nnn=0  # 次数累积
mmm=0  # 胜率累加
#s = -2  # 一般为-1，不得大于-1
for s in [-2,-1]:
    print(f"****************************************({s})****************************************")
    rrr=[]
    rrr2={"A":0,"O":0,"V":0}  # s当日上涨与下跌股票数量
    rrr_amount=[]  # 统计股票s及之前一段时间内的交易额，包括s日
    rrr_cap=[]  # 统计s日的市值
    rrr_turn=[]  # 统计股票s及之前一段时间内的换手率，包括s日
    
    for dd in ddd:
        if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
            #print(dd)
            if os.path.exists(f'data/k_line_d_东方财富/{dd[0]}_d.txt'):
                with open(f'data/k_line_d_东方财富/{dd[0]}_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                    ooo=json.loads(f.read())

                if (lenn:=len(ooo))>=abs(s):
                    if s==-1:
                        amountt=sum([f0(x[6]) for x in ooo[s-6:]])  # 包括s日的交易额
                    else:
                        amountt=sum([f0(x[6]) for x in ooo[s-6:s+1]])  # 包括s日的交易额
                    rrr_amount.append([dd[0], amountt])

                    if s==-1:
                        turnn=sum([f0(x[10]) for x in ooo[s-6:]])  # 包括s日的换手率
                    else:
                        turnn=sum([f0(x[10]) for x in ooo[s-6:s+1]])  # 包括s日的换手率
                    rrr_turn.append([dd[0], turnn])

                    if f0(ooo[s][10])!=0:
                        capp=f0(ooo[s][2])*(f0(ooo[s][5])*100/f0(ooo[s][10]))  # s日的市值
                    else:
                        capp=0
                    rrr_cap.append([dd[0], capp])
                    
                    if (f12:=f0(ooo[s][8]))>0:
                        rrr2["A"]+=1
                    elif f12<0:
                        rrr2["V"]+=1
                    else:
                        rrr2["O"]+=1
                        
                    n=0
                    x=-1000
                    for oo in ooo[s::-1]:
                        if f0(oo[8])<0 and f0(oo[8])>x:  # 加速下跌  #====================
                        #if (z21:=f0(oo[2])/f0(oo[1])-1)<0 and z21>x:  #--------------------
                            n+=1
                            x=f0(oo[8])  #====================
                            #x=z21  #--------------------
                        else:
                            break

                    #if n>=3:  #加速下跌超过3天
                    if n>=3 and f0(ooo[-n+s][8])>0:  #====================
                    #if n>=3 and (f0(ooo[-n+s][2])/f0(ooo[-n+s][1])-1)>0:  #--------------------
                        EE=sum([abs(f0(x[8])) for x in ooo])/lenn
                        if dd[0] in ddd3:
                            if s<-1:
                                rrr.append([dd[0], dd[1], ddd2[dd[0]], n, ooo[s][0], f0(ooo[s][2]), f0(ooo[s][8]), 1, f0(ooo[s+1][8]), amountt, EE, capp, turnn])
                            else:
                                rrr.append([dd[0], dd[1], ddd2[dd[0]], n, ooo[s][0], f0(ooo[s][2]), f0(ooo[s][8]), 1, 0, amountt, EE, capp, turnn])
                        else:
                            if s<-1:
                                rrr.append([dd[0], dd[1], ddd2[dd[0]], n, ooo[s][0], f0(ooo[s][2]), f0(ooo[s][8]), 0, f0(ooo[s+1][8]), amountt, EE, capp, turnn])
                            else:
                                rrr.append([dd[0], dd[1], ddd2[dd[0]], n, ooo[s][0], f0(ooo[s][2]), f0(ooo[s][8]), 0, 0, amountt, EE, capp, turnn])


    print("\r\n说明：1、数据使用为不复权数据；2、当日涨跌幅度=(当日收盘-前日收盘)/前日收盘*100%；3、每年分红股票（●）为至少上市4年，最多1年没有分红（除权）的股票；4、新上市股票不定期更新。\r\n")
    print("(-10->-9: -1.428) (●-9->-8: 0.844) (●-8->-7: 0.645) (●-7->-6: 0.498) (-6->-5: -0.049) (-5->-4: -0.034) (-4->-3: -0.088) (-3->-2: -0.013) (-2->-1: -0.195) (●-1->0: 1.157)")


    if os.path.exists(f'data/k_line_d_东方财富/sh.000001_d.txt'):  #使用不复权数据，上证
        with open(f'data/k_line_d_东方财富/sh.000001_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
            ooo=json.loads(f.read())
        if s<-1:
            print(f"\r\n上证：{ooo[s][0]}，【{ooo[s][2]}】，{f0(ooo[s][8]):.2f}%    {ooo[s+1][0]}，【{ooo[s+1][2]}】，{f0(ooo[s+1][8]):.2f}%")
        else:
            print(f"上证：{ooo[s][0]}，【{ooo[s][2]}】，{f0(ooo[s][8]):.2f}%")
    #====================
    if os.path.exists(f'data/k_line_d_东方财富/sz.399001_d.txt'):  #使用不复权数据，深证
        with open(f'data/k_line_d_东方财富/sz.399001_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
            ooo=json.loads(f.read())
        if s<-1:
            print(f"深证：{ooo[s][0]}，【{ooo[s][2]}】，{f0(ooo[s][8]):.2f}%    {ooo[s+1][0]}，【{ooo[s+1][2]}】，{f0(ooo[s+1][8]):.2f}%")
        else:
            print(f"深证：{ooo[s][0]}，【{ooo[s][2]}】，{f0(ooo[s][8]):.2f}%")
    #====================
    if os.path.exists(f'data/k_line_d_东方财富/sz.399006_d.txt'):  #使用不复权数据，创业板
        with open(f'data/k_line_d_东方财富/sz.399006_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
            ooo=json.loads(f.read())
        if s<-1:
            print(f"创业板：{ooo[s][0]}，【{ooo[s][2]}】，{f0(ooo[s][8]):.2f}%    {ooo[s+1][0]}，【{ooo[s+1][2]}】，{f0(ooo[s+1][8]):.2f}%")
        else:
            print(f"创业板：{ooo[s][0]}，【{ooo[s][2]}】，{f0(ooo[s][8]):.2f}%")
    #====================
        
    print(f"\r\n{rrr2}")
    if 1/2 <= rrr2["A"]/rrr2["V"] <= 1:
        print("●●●：1/2 <= A/V <=1/1")
    else:
        print("●●●PASS，应：1/2--1/1")
    #rrr=sorted(rrr, key=lambda x: x[6], reverse=False)  # 按跌幅排名
    rrr=sorted(rrr, key=lambda x: x[9], reverse=True)  # 按7日额排名

    rrr_amount.sort(key=lambda x: x[1], reverse=True)
    rrr_cap.sort(key=lambda x: x[1], reverse=True)
    rrr_turn.sort(key=lambda x: x[1], reverse=True)
    print(f"共：{len(rrr_amount)}只股票，●●●：{len(rrr_amount)//5}-{len(rrr_amount)//4}")

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
        #if rr[5]>=10.0 and rr[5]<=60 and 500<=rrr_amount.index([rr[0], rr[9]])+1<900:
        #if rrr_amount.index([rr[0], rr[9]])+1 < rrr_cap.index([rr[0], rr[11]])+1 and rrr_amount.index([rr[0], rr[9]])+1 < 1000:
        #if rr[1].find("ST")==-1 and rr[6]>=-5 and 10<=rr[5]<50 and rrr_cap.index([rr[0], rr[11]])+1<1000:
        #if rr[1].find("ST")==-1 and rrr_cap.index([rr[0], rr[11]])+1<1000:
        if 1:
        #if -0.6<rr[6]<-0 and rr[1].find("ST")==-1 and 8<=rr[5]<=60:
        #if 0<=rrr_amount.index([rr[0], rr[9]])<600 and rr[1].find("ST")==-1 and 8<=rr[5]<=60 and -9<rr[6]<-0:
            nn+=1
            ss+=rr[6]
            ss2+=rr[8]
            if rr[0][:6]=="sh.688":
                print(f"{rr[0]} {rr[1]:　^4}（{rr[2]:　^4}） 加速下跌：{rr[3]}天，截止：{rr[4]}，收盘：{rr[5]:7.2f}元，涨跌：【{rr[6]:6.2f}%】，下一日：【{rr[8]:6.2f}%】  \
7日额：{rrr_amount.index([rr[0], rr[9]])+1:4}, 7日换手：{rrr_turn.index([rr[0], rr[12]])+1:4}  市值：{rrr_cap.index([rr[0], rr[11]])+1:4}  \
平均AV：{rr[10]:.2f}%  {'●' if rr[7]==1 else ''}  科创板")
            elif rr[0][:4]=="sz.3":
                print(f"{rr[0]} {rr[1]:　^4}（{rr[2]:　^4}） 加速下跌：{rr[3]}天，截止：{rr[4]}，收盘：{rr[5]:7.2f}元，涨跌：【{rr[6]:6.2f}%】，下一日：【{rr[8]:6.2f}%】  \
7日额：{rrr_amount.index([rr[0], rr[9]])+1:4}, 7日换手：{rrr_turn.index([rr[0], rr[12]])+1:4}  市值：{rrr_cap.index([rr[0], rr[11]])+1:4}  \
平均AV：{rr[10]:.2f}%  {'●' if rr[7]==1 else ''}  创业板")
            else:
                print(f"{rr[0]} {rr[1]:　^4}（{rr[2]:　^4}） 加速下跌：{rr[3]}天，截止：{rr[4]}，收盘：{rr[5]:7.2f}元，涨跌：【{rr[6]:6.2f}%】，下一日：【{rr[8]:6.2f}%】  \
7日额：{rrr_amount.index([rr[0], rr[9]])+1:4}, 7日换手：{rrr_turn.index([rr[0], rr[12]])+1:4}  市值：{rrr_cap.index([rr[0], rr[11]])+1:4}  \
平均AV：{rr[10]:.2f}%  {'●' if rr[7]==1 else ''}")

    if nn==0 or len(rrr)==0:
        print(f"\r\n以上共：{nn}条  涨跌累加：{ss:.2f}%  下一日涨跌累加：{ss2:.2f}%")
        print(f"\r\n共：{len(rrr)}条  涨跌累加：{sum([x[6] for x in rrr]):.2f}%  下一日涨跌累加：{sum([x[8] for x in rrr]):.2f}%")
    else:
        print(f"\r\n以上共：{nn}条  涨跌累加：{ss:.2f}%  下一日涨跌累加：{ss2:.2f}%  平均：{ss2/nn:.2f}%")
##        #if rrr2["A"]<rrr2["V"]:
##        if 1/2 <= rrr2["A"]/rrr2["V"] <= 1:
##        #if 1:
##            nnn+=1
##            mmm+=ss2/nn
##        print(f"共：{nnn} 次，累计平均：{mmm}")
        print(f"\r\n共：{len(rrr)}条  涨跌累加：{sum([x[6] for x in rrr]):.2f}%  下一日涨跌累加：{sum([x[8] for x in rrr]):.2f}%  平均：{sum([x[8] for x in rrr])/len(rrr):.2f}%")


##print("\033[31mHello, World!\033[0m")
##print("\033[32mHello, World!\033[0m")
##
##while (x:=input("输入X退出：")):
##    if x=="x" or x=="X":
##        print("--end--")
##        break

print("--end--")
