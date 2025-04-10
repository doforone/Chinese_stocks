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

rrr2=[rr[0][0] for rr in rrr]


with open(f'data/市值排序.txt', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(json.dumps(rrr2, indent=0, ensure_ascii=False)+"\r\n")
    
for rr in rrr[:10]:
    print(f"{rr[0][0]}({rr[0][1]:　^4})  {rr[1]}元，{rr[2]}%，{round(rr[3]/100000000,2)}亿元")


print("--end--")
