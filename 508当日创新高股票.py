# AB量化，运行环境Python3.8
# -*- coding: UTF-8 -*-

import json
import os
from PIL import Image, ImageDraw,ImageFont
import random


##  日期【0】  昨收【1】  开盘【2】  最低【3】  最高【4】  收盘【5】  振幅【6】  涨跌【7】
##  成交量【8】  成交额【9】  换手率【10】  （收开【11】  昨均【12】  均价【13】  均幅【14】  市值【15】）
##  说明：振幅=最高*100/最低-100，收开=（收盘*100/开盘）-100
##  昨均=昨成交额/昨成交量，均幅=（（成交额/成交量）*100）/昨均-100
##  市值=收盘*（成交量*100）/换手率


with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

with open('data/行业分类2.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd2=json.loads(f.read())

with open('data/每年都有分红的股票.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd3=json.loads(f.read())

with open('data/不再更新的股票.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd4=json.loads(f.read())
    

f0=lambda x: 0.0 if x=="" else float(x)


a="d"
rrr1=[]
for dd in ddd:
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3" and dd[0] not in ddd4:
        ooo=[]
        if os.path.exists(f'data/K_line_{a}_前复权_计算获得/{dd[0]}_{a}.txt'):
            with open(f'data/K_line_{a}_前复权_计算获得/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())

        if ooo!=[]:
            # 创新高
            if ooo[-1][4]==max([x[4] for x in ooo]):
                rrr1.append([dd, ooo[-1][0], ooo[-1][5], ooo[-1][7]])


print(f"盘中创【新高】股票：")
for rr in rrr1:
    print(f"{rr[0][0]}  {rr[0][1]}({ddd2[rr[0][0]]})  上市日期：{rr[0][2]}  数据截止：{rr[1]}  {rr[2]}元  {rr[3]}%")
print(f"共计：{len(rrr1)}")

print("--end--")
