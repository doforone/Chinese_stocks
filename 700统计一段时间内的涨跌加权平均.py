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

with open('data/不再更新的股票.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd4=json.loads(f.read())


f0=lambda x: 0.0 if x=="" else float(x)


if os.path.exists(f'data/k_line_d_东方财富/sh.000001_d.txt'):  #使用不复权数据，上证
    with open(f'data/k_line_d_东方财富/sh.000001_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo_A=json.loads(f.read())
    AA=ooo_A[0][0]
    ZZ=ooo_A[-1][0]
            

AV=0
N=0

for dd in ddd:
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3" and dd[0] not in ddd4:
        #print(dd)
        if os.path.exists(f'data/k_line_d_东方财富/{dd[0]}_d.txt'):
            with open(f'data/k_line_d_东方财富/{dd[0]}_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())
                    
            if ooo[0][0]!=AA or ooo[-1][0]!=ZZ:
                continue
            else:
                AV+=sum([f0(x[8]) for x in ooo])
                N+=len(ooo)

print(AV,N,AV/N)


if os.path.exists(f'data/k_line_d_东方财富/sh.000001_d.txt'):  #使用不复权数据，上证
    with open(f'data/k_line_d_东方财富/sh.000001_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo=json.loads(f.read())

    print(f"\r\n上证：{ooo[0][0]}，【{ooo[0][2]}】({f0(ooo[0][6])/100000000:.0f}亿)，{f0(ooo[0][8]):.2f}%    {ooo[-1][0]}，\
【{ooo[-1][2]}】({f0(ooo[-1][6])/100000000:.0f}亿)，{f0(ooo[-1][8]):.2f}%")
#====================
if os.path.exists(f'data/k_line_d_东方财富/sz.399001_d.txt'):  #使用不复权数据，深证
    with open(f'data/k_line_d_东方财富/sz.399001_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ooo=json.loads(f.read())

    print(f"深证：{ooo[0][0]}，【{ooo[0][2]}】({f0(ooo[0][6])/100000000:.0f}亿)，{f0(ooo[0][8]):.2f}%    {ooo[-1][0]}，\
【{ooo[-1][2]}】({f0(ooo[-1][6])/100000000:.0f}亿)，{f0(ooo[-1][8]):.2f}%")
#====================

print("--end--")
