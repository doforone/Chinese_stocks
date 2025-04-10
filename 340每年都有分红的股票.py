import baostock as bs
import pandas as pd

import json
import os
from PIL import Image, ImageDraw,ImageFont

with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

with open('data/行业分类2.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd2=json.loads(f.read())


a="d"
ddd3=[]
for dd in ddd:
    #print(dd[0])
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1":
        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):
            with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())
        else:
            continue

        if ooo!=[]:
            startt=int(ooo[0][0][:4])
            endd=int(ooo[-1][0][:4])
            endd_startt=endd-startt

            yearr={}
            for i in range(1,len(ooo)):
                if ooo[i][6]!=ooo[i-1][5]:
                    #yearr+=1
                    yearr[ooo[i][0][:4]]=ooo[i][0]

            if abs(endd_startt-len(yearr))<=1 and len(yearr)>=4:
            #if abs(endd_startt-len(yearr))<=0 and len(yearr)>=4:
                ddd3.append(dd[0])
                print(f"{dd[0]}  {dd[1]}（{ddd2[dd[0]]}）  {endd_startt}:{len(yearr)}  {ooo[-1][0]}")


                
##            if ooo[-1][5]=="":
##                closee=0
##            else:
##                closee=float(ooo[-1][5])
##
##            if ooo[-1][12]!="" and ooo[-2][12]!="":
##                if float(ooo[-1][12])<0 and float(ooo[-2][12])<0 \
##                   and abs(float(ooo[-1][12]))==max(list(map(lambda x: abs(float("0" if x[12]=="" else x[12])), ooo[-23:]))):
##                    print(f"{dd[0]}  {dd[1]}（{ddd2[dd[0]]}）  {closee}元  {ooo[-1][0]}")

with open(f'data/每年都有分红的股票.txt', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(json.dumps(ddd3, indent=4, ensure_ascii=False)+"\r\n")
print("--end--")
