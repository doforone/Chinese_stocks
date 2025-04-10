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
            if uuu[-1][0] in rrr_d.keys():
                rrr_d[uuu[-1][0]]+=1
            else:
                rrr_d[uuu[-1][0]]=1

##            # 通过昨日收盘价反向生成前复权数据
##            vvv=[[uuu[-1][0], uuu[-1][1], uuu[-1][2], uuu[-1][3], uuu[-1][4], uuu[-1][5]]]
##            # 以上按倒序取最后一个值
##            lenn=len(ooo)
##            s=1.0
##            for i in range(-2,-lenn-1,-1):
##                if uuu[i][5]!=uuu[i+1][1]:  # 收盘不等于下一个的昨收
##                    s*=uuu[i+1][1]/uuu[i][5]
##                vvv.append([uuu[i][0], uuu[i][1]*s, uuu[i][2]*s, uuu[i][3]*s, uuu[i][4]*s, uuu[i][5]*s])
##            
##            if dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
##                TT=round(sum(uu[7]>=9.8 for uu in uuu)*100/len(uuu),2)  # 普通版
##            else:
##                TT=round(sum(uu[7]>=19.8 for uu in uuu)*100/len(uuu),2)  # 科创板
##                
##            LL=min([x[3] for x in uuu])
##            EE=int((uuu[-1][5]-LL)*100/(max([x[4] for x in uuu])-LL))

            # 创新高
            if uuu[-1][4]==max([x[4] for x in uuu]):
##                rrr1.append([dd, uuu[-1][5], TT, EE])
                rrr1.append([dd, uuu[-1][5]])
                #print(f"创新高：{dd}")

            # 创新低
            if uuu[-1][3]==min([x[3] for x in uuu]):
##                rrr2.append([dd, uuu[-1][5], TT, EE])
                rrr2.append([dd, uuu[-1][5]])
                #print(f"创新低：{dd}")

            # 连续上涨
            n=0
            for uu in uuu[::-1]:
                if uu[7]>0:
                    n+=1
                else:
                    break
##            rrr3.append([dd, uuu[-1][5], n, TT, EE])
            rrr3.append([dd, uuu[-1][5], n])

            # 连续下跌
            n=0
            for uu in uuu[::-1]:
                if uu[7]<0:
                    n+=1
                else:
                    break
##            rrr4.append([dd, uuu[-1][5], n, TT, EE])
            rrr4.append([dd, uuu[-1][5], n])

            # 加速上涨
            n=0
            x=1000
            for uu in uuu[::-1]:
                if uu[7]>0 and uu[7]<x:
                    n+=1
                    x=uu[7]
                else:
                    break
##            rrr5.append([dd, uuu[-1][5], n, TT, EE])
            rrr5.append([dd, uuu[-1][5], n])
            
            # 加速下跌
            n=0
            x=-1000
            for uu in uuu[::-1]:
                if uu[7]<0 and uu[7]>x:
                    n+=1
                    x=uu[7]
                else:
                    break
##            rrr6.append([dd, uuu[-1][5], n, TT, EE])
            rrr6.append([dd, uuu[-1][5], n])

            # 区间震荡 1%
            vvv=[x[9]/x[8] for x in uuu if x[8]>0]
            for i in range(1,len(vvv)):
                if max(vvv[-i:])/min(vvv[-i:])>1.01:
##                    rrr7.append([dd, uuu[-1][5], i, TT, EE])
                    rrr7.append([dd, uuu[-1][5], i])
                    break

            # 区间震荡 2%
            vvv=[x[9]/x[8] for x in uuu if x[8]>0]
            for i in range(1,len(vvv)):
                if max(vvv[-i:])/min(vvv[-i:])>1.02:
##                    rrr8.append([dd, uuu[-1][5], i, TT, EE])
                    rrr8.append([dd, uuu[-1][5], i])
                    break

            # 区间震荡 3%
            vvv=[x[9]/x[8] for x in uuu if x[8]>0]
            for i in range(1,len(vvv)):
                if max(vvv[-i:])/min(vvv[-i:])>1.03:
##                    rrr9.append([dd, uuu[-1][5], i, TT, EE])
                    rrr9.append([dd, uuu[-1][5], i])
                    break


##print(f"\n说明：1、数据均使用不复权数据；2、T为涨停天数占比；3、E为当前收盘价在历史最低与最高中位置，最低与最高之间100等分。")
rrr_d=sorted(rrr_d.items(), key=lambda x: x[1], reverse=True)
s=rrr_d[0][0].split("-")
datee=f"{s[0]}年{int(s[1])}月{int(s[2])}日"
#datee="2023年3月24日"
print(f"\n{datee} 盘中创【新高】股票")
for rr in rrr1:
    #print(f"{rr[0][0]} {rr[0][1]}（{ddd2[rr[0][0]]}） {rr[1]}元")
##    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元  T:{rr[2]}%  E:{rr[3]}")
    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元")

print(f"\n{datee} 盘中创【新低】股票")
for rr in rrr2:
##    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元  T:{rr[2]}%  E:{rr[3]}")
    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元")

print(f"\n{datee} 收盘【连续上涨】股票(前10)")
rrr3=sorted(rrr3, key=lambda x: x[2], reverse=True)
for rr in rrr3[:10]:
##    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元  {rr[2]}天  T:{rr[3]}%  E:{rr[4]}")
    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元  {rr[2]}天")

print(f"\n{datee} 收盘【连续下跌】股票(前10)")
rrr4=sorted(rrr4, key=lambda x: x[2], reverse=True)
for rr in rrr4[:10]:
##    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元  {rr[2]}天  T:{rr[3]}%  E:{rr[4]}")
    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元  {rr[2]}天")

print(f"\n{datee} 收盘【加速上涨】股票(前10)")
rrr5=sorted(rrr5, key=lambda x: x[2], reverse=True)
for rr in rrr5[:10]:
##    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元  {rr[2]}天  T:{rr[3]}%  E:{rr[4]}")
    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元  {rr[2]}天")

print(f"\n{datee} 收盘【加速下跌】股票(前10)")
rrr6=sorted(rrr6, key=lambda x: x[2], reverse=True)
for rr in rrr6[:10]:
##    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元  {rr[2]}天  T:{rr[3]}%  E:{rr[4]}")
    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元  {rr[2]}天")

print(f"\n{datee} 【区间震荡1%】股票(前20)")
rrr7=sorted(rrr7, key=lambda x: x[2], reverse=True)
for rr in rrr7[:20]:
##    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元  {rr[2]}天  T:{rr[3]}%  E:{rr[4]}")
    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元  {rr[2]}天")

print(f"\n{datee} 【区间震荡2%】股票(前20)")
rrr8=sorted(rrr8, key=lambda x: x[2], reverse=True)
for rr in rrr8[:20]:
##    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元  {rr[2]}天  T:{rr[3]}%  E:{rr[4]}")
    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元  {rr[2]}天")

print(f"\n{datee} 【区间震荡3%】股票(前10)")
rrr9=sorted(rrr9, key=lambda x: x[2], reverse=True)
for rr in rrr9[:10]:
##    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元  {rr[2]}天  T:{rr[3]}%  E:{rr[4]}")
    print(f"{rr[0][0]} {rr[0][1]}  {rr[1]}元  {rr[2]}天")

print("--end--")
