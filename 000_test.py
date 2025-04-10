import json
from PIL import Image, ImageDraw,ImageFont
import datetime
import os
import time
import random


#### 日K线参数名称及定义 ####
##"2023-07-27,1836.00,1838.03,1854.79,1828.70,20340,3749635290.00,1.43,0.52,9.48,0.16"
##茅台日期         开盘        收盘         最高        最低        成交量（手）成交额（元）振幅% 涨跌幅% 涨跌值 流通换手率
##   0              1           2            3          4            5           6           7    8      9     10
## 振幅%=（最高-最低）/昨收；涨跌幅%=（收盘-昨收）/昨收；涨跌值=收盘-昨收

## 本测试说明,东方财富的不复权涨跌幅是以不复权的上一个收盘价格为基准计算的,前复权数据也是以前复权数据的上一个收盘价为基准计算的.


##with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
##    ddd=json.loads(f.read())
##
##uuu=[dd[0] for dd in ddd if
##     (dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3") or dd[0]=="sh.000001" or dd[0]=="sz.399001" or dd[0]=="sz.399006"]
##
##
##f0=lambda x: 0.0 if x=="" else float(x)
##
##
##vvv = random.sample(uuu, 20)
##for vv in vvv:
##    print(vv)
##    if os.path.exists(f'data/k_line_d_东方财富_不复权/{vv}_d.txt'):
##        with open(f'data/k_line_d_东方财富_不复权/{vv}_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
##            ddd1=json.loads(f.read())
##
##    www=[]
##    if os.path.exists(f'data/k_line_d/{vv}_d.txt'):
##        with open(f'data/k_line_d/{vv}_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
##            ddd2=json.loads(f.read())
##        for ii,vv in enumerate(ddd2[:-1]):
##            if vv[5]!=ddd2[ii+1][6]:
##                www.append(ddd2[ii+1][0])
##
##    #www=random.sample(ddd1, 3)
##    print(www)
##    for ww in www:
##        for dd in ddd1:
##            #if dd[0]==ww[0]:
##            if dd[0]==ww:
##                #print(dd[0],f0(dd[2])-f0(dd[9]),dd[1],dd[4],dd[3],dd[2])
##                print(dd[0],(f0(dd[2])*100)/(f0(dd[8])+100),dd[1],dd[4],dd[3],dd[2],dd[8])
##                break
##
##        for dd in ddd2:
##            #if dd[0]==ww[0]:
##            if dd[0]==ww:
##                print(dd[0],dd[6][:-2],dd[2][:-2],dd[4][:-2],dd[3][:-2],dd[5][:-2],dd[12])
##                break
##        print("----------------")
##    print("===================")


#### 日K线参数名称及定义 ####
##"2023-07-27,1836.00,1838.03,1854.79,1828.70,20340,3749635290.00,1.43,0.52,9.48,0.16"
##茅台日期         开盘        收盘         最高        最低        成交量（手）成交额（元）振幅% 涨跌幅% 涨跌值 流通换手率
##   0              1           2            3          4            5           6           7    8      9     10
## 振幅%=（最高-最低）/昨收；涨跌幅%=（收盘-昨收）/昨收；涨跌值=收盘-昨收

## 本测试说明,东方财富的不复权涨跌幅是以不复权的上一个收盘价格为基准计算的,前复权数据也是以前复权数据的上一个收盘价为基准计算的.


f0=lambda x: 0.0 if x=="" else float(x)

with open(f'data/k_line_d_东方财富_不复权/sz.002047_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd0=json.loads(f.read())

with open(f'data/k_line_d_东方财富_前复权/sz.002047_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd1=json.loads(f.read())

##a=1
##if len(ddd0)==len(ddd1):
##    for i in range(len(ddd0)-1,0,-1):
##        if round((round(f0(ddd0[i][2])*a,2)*100)/round(f0(ddd0[i-1][2])*a,2)-100,2)!=f0(ddd1[i][8]):
##            #a=round(a*(f0(ddd1[i-1][2])/f0(ddd0[i-1][2])),4)
##            a0=f0(ddd1[i-1][2])/f0(ddd0[i-1][2])
##            a0=round(a0,6)
##            a=a*a0
##            print(i,ddd0[i][0],a)
##            #break


##a=1
##if len(ddd0)==len(ddd1):
##    for i in range(len(ddd0)-1,0,-1):
##        if round(f0(ddd0[i][1])*a,2)!=f0(ddd1[i][1])\
##           or round(f0(ddd0[i][2])*a,2)!=f0(ddd1[i][2])\
##           or round(f0(ddd0[i][3])*a,2)!=f0(ddd1[i][3])\
##           or round(f0(ddd0[i][4])*a,2)!=f0(ddd1[i][4]):
##            
##            #a=(f0(ddd1[i][2])/(round(f0(ddd0[i][2])*a),2))*a
##            a=(f0(ddd1[i][3])/round(f0(ddd0[i][3])*a,2))*a
##            print(i,ddd0[i][0],a)
##            #break


##a=1
##if len(ddd0)==len(ddd1):
##    for i in range(len(ddd0)-1,0,-1):
##        if round(f0(ddd1[i][1])*a,2)!=f0(ddd0[i][1])\
##           or round(f0(ddd1[i][2])*a,2)!=f0(ddd0[i][2])\
##           or round(f0(ddd1[i][3])*a,2)!=f0(ddd0[i][3])\
##           or round(f0(ddd1[i][4])*a,2)!=f0(ddd0[i][4]):
##            
##            #a=(f0(ddd1[i][2])/(round(f0(ddd0[i][2])*a),2))*a
##            a=(f0(ddd0[i][3])/round(f0(ddd1[i][3])*a,2))*a
##            print(i,ddd0[i][0],a)
##            #break


##a=1
##if len(ddd0)==len(ddd1):
##    for i in range(len(ddd0)-1,0,-1):
##        if (x1:=round(f0(ddd1[i][2])-f0(ddd1[i][9]),2))\
##           !=(x0:=round((f0(ddd0[i][2])-f0(ddd0[i][9]))*a,2)):
##            a*=x1/x0
##            print(i,ddd0[i][0],a)
##            #break
##else:
##    print("leng err")


##a=1
##if len(ddd0)==len(ddd1):
##    for i in range(len(ddd0)-1,0,-1):
##        if (x1:=round(f0(ddd1[i][2])-f0(ddd1[i][9])*a,2))\
##           !=(x0:=round((f0(ddd0[i][2])-f0(ddd0[i][9])),2)):
##            a*=x0/x1
##            print(i,ddd0[i][0],a)
##            #break
##else:
##    print("leng err")


for dd0 in ddd0:
    if round(f0(dd0[2])*100/(f0(dd0[2])-f0(dd0[9]))-100,2)!=f0(dd0[8]):
        print(dd0)
        print(round(f0(dd0[2])*100/(f0(dd0[2])-f0(dd0[9]))-100,2), f0(dd0[8]))

print("-----------")

for dd0 in ddd1:
    if round(f0(dd0[2])*100/(f0(dd0[2])-f0(dd0[9]))-100,2)!=f0(dd0[8]):
        print(dd0)
        print(f0(dd0[2])*100/(f0(dd0[2])-f0(dd0[9]))-100, f0(dd0[8]))

print("--end--")









