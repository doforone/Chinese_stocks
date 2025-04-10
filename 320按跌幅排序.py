import baostock as bs
import pandas as pd

import json
import os
from PIL import Image, ImageDraw,ImageFont

with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

with open('data/行业分类2.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd2=json.loads(f.read())

ddd3=[]
a="d"
for dd in ddd:
    #print(dd[0])
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1":
        if os.path.exists(f'data/k_line_{a}_前复权/{dd[0]}_{a}.txt'):
            with open(f'data/k_line_{a}_前复权/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())

        if ooo!=[]:
            if ooo[-1][5]=="":
                closee=0
            else:
                closee=float(ooo[-1][5])

            if ooo[-1][12]=="":
                av=0
            else:
                av=float(ooo[-1][12])
                
            ddd3.append([dd[0], dd[1], closee, av, ooo[-1][0]])
            #代码 名称 收盘 涨跌幅

ddd3=sorted(ddd3,key=lambda x: x[3], reverse=False)

for dd3 in ddd3[:100]:
    print(dd3)
