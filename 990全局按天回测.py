##  AB量化，chaoxian102，运行环境Python3.8
##  -*- coding: UTF-8 -*-


import os
import time
import json
import random
from PIL import Image, ImageDraw,ImageFont

f0=lambda x: 0.0 if x=="" else float(x)  # 字符串类型数字转为浮点数字


with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())
    # [[【0】证券代码  【1】证券名称  【2】上市日期  【3】退市日期  【4】证券类型，其中1：股票，2：指数，3：其它，4：可转债，5：ETF  【5】上市状态，其中1：上市，0：退市]]

with open('data/行业分类2.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd2=json.loads(f.read())
    # {【证券代码：所属行业】}

with open('data/每年都有分红的股票.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd3=json.loads(f.read())
    # [【0】证券代码]

with open('data/不再更新的股票.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd4=json.loads(f.read())
    # [【0】证券代码]


##  ------ 前复权日K线数据 ------
##  [日期【0】  昨收【1】  开盘【2】  最低【3】  最高【4】  收盘【5】  振幅【6】  涨跌【7】
##  成交量【8】  成交额【9】  换手率【10】  收开【11】  昨均【12】  均价【13】  均幅【14】  市值【15】]
##  说明：振幅=最高*100/最低-100，收开=（收盘*100/开盘）-100
##  昨均=昨成交额/昨成交量，均幅=（（成交额/成交量）*100）/昨均-100
##  市值=收盘*（成交量*100）/换手率
##  除日期为字符串类型，成交量为整型外，其他均为浮点数类型。


uuu={}
MN=900  # 回测天数
AA=""  # 开始日期
ZZ=""  # 结束日期
#SS=3  # 从第几天开始
SS=6  # 从第几天开始，7日额
cang={}  # 持仓股票情况
fen=3  # 资金平均分几份
bal=0  # 总收益

vvv=vvv2=vvv3=[]
if os.path.exists(f'data/k_line_d/sh.000001_d.txt'):
    with open(f'data/k_line_d/sh.000001_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        vvv2=json.loads(f.read())[-MN:]
    AA=vvv2[0][0]
    ZZ=vvv2[-1][0]
    print(AA,ZZ)

if os.path.exists(f'data/k_line_d/sz.399001_d.txt'):
    with open(f'data/k_line_d/sz.399001_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        vvv3=json.loads(f.read())[-MN:]
    if AA==vvv3[0][0] and ZZ==vvv3[-1][0]:
        print(AA,ZZ)
    else:
        print("Err")
    
for dd in ddd:
    vvv=[]
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3" and dd[0] not in ddd4 and dd[1].find("ST")==-1:
        #print(dd[0])
        if os.path.exists(f'data/k_line_d_前复权_计算获得/{dd[0]}_d.txt'):
            with open(f'data/k_line_d_前复权_计算获得/{dd[0]}_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                vvv=json.loads(f.read())
        if len(vvv)>MN+5:  # 剔除上市后前5天的数据
            if vvv[-MN][0]==AA and vvv[-1][0]==ZZ:  # 如何开始与结束日期对齐，即可加载
                uuu[dd[0]]=vvv[-MN:]

for i in range(SS, MN-1):  # 截取倒数第一天的数据
    vvv=[]
    for k in uuu.keys():
        #if uuu[k][i-3][7]>0 and 0>uuu[k][i-2][7]>uuu[k][i-1][7]>uuu[k][i][7]:  # 三天加速下跌
        if uuu[k][i-3][7]>0 and 0>uuu[k][i-2][7] and 0>uuu[k][i-1][7] and 0>uuu[k][i][7]:  # 三天连续下跌
        #if uuu[k][i-2][7]>0 and 0>uuu[k][i-1][7]>uuu[k][i][7]:  # 两天加速下跌
        #if uuu[k][i-2][7]>0 and 0>uuu[k][i-1][7] and 0>uuu[k][i][7]:  # 两天连续下跌
        #if uuu[k][i-3][7]<0 and 0<uuu[k][i-2][7]<uuu[k][i-1][7]<uuu[k][i][7]:  # 三天加速上涨
        #if uuu[k][i-3][7]>0 and 0<uuu[k][i-2][7] and 0<uuu[k][i-1][7] and 0<uuu[k][i][7]:  # 三天连续上涨
        #if uuu[k][i-2][7]>0 and 0<uuu[k][i-1][7]<uuu[k][i][7]:  # 两天加速上涨
        #if uuu[k][i-2][7]>0 and 0<uuu[k][i-1][7] and 0<uuu[k][i][7]:  # 两天连续上涨
            #vvv.append([k,uuu[k][i][7],uuu[k][i][5],uuu[k][i][0]])  # 股票代码，涨跌，收盘，日期
            vvv.append([k,sum([x[9] for x in uuu[k][i-6:i+1]]),uuu[k][i][5],uuu[k][i][0]])  # 股票代码，7日成交额，收盘，日期
            #print(k,uuu[k][i][7],uuu[k][i][5],uuu[k][i][0])
        #elif uuu[k][i][7]>0:  # 第一个上涨卖出
        #elif uuu[k][i][7]<0:  # 第一个下跌卖出
        if k in cang.keys():
            #print(cang)
            #print(k,uuu[k][i][5])
            bal+=(uuu[k][i][5]-cang[k])/cang[k]
            del cang[k]
            fen+=1
            
    #vvv.sort(key=lambda x: x[1], reverse=False)  # 从小到大，因为是下跌
    vvv.sort(key=lambda x: x[1], reverse=True)  # 7日成交额，从大到小
    for vv in vvv:
        if fen>0:
            #if -10.2<vv[1]<=-9.8 and f0(vvv2[i][12])<0 and f0(vvv3[i][12])<0:  # 按最后的跌幅买入
            #if -10.2<vv[1]<=-9.8:  # 按最后的涨幅买入
            if f0(vvv2[i][12])<0 and f0(vvv3[i][12])<0:  # 双指数都下跌买入
                if vv[0] not in cang.keys():
                    #print(vv)
                    cang[vv[0]]=uuu[vv[0]][i][5]  # 以收盘价买入
                    fen-=1
        else:
            break
                    
    #print(f"{bal*100:.2f}%, {fen}")
    
for k in cang.keys():  # 最后持仓的按最后一天的收盘计算收益
    bal+=(uuu[k][-1][5]-cang[k])/cang[k]
    #del cang[k]
    fen+=1
cang={}


print(f"{bal*100:.2f}%, {fen}")


print("-- End --")
