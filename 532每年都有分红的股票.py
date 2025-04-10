##白点数据，运行环境python3.8

import json
import os
from PIL import Image, ImageDraw,ImageFont


with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

with open('data/行业分类2.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd2=json.loads(f.read())

a="d"
rrr=[]
for dd in ddd:
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1":
        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):
            with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', \
                      encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())
                ##[
                ##    "2020-08-28",
                ##    "sh.688215",
                ##    "90.0000",
                ##    "108.0000",
                ##    "86.6600",
                ##    "90.4100",
                ##    "34.7300",
                ##    "7110891",
                ##    "656958998.2700",
                ##    "3",
                ##    "78.339200",
                ##    "1",
                ##    "160.322500",
                ##    "80.695677",
                ##    "16.984859",
                ##    "440.980030",
                ##    "26.263406",
                ##    "0"
                ##]
        else:
            continue

        if ooo!=[]:
            startt=int(ooo[0][0][:4])
            endd=int(ooo[-1][0][:4])
            endd_startt=endd-startt
            
            yearr={}
            for i in range(1,len(ooo)):
                if ooo[i][6]!=ooo[i-1][5]:
                    yearr[ooo[i][0][:4]]=ooo[i][0]

            if abs(endd_startt-len(yearr))<=1 and len(yearr)>=4:
                #上市大于4年，最多1年没有除权（分红）的股票
                #我们认为这样的股票相对安全，不会暴跌或st
                rrr.append(dd[0])
                print(f"{dd[0]}  {dd[1]}（{ddd2[dd[0]]}）  \
上市日期：{ooo[0][0]}")

print(f"共计：{len(rrr)}")
                
with open(f'data/每年都有分红的股票2.txt', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(json.dumps(rrr, indent=4, ensure_ascii=False)+"\r\n")

print("--end--")
