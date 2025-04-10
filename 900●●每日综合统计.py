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


##  日期【0】  昨收【1】  开盘【2】  最低【3】  最高【4】  收盘【5】  振幅【6】  涨跌【7】
##  成交量【8】  成交额【9】  换手率【10】  （收开【11】  昨均【12】  均价【13】  均幅【14】  市值【15】）
##  说明：振幅=最高*100/最低-100，收开=（收盘*100/开盘）-100
##  昨均=昨成交额/昨成交量，均幅=（（成交额/成交量）*100）/昨均-100
##  市值=收盘*（成交量*100）/换手率


f0=lambda x: 0.0 if x=="" else float(x)


rrr1=[]  # 创新高
rrr2=[]  # 创新低
rrr3=[]  # 连续上涨
rrr4=[]  # 连续下跌
rrr5=[]  # 加速上涨
rrr6=[]  # 加速下跌
rrr7=[]  # 区间震荡 1%
rrr8=[]  # 区间震荡 2%
rrr9=[]  # 区间震荡 3%
rrr_d={}

a="d"
today="2023-12-11"
for dd in ddd:
    #print(dd[0])
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0] in ddd3 and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1":
        #print(dd)
        uuu=[]
        if os.path.exists(f'data/K_line_{a}_前复权_计算获得/{dd[0]}_{a}.txt'):  #使用不复权数据
            with open(f'data/K_line_{a}_前复权_计算获得/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                uuu=json.loads(f.read())

        if uuu!=[] and len(uuu)>5:
            if uuu[-1][0] in rrr_d.keys():
                rrr_d[uuu[-1][0]]+=1
            else:
                rrr_d[uuu[-1][0]]=1

            # 创新高
            if uuu[-1][4]==max([x[4] for x in uuu]):
                if uuu[-1][0]==today:
                    rrr1.append([dd, uuu[-1][5], uuu[-1][7]])

            # 创新低
            if uuu[-1][3]==min([x[3] for x in uuu]):
                if uuu[-1][0]==today:
                    rrr2.append([dd, uuu[-1][5], uuu[-1][7]])

            # 连续上涨
            n=0
            for uu in uuu[::-1]:
                if uu[7]>0:
                    n+=1
                else:
                    break
            if uuu[-1][0]==today:
                rrr3.append([dd, uuu[-1][5], uuu[-1][7], n])

            # 连续下跌
            n=0
            for uu in uuu[::-1]:
                if uu[7]<0:
                    n+=1
                else:
                    break
            if uuu[-1][0]==today:
                rrr4.append([dd, uuu[-1][5], uuu[-1][7], n])

            # 加速上涨
            n=0
            x=1000
            for uu in uuu[::-1]:
                if uu[7]>0 and uu[7]<x:
                    n+=1
                    x=uu[7]
                else:
                    break
            if uuu[-1][0]==today:
                rrr5.append([dd, uuu[-1][5], uuu[-1][7], n])
            
            # 加速下跌
            n=0
            x=-1000
            for uu in uuu[::-1]:
                if uu[7]<0 and uu[7]>x:
                    n+=1
                    x=uu[7]
                else:
                    break
            if uuu[-1][0]==today:
                rrr6.append([dd, uuu[-1][5], uuu[-1][7], n])

            # 区间震荡
            vvv=[x[13] for x in uuu if x[13]>0]
            lenn=len(vvv)
            # 区间震荡 1%
            for i in range(1,lenn):
                if max(vvv[-i:])/min(vvv[-i:])>1.01:
                    if uuu[-1][0]==today:
                        rrr7.append([dd, uuu[-1][5], uuu[-1][7], i])
                    break

            # 区间震荡 2%
            for i in range(1,lenn):
                if max(vvv[-i:])/min(vvv[-i:])>1.02:
                    if uuu[-1][0]==today:
                        rrr8.append([dd, uuu[-1][5], uuu[-1][7], i])
                    break

            # 区间震荡 3%
            for i in range(1,lenn):
                if max(vvv[-i:])/min(vvv[-i:])>1.03:
                    if uuu[-1][0]==today:
                        rrr9.append([dd, uuu[-1][5], uuu[-1][7], i])
                    break


##print(f"\n说明：1、数据均使用不复权数据；2、T为涨停天数占比；3、E为当前收盘价在历史最低与最高中位置，最低与最高之间100等分。")
rrr_d=sorted(rrr_d.items(), key=lambda x: x[1], reverse=True)
s=rrr_d[0][0].split("-")
datee=f"{s[0]}年{int(s[1])}月{int(s[2])}日"
#datee="2023年3月24日"
print(f"\n--------------------\n{datee} 盘中创【新高】股票：")
for rr in rrr1:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%")

print(f"\n--------------------\n{datee} 盘中创【新低】股票：")
for rr in rrr2:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%")

print(f"\n--------------------\n{datee} 收盘【连续上涨】股票(前10)：")
rrr3=sorted(rrr3, key=lambda x: x[3], reverse=True)
for rr in rrr3[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[3]}天")

print(f"\n--------------------\n{datee} 收盘【连续下跌】股票(前10)：")
rrr4=sorted(rrr4, key=lambda x: x[3], reverse=True)
for rr in rrr4[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[3]}天")

print(f"\n--------------------\n{datee} 收盘【加速上涨】股票(前10)：")
rrr5=sorted(rrr5, key=lambda x: x[3], reverse=True)
for rr in rrr5[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[3]}天")

print(f"\n--------------------\n{datee} 收盘【加速下跌】股票(前10)：")
rrr6=sorted(rrr6, key=lambda x: x[3], reverse=True)
for rr in rrr6[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[3]}天")

print(f"\n--------------------\n{datee} 【区间震荡1%】股票(前10)：")
rrr7=sorted(rrr7, key=lambda x: x[3], reverse=True)
for rr in rrr7[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[3]}天")

print(f"\n--------------------\n{datee} 【区间震荡2%】股票(前10)：")
rrr8=sorted(rrr8, key=lambda x: x[3], reverse=True)
for rr in rrr8[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[3]}天")

print(f"\n--------------------\n{datee} 【区间震荡3%】股票(前10)：")
rrr9=sorted(rrr9, key=lambda x: x[3], reverse=True)
for rr in rrr9[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[3]}天")

print("--end--")
