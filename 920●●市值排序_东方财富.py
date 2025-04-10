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


rrr=[]
for dd in ddd:
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3" and dd[0] not in ddd4:
        uuu=[]
        if os.path.exists(f'data/K_line_d_东方财富_前复权/{dd[0]}_d.txt'):  #使用不复权数据
            with open(f'data/K_line_d_东方财富_前复权/{dd[0]}_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                uuu=json.loads(f.read())

        if uuu!=[] and len(uuu)>5:
            rrr.append([dd, f0(uuu[-1][2]), f0(uuu[-1][8]), f0(uuu[-1][6])*100/f0(uuu[-1][10])])


print(f"市值前100：")
rrr=sorted(rrr, key=lambda x: x[3], reverse=True)
for rr in rrr[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{round(rr[3]/100000000,2)}亿元")

print("")
cap_100=sum([x[3] for x in rrr[:100]])/sum([x[3] for x in rrr])
a_0_100=sum([x[2] for x in rrr[:100]])/100
a_100_end=sum([x[2] for x in rrr[100:]])/len(rrr[100:])
a_all=sum([x[2] for x in rrr])/len(rrr)
print(f"市值前100总市值占比：{cap_100*100:.2f}%")
print(f"市值前100涨跌加权平均：{a_0_100:.2f}%")
print(f"市值100后涨跌加权平均：{a_100_end:.2f}%")
print(f"全部涨跌加权平均：{a_all:.2f}%")

rrr=sorted(rrr,key=lambda x: x[2])
print(f"涨跌排序后中位数：{rrr[len(rrr)//2][2]}%")

print(f"\n价格前100：")
rrr=sorted(rrr,key=lambda x: x[1], reverse=True)
for rr in rrr[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{round(rr[3]/100000000,2)}亿元")
print(f"\n价格前100涨跌加权平均：{sum([x[2] for x in rrr[:100]])/100:.2f}%")
print(f"价格100后涨跌加权平均：{sum([x[2] for x in rrr[100:]])/len(rrr[100:]):.2f}%")
a=b=0
for rr in rrr:
    if rr[1]<10:
        a+=rr[2]
        b+=1
print(f"价格<10涨跌加权平均：{a/b:.2f}%")
print(a,b)


print(f"\n上涨：{sum([1 for x in rrr if x[2]>0])}支，平盘：{sum([1 for x in rrr if x[2]==0])}支，下跌：{sum([1 for x in rrr if x[2]<0])}支")

if os.path.exists(f'data/k_line_d_东方财富_前复权/sh.000001_d.txt'):  #使用不复权数据，上证
    with open(f'data/k_line_d_东方财富_前复权/sh.000001_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo=json.loads(f.read())
        print(f"上证：{ooo[-1][0]}，【{ooo[-1][2]}】({f0(ooo[-1][6])/100000000:.0f}亿)，{f0(ooo[-1][8]):.2f}%")
        #print(f"上证：【{ooo[-1][2]}】({f0(ooo[-1][6])/100000000:.0f}亿)，{f0(ooo[-1][8]):.2f}%")
#====================
if os.path.exists(f'data/k_line_d_东方财富_前复权/sz.399001_d.txt'):  #使用不复权数据，深证
    with open(f'data/k_line_d_东方财富_前复权/sz.399001_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo=json.loads(f.read())
        print(f"深证：{ooo[-1][0]}，【{ooo[-1][2]}】({f0(ooo[-1][6])/100000000:.0f}亿)，{f0(ooo[-1][8]):.2f}%")
        #print(f"深证：【{ooo[-1][2]}】({f0(ooo[-1][6])/100000000:.0f}亿)，{f0(ooo[-1][8]):.2f}%")
#====================
if os.path.exists(f'data/k_line_d_东方财富_前复权/sz.399006_d.txt'):  #使用不复权数据，创业板
    with open(f'data/k_line_d_东方财富_前复权/sz.399006_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo=json.loads(f.read())
        print(f"创业板：{ooo[-1][0]}，【{ooo[-1][2]}】({f0(ooo[-1][6])/100000000:.0f}亿)，{f0(ooo[-1][8]):.2f}%")
        #print(f"创业板：【{ooo[-1][2]}】({f0(ooo[-1][6])/100000000:.0f}亿)，{f0(ooo[-1][8]):.2f}%")
#====================
print("PS.统计不含科创板和近期上市股票。")

print("--end--")
