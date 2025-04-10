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

with open('data/每年都有分红的股票.txt', 'r', encoding='utf-8-sig', \
          newline='\r\n') as f:
    ddd3=json.loads(f.read())


def float_000(a):
    return 0.0 if a=="" else float(a)


# 统计第一次跌停后，第二日上涨与下跌的数量，值统计数量，不考虑收益和交易成本。
rrr={"A":0, "V":0}  # A为上涨计数，V为下跌计数
a="d"
for dd in ddd:
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1":  # 除指数外，全部统计
        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):  # 使用不复权数据
            with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())
        if ooo!=[] and (lenn:=len(ooo))>=3:
            i=1
            while i<lenn-1:
                if dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":  # 普通股票
                    if float_000(ooo[i-1][12])>0 and float_000(ooo[i][12])<=9.8:  # # 普通股票第一次下跌按<=9.8
                        if float_000(ooo[i+1][12])>0:  # 第二日上涨
                            rrr["A"]+=1
                            i+=1
                        elif float_000(ooo[i+1][12])<0:  # 第二日下跌
                            rrr["V"]+=1
                            i+=2
                else:  # 科创板股票
                    if float_000(ooo[i-1][12])>0 and float_000(ooo[i][12])<=19.8:  # 科创板股票第一次下跌按<=19.8
                        if float_000(ooo[i+1][12])>0:  # 第二日上涨
                            rrr["A"]+=1
                            i+=1
                        elif float_000(ooo[i+1][12])<0:  # 第二日下跌
                            rrr["V"]+=1
                            i+=2
                i+=1


print(f"第一次跌停后，第二日上涨：{rrr['A']}，下跌：{rrr['V']}，上涨与下跌之比为：{round(rrr['A']/rrr['V'],2)}")
print("--end--")
