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
a="w"  #===========注意时周K线
for dd in ddd:
    #print(dd[0])
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1":
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):
            with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())

        if ooo!=[]:
            if ooo[-1][5]=="":
                closee=0
            else:
                closee=float(ooo[-1][5])

            if ooo[-1][8]=="":
                amountt=0
            else:
                amountt=float(ooo[-1][7])  #天为8

            if ooo[-1][10]=="":
                continue
            else:
                trunn=float(ooo[-1][9])  #换手率
                if trunn!=0:
                    #print(trunn)
                    ddd3.append([dd[0], dd[1], closee, amountt, amountt*100/trunn, trunn])
            #代码 名称 收盘 成交额

ddd3=sorted(ddd3,key=lambda x: x[4], reverse=True)

##for dd3 in ddd3[:100]:
##    print(dd3)

summ=0
summ_10=0
n_10=0
for ii, vv in enumerate(ddd3, start=1):
    #if vv[2]<10:
    print(f"{ii:>4}  {vv[0]}  {vv[1]:　^4}  {vv[2]:>8.2f}  {vv[4]/100000000:>8.2f} 亿元")
        
    summ+=vv[4]
    
    if 0<=vv[2]<10:
        summ_10+=vv[4]
        n_10+=1
        
    if ii%100==0:
        print(f"------以上市值：{summ/100000000:.2f} 亿元；  平均：{(summ/ii)/100000000:.2f} 亿元")

print("------")
print(f"总市值：{summ/100000000:.2f} 亿元；  平均：{(summ/len(ddd3))/100000000:.2f} 亿元")

print(f"股价<10总市值：{summ_10/100000000:.2f} 亿元；  个数：{n_10}，  平均：{(summ_10/n_10)/100000000:.2f} 亿元")
