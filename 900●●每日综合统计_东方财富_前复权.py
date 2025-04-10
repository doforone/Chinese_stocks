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

with open('data/不再更新的股票.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd4=json.loads(f.read())


##  日期【0】  昨收【1】  开盘【2】  最低【3】  最高【4】  收盘【5】  振幅%【6】  涨跌%【7】
##  成交量【8】  成交额【9】  换手率【10】  （收开%【11】  昨均【12】  今均【13】  均幅%【14】  市值【15】）
##  说明：振幅=最高*100/最低-100，收开=（收盘*100/开盘）-100
##  昨均=昨成交额/昨成交量，均幅=（（成交额/成交量）*100）/昨均-100
##  市值=收盘*（成交量*100）/换手率

#### 日K线参数名称及定义 ####
##"2023-07-27,1836.00,1838.03,1854.79,1828.70,20340,3749635290.00,1.43,0.52,9.48,0.16"
##茅台日期         开盘        收盘         最高        最低        成交量（手）成交额（元）振幅% 涨跌幅% 涨跌值 流通换手率
##   0              1           2            3          4            5           6           7    8      9     10
## 振幅%=（最高-最低）/昨收；涨跌幅%=（收盘-昨收）/昨收；涨跌值=收盘-昨收


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
rrr10=[]  # 平盘1%向上突破
rrr11=[]  # 平盘2%向上突破
rrr12=[]  # 平盘3%向上突破
rrr13=[]  # 平盘1%向下突破
rrr14=[]  # 平盘2%向下突破
rrr15=[]  # 平盘3%向下突破
rrr_000=[]  # 综合

if os.path.exists(f'data/k_line_d_东方财富_前复权/sh.000001_d.txt'):  #使用不复权数据，上证
    with open(f'data/k_line_d_东方财富_前复权/sh.000001_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        uuu_a=json.loads(f.read())
today=uuu_a[-1][0]
for dd in ddd:
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3" and dd[0] not in ddd4:
        uuu=[]
        if os.path.exists(f'data/K_line_d_东方财富_前复权/{dd[0]}_d.txt'):
            with open(f'data/K_line_d_东方财富_前复权/{dd[0]}_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                uuu=json.loads(f.read())

        if uuu[-1][0]==today:
            # 创新高
            if f0(uuu[-1][3])==max([f0(x[3]) for x in uuu]):
                rrr1.append([dd, uuu[-1][2], uuu[-1][8]])

            # 创新低
            if f0(uuu[-1][4])==min([f0(x[4]) for x in uuu]):
                rrr2.append([dd, uuu[-1][2], uuu[-1][8]])

            # 连续上涨
            n=0
            for uu in uuu[::-1]:
                if f0(uu[8])>0:
                    n+=1
                else:
                    break
            rrr3.append([dd, uuu[-1][2], uuu[-1][8], n])

            # 连续下跌
            n=0
            for uu in uuu[::-1]:
                if f0(uu[8])<0:
                    n+=1
                else:
                    break
            rrr4.append([dd, uuu[-1][2], uuu[-1][8], n])

            # 加速上涨
            n=0
            x=1000
            for uu in uuu[::-1]:
                uu8=f0(uu[8])
                if uu8>0 and uu8<x:
                    n+=1
                    x=uu8
                else:
                    break
            rrr5.append([dd, uuu[-1][2], uuu[-1][8], n])
            
            # 加速下跌
            n=0
            x=-1000
            for uu in uuu[::-1]:
                uu8=f0(uu[8])
                if uu8<0 and uu8>x:
                    n+=1
                    x=uu8
                else:
                    break
            rrr6.append([dd, uuu[-1][2], uuu[-1][8], n])

            # 区间震荡
            vvv=[f0(x[6])/f0(x[5]) for x in uuu if f0(x[5])>0]
            lenn=len(vvv)
            # 区间震荡 1%
            for i in range(2,lenn):
                if max(vvv[-i:])/min(vvv[-i:])>1.01:
                    rrr7.append([dd, uuu[-1][2], uuu[-1][8], i-1])
                    break

            # 区间震荡 2%
            for i in range(2,lenn):
                if max(vvv[-i:])/min(vvv[-i:])>1.02:
                    rrr8.append([dd, uuu[-1][2], uuu[-1][8], i-1])
                    break

            # 区间震荡 3%
            for i in range(2,lenn):
                if max(vvv[-i:])/min(vvv[-i:])>1.03:
                    rrr9.append([dd, uuu[-1][2], uuu[-1][8], i-1])
                    break

            # 平盘1%向上突破
            for i in range(3,lenn):
                maxx=max(vvv[-i:-1])
                minn=min(vvv[-i:-1])
                if minn>0:
                    if maxx/minn>1.01:
                        if vvv[-1]/min(vvv[-i+1:-1])>1.01:
                            rrr10.append([dd, uuu[-1][2], uuu[-1][8], i-2])
                        break

            # 平盘2%向上突破
            for i in range(3,lenn):
                maxx=max(vvv[-i:-1])
                minn=min(vvv[-i:-1])
                if minn>0:
                    if maxx/minn>1.02:
                        if vvv[-1]/min(vvv[-i+1:-1])>1.02:
                            rrr11.append([dd, uuu[-1][2], uuu[-1][8], i-2])
                        break

            # 平盘3%向上突破
            for i in range(3,lenn):
                maxx=max(vvv[-i:-1])
                minn=min(vvv[-i:-1])
                if minn>0:
                    if maxx/minn>1.03:
                        if vvv[-1]/min(vvv[-i+1:-1])>1.03:
                            rrr12.append([dd, uuu[-1][2], uuu[-1][8], i-2])
                        break

            # 平盘1%向下突破
            for i in range(3,lenn):
                maxx=max(vvv[-i:-1])
                minn=min(vvv[-i:-1])
                if minn>0:
                    if maxx/minn>1.01:
                        if max(vvv[-i+1:-1])/vvv[-1]>1.01:
                            rrr13.append([dd, uuu[-1][2], uuu[-1][8], i-2])
                        break

            # 平盘2%向下突破
            for i in range(3,lenn):
                maxx=max(vvv[-i:-1])
                minn=min(vvv[-i:-1])
                if minn>0:
                    if maxx/minn>1.02:
                        if max(vvv[-i+1:-1])/vvv[-1]>1.02:
                            rrr14.append([dd, uuu[-1][2], uuu[-1][8], i-2])
                        break

            # 平盘3%向下突破
            for i in range(3,lenn):
                maxx=max(vvv[-i:-1])
                minn=min(vvv[-i:-1])
                if minn>0:
                    if maxx/minn>1.03:
                        if max(vvv[-i+1:-1])/vvv[-1]>1.03:
                            rrr15.append([dd, uuu[-1][2], uuu[-1][8], i-2])
                        break
                    
            if f0(uuu[-1][10])>0:  # 流通换手率>0，否则计算市值出错。
                rrr_000.append([dd, f0(uuu[-1][2]), f0(uuu[-1][8]), sum([f0(x[6]) for x in uuu[-7:]]), sum([f0(x[10]) for x in uuu[-7:]]),
                                sum([1 if f0(x[8])>9.8 else 0 for x in uuu[-10:]]), sum([1 if f0(x[8])<-9.8 else 0 for x in uuu[-10:]]),
                                f0(uuu[-1][6])*100/f0(uuu[-1][10]), f0(uuu[-2][6])*100/f0(uuu[-2][10])*(f0(uuu[-1][8])/100)])

##print(f"\n说明：1、数据均使用不复权数据；2、T为涨停天数占比；3、E为当前收盘价在历史最低与最高中位置，最低与最高之间100等分。")
s=today.split("-")
datee=f"{s[0]}年{int(s[1])}月{int(s[2])}日"
#datee="2023年3月24日"

print(f"\n======== {datee}A股收盘统计 ========\n")

if os.path.exists(f'data/k_line_d_东方财富_前复权/sh.000001_d.txt'):  #使用不复权数据，上证
    with open(f'data/k_line_d_东方财富_前复权/sh.000001_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo=json.loads(f.read())
        print(f"上证：{ooo[-1][0]}，【{ooo[-1][2]}】({f0(ooo[-1][6])/100000000:.0f}亿)，{f0(ooo[-1][8]):.2f}%")
#====================
if os.path.exists(f'data/k_line_d_东方财富_前复权/sz.399001_d.txt'):  #使用不复权数据，深证
    with open(f'data/k_line_d_东方财富_前复权/sz.399001_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo=json.loads(f.read())
        print(f"深证：{ooo[-1][0]}，【{ooo[-1][2]}】({f0(ooo[-1][6])/100000000:.0f}亿)，{f0(ooo[-1][8]):.2f}%")
#====================
if os.path.exists(f'data/k_line_d_东方财富_前复权/sz.399006_d.txt'):  #使用不复权数据，创业板
    with open(f'data/k_line_d_东方财富_前复权/sz.399006_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo=json.loads(f.read())
        print(f"创业板：{ooo[-1][0]}，【{ooo[-1][2]}】({f0(ooo[-1][6])/100000000:.0f}亿)，{f0(ooo[-1][8]):.2f}%")
#====================

print(f"\n上涨：{sum([1 for x in rrr_000 if x[2]>0])}支，平盘：{sum([1 for x in rrr_000 if x[2]==0])}支，下跌：{sum([1 for x in rrr_000 if x[2]<0])}支\n")

rrr=sorted(rrr_000, key=lambda x: x[7], reverse=True)
cap_100=sum([x[7] for x in rrr[:100]])/sum([x[7] for x in rrr])
print(f"市值前100总市值占比：{cap_100*100:.2f}%")
a_0_100=sum([x[2] for x in rrr[:100]])/100
print(f"市值前100涨跌简单加权平均：{a_0_100:.2f}%")
a_100_end=sum([x[2] for x in rrr[100:]])/len(rrr[100:])
print(f"市值100后涨跌简单加权平均：{a_100_end:.2f}%")
a_all=sum([x[2] for x in rrr])/len(rrr)
print(f"全部涨跌简单加权平均：{a_all:.2f}%")
rrr=sorted(rrr,key=lambda x: x[2])
print(f"涨跌排序后中位数：{rrr[len(rrr)//2][2]}%")

print("\n注：本页统计不含科创板和近期上市股票，前复权。")
#print("如需回测、交叉统计，请联系：chaoxian102（微信）。")
#print("\n作者：AB量化；\n如需交叉统计，回测，请联系：chaoxian102（微信）。"



print(f"\n--------------------\n{datee} 盘中创【新高】股票：")
for rr in rrr1:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%")

print(f"\n--------------------\n{datee} 盘中创【新低】股票：")
for rr in rrr2:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%")

print(f"\n--------------------\n{datee} 【市值增额】股票(前10)：")
rrr=sorted(rrr_000, key=lambda x: x[8], reverse=True)
for rr in rrr[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[8]/100000000:.2f}亿")

print(f"\n--------------------\n{datee} 【市值减额】股票(前10)：")
rrr=sorted(rrr_000, key=lambda x: x[8], reverse=False)
for rr in rrr[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[8]/100000000:.2f}亿")

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

##print(f"\n--------------------\n{datee} 【区间震荡1%】股票(前10)：")
##rrr7=sorted(rrr7, key=lambda x: x[3], reverse=True)
##for rr in rrr7[:10]:
##    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[3]}天")

print(f"\n--------------------\n{datee} 【区间震荡2%】股票(前10)：")
rrr8=sorted(rrr8, key=lambda x: x[3], reverse=True)
for rr in rrr8[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[3]}天")
print(f"注：以日均价计算。")

##print(f"\n--------------------\n{datee} 【区间震荡3%】股票(前10)：")
##rrr9=sorted(rrr9, key=lambda x: x[3], reverse=True)
##for rr in rrr9[:10]:
##    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[3]}天")

print(f"\n--------------------\n{datee} 【平盘2%向上突破】股票(前10)：")
rrr11=sorted(rrr11, key=lambda x: x[3], reverse=True)
for rr in rrr11[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[3]}天")
print(f"注：以日均价计算。")

print(f"\n--------------------\n{datee} 【平盘2%向下突破】股票(前10)：")
rrr14=sorted(rrr14, key=lambda x: x[3], reverse=True)
for rr in rrr14[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[3]}天")
print(f"注：以日均价计算。")



print(f"\n--------------------\n{datee} 【7日成交额排名】股票(前10)：")
rrr=sorted(rrr_000, key=lambda x: x[3], reverse=True)
for rr in rrr[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[3]/100000000:.1f}亿")

print(f"\n--------------------\n{datee} 【7日换手率排名】股票(前10)：")
rrr=sorted(rrr_000, key=lambda x: x[4], reverse=True)
for rr in rrr[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[4]:.1f}%")

print(f"\n--------------------\n{datee} 【10日内涨停天数排名】(前10)：")
rrr=sorted(rrr_000, key=lambda x: x[5], reverse=True)
for rr in rrr[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[5]}天")
print(f"注：涨跌幅>9.8即为涨停。")

print(f"\n--------------------\n{datee} 【10日内跌停天数排名】(前10)：")
rrr=sorted(rrr_000, key=lambda x: x[6], reverse=True)
for rr in rrr[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[6]}天")
print(f"注：涨跌幅<-9.8即为跌停。")

print(f"\n--------------------\n{datee} 【收盘市值排名】股票(前10)：")
rrr=sorted(rrr_000, key=lambda x: x[7], reverse=True)
for rr in rrr[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{rr[7]/100000000:.0f}亿")

print(f"\n--------------------\n{datee} 【收盘股价排名】股票(前10)：")
rrr=sorted(rrr_000, key=lambda x: x[1], reverse=True)
for rr in rrr[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%")


print(f"\n--------------------\n{datee} 【股价结构化分布】：")
print(f"  0--  5元：{sum([1 if 0<=x[1]<5 else 0 for x in rrr_000])}支")
print(f"  5-- 10元：{sum([1 if 5<=x[1]<10 else 0 for x in rrr_000])}支")
print(f" 10-- 20元：{sum([1 if 10<=x[1]<20 else 0 for x in rrr_000])}支")
print(f" 20-- 50元：{sum([1 if 20<=x[1]<50 else 0 for x in rrr_000])}支")
print(f" 50--100元：{sum([1 if 50<=x[1]<100 else 0 for x in rrr_000])}支")
print(f"100元以上 ：{sum([1 if 100<=x[1]<50000 else 0 for x in rrr_000])}支")

print(f"\n--------------------\n{datee} 【市值结构化分布】：")
print(f"   0--  10亿元：{sum([1 if 0<=x[7]<10_00000000 else 0 for x in rrr_000])}支")
print(f"  10--  50亿元：{sum([1 if 10_00000000<=x[7]<50_00000000 else 0 for x in rrr_000])}支")
print(f"  50-- 100亿元：{sum([1 if 50_00000000<=x[7]<100_00000000 else 0 for x in rrr_000])}支")
print(f" 100-- 500亿元：{sum([1 if 100_00000000<=x[7]<500_00000000 else 0 for x in rrr_000])}支")
print(f" 500--1000亿元：{sum([1 if 500_00000000<=x[7]<1000_00000000 else 0 for x in rrr_000])}支")
print(f"1000亿元以上  ：{sum([1 if 1000_00000000<=x[7]<1000000_00000000 else 0 for x in rrr_000])}支")

print("\n--- End ---")
