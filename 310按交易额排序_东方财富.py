import baostock as bs
import pandas as pd

import json
import os
from PIL import Image, ImageDraw,ImageFont

import random


#### 日K线参数名称及定义 ####
##"2023-07-27,1836.00,1838.03,1854.79,1828.70,20340,3749635290.00,1.43,0.52,9.48,0.16"
##茅台日期         开盘        收盘         最高        最低        成交量（手）成交额（元）振幅 涨跌幅 涨跌 流通换手率
##   0              1           2            3          4            5           6           7    8      9     10


f0=lambda x: 0.0 if x=="" else float(x)


with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

with open('data/行业分类2.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd2=json.loads(f.read())

with open('data/每年都有分红的股票.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd3=json.loads(f.read())

with open('data/不再更新的股票.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd4=json.loads(f.read())


a="d"
for dd in ddd:
    if (dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3" and dd[0] not in ddd4) and dd[0][:3]=="sz.":
        if os.path.exists(f'data/k_line_d_东方财富/{dd[0]}_d.txt'):
            with open(f'data/k_line_d_东方财富/{dd[0]}_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())

        if ooo!=[]:
            print(f"{dd[0]},{dd[1]},{ddd2[dd[0]]},{ooo[-1][0]},{ooo[-1][6]}/{ooo[-2][6]}={f0(ooo[-1][6])/f0(ooo[-2][6]):.4f}")
