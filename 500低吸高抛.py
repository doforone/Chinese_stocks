import baostock as bs
import pandas as pd

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

#日期【0】  昨收【1】  开盘【2】  最低【3】  最高【4】  收盘【5】
#振幅【6】  涨跌【7】  成交量【8】  成交额【9】  换手率【10】

def float_000(a):
    if a=="":
        return 0.0
    else:
        return float(a)
        
        
a="d"
MN=23
AV=.06
for dd in random.sample(ddd,200):
    #print(dd[0])
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0] in ddd3 and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
        print(dd)
        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):
            with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())

        if ooo!=[]:
            uuu=[[x[0], float_000(x[6]), float_000(x[2]), float_000(x[4]), float_000(x[3]), float_000(x[5]), float(x[3])-min([float(x[4]),float(x[6])]),\
                 float_000(x[12]), float_000(x[7]), float_000(x[8]), float_000(x[10])] for x in ooo]

##            uuu=[[x[0], x[6], x[2], x[4], x[3], x[5], float(x[3])-min([float(x[4]),float(x[6])]),\
##                 x[12], x[7], x[8], x[10]] for x in ooo]

            buy=0
            price=0
            vvv=0
            n=0
            for i in range(MN-1, len(uuu)):
                if buy==0:
                    if uuu[i-1][7]<0 and uuu[i][7]<min([-abs(x[7]) for x in uuu[i-MN+1: i]]):
                        #vvv.append(uuu[i+1][7])
                        buy=1
                        price=uuu[i][5]
                else:
                    if uuu[i][7]>3:
                        #vvv.append(uuu[i][5]-price)
                        vvv+=uuu[i][5]-price
                        n+=1
                        buy=0
                        price=0

            print(vvv,n)
                




            with open(f'data/临时/{dd[0]}.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                f.write(json.dumps(uuu, indent=4, ensure_ascii=False)+"\r\n")



##            if ooo[-1][5]=="":
##                closee=0
##            else:
##                closee=float(ooo[-1][5])
##
##            
##
##
##
##
##
##            if ooo[-1][12]!="" and ooo[-2][12]!="":
##                if float(ooo[-1][12])<0 and float(ooo[-2][12])<0 \
##                   and abs(float(ooo[-1][12]))==max(list(map(lambda x: abs(float("0" if x[12]=="" else x[12])), ooo[-23:]))):
##                    print(f"{dd[0]}  {dd[1]}（{ddd2[dd[0]]}）  【{round(float(ooo[-1][12]),2)}】  {closee}元  {ooo[-1][0]}")

print("--end--")
