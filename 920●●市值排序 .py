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
    

##  日期【0】  昨收【1】  开盘【2】  最低【3】  最高【4】  收盘【5】  振幅【6】  涨跌【7】
##  成交量【8】  成交额【9】  换手率【10】  （收开【11】  昨均【12】  均价【13】  均幅【14】  市值【15】）
##  说明：振幅=最高*100/最低-100，收开=（收盘*100/开盘）-100
##  昨均=昨成交额/昨成交量，均幅=（（成交额/成交量）*100）/昨均-100
##  市值=收盘*（成交量*100）/换手率


f0=lambda x: 0.0 if x=="" else float(x)


rrr=[]

a="d"
today="2023-09-08"  #==========================
for dd in ddd:
    #print(dd[0])
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0] in ddd3 and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1":
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3" and dd[0] not in ddd4:
        #print(dd)
        uuu=[]
        if os.path.exists(f'data/K_line_{a}_前复权_计算获得/{dd[0]}_{a}.txt'):  #使用不复权数据
            with open(f'data/K_line_{a}_前复权_计算获得/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                uuu=json.loads(f.read())

        if uuu!=[] and len(uuu)>5:
            if uuu[-1][0]==today:
                rrr.append([dd, uuu[-1][5], uuu[-1][7], uuu[-1][15]])


##print(f"\n说明：1、数据均使用不复权数据；2、T为涨停天数占比；3、E为当前收盘价在历史最低与最高中位置，最低与最高之间100等分。")

print(f"市值前100：")
rrr=sorted(rrr, key=lambda x: x[3], reverse=True)
for rr in rrr[:100]:
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
print(f"中位数涨跌：{rrr[len(rrr)//2][2]}%")


if os.path.exists(f'data/k_line_d_东方财富/sh.000001_d.txt'):  #使用不复权数据，上证
    with open(f'data/k_line_d_东方财富/sh.000001_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo=json.loads(f.read())
        print(f"上证：{ooo[-1][0]}，【{ooo[-1][2]}】，{f0(ooo[-1][8]):.2f}%")
#====================
if os.path.exists(f'data/k_line_d_东方财富/sz.399001_d.txt'):  #使用不复权数据，深证
    with open(f'data/k_line_d_东方财富/sz.399001_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo=json.loads(f.read())
        print(f"深证：{ooo[-1][0]}，【{ooo[-1][2]}】，{f0(ooo[-1][8]):.2f}%")
#====================
if os.path.exists(f'data/k_line_d_东方财富/sz.399006_d.txt'):  #使用不复权数据，创业板
    with open(f'data/k_line_d_东方财富/sz.399006_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo=json.loads(f.read())
        print(f"创业板：{ooo[-1][0]}，【{ooo[-1][2]}】，{f0(ooo[-1][8]):.2f}%")
#====================

print("--end--")
