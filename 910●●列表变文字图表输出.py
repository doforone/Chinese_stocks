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

with open('data/每年都有分红的股票.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd3=json.loads(f.read())

##      参数名称	参数描述	说明
## 0    date	交易所行情日期	格式：YYYY-MM-DD
## 1    code	证券代码	格式：sh.600000。sh：上海，sz：深圳
## 2    open	今开盘价格	精度：小数点后4位；单位：人民币元
## 3    high	最高价	精度：小数点后4位；单位：人民币元
## 4    low	最低价	精度：小数点后4位；单位：人民币元
## 5    close	今收盘价	精度：小数点后4位；单位：人民币元
## 6    preclose	昨日收盘价	精度：小数点后4位；单位：人民币元
## 7    volume	成交数量	单位：股
## 8    amount	成交金额	精度：小数点后4位；单位：人民币元
## 9    adjustflag	复权状态	不复权、前复权、后复权
##10    turn	换手率	精度：小数点后6位；单位：%
##11    tradestatus	交易状态	1：正常交易 0：停牌
##12    pctChg	涨跌幅（百分比）	精度：小数点后6位
##13    peTTM	滚动市盈率	精度：小数点后6位
##14    psTTM	滚动市销率	精度：小数点后6位
##15    pcfNcfTTM	滚动市现率	精度：小数点后6位
##16    pbMRQ	市净率	精度：小数点后6位
##17    isST	是否ST	1是，0否

#日期【0】  昨收【1】  开盘【2】  最低【3】  最高【4】  收盘【5】
#振幅【6】  涨跌【7】  成交量【8】  成交额【9】  换手率【10】


def float_000(a):
    return 0.0 if a=="" else float(a)


def list_chart(ddd: list, a="@", title="")->str:
    # 说明ddd为两列列表，第一列为字符串，如日期，但不能有中文，第二列为数字。
    maxx=max([x[1] for x in ddd])
    minn=min([x[1] for x in ddd])
    print(f"{title}  max:{maxx}  min:{minn}")
    ddd2=[int((x[1]-minn)*100/(maxx-minn)) for x in ddd]
    for i in range(100, -1, -2):
        sss=""
        for dd in ddd2:
            if dd==i:
                sss+="-"
            elif dd==i-1:
                sss+="_"
            elif dd>i:
                sss+=a
            else:
                sss+=" "
        if i%10==0:
            print(sss+"=|"+str(round(minn+((maxx-minn)*(i//10))/10, 2)))
        else:
            print(sss+" |")

    maxx2=max([len(x[0]) for x in ddd])
    ddd3=[x[0] for x in ddd]
    print("+"*len(ddd)+"-+")
    for i in range(maxx2):
        sss=""
        for dd in ddd3:
            if len(dd)>i:
                sss+=dd[i]
            else:
                sss+=" "
        print(sss)

    return "ok"


def list_chart2(ddd: list)->str:
    # 说明ddd为三列列表，第一列为字符串，如日期，但不能有中文，第二、三列为数字，数字为相同单位。
    maxx=max([max([x[1] for x in ddd]), max([x[2] for x in ddd])])
    minn=min([min([x[1] for x in ddd]), min([x[2] for x in ddd])])
    print(f"max:{maxx}  min:{minn}")
    ddd2=[int((x[1]-minn)*100/(maxx-minn)) for x in ddd]
    ddd3=[int((x[2]-minn)*100/(maxx-minn)) for x in ddd]
    for i in range(100, -1, -2):
        sss=""
        for j in range(len(ddd)):
            if ddd2[j]==i:
                sss+="-"
            elif ddd2[j]==i-1:
                sss+="_"
            elif ddd2[j]>i:
                sss+="@"
            else:
                sss+=" "

            if ddd3[j]==i:
                sss+="-"
            elif ddd3[j]==i-1:
                sss+="_"
            elif ddd3[j]>i:
                sss+="#"
            else:
                sss+=" "
                
        if i%10==0:
            print(sss+"=|"+str(round(minn+((maxx-minn)*(i//10))/10, 2)))
        else:
            print(sss+" |")

    maxx2=max([len(x[0]) for x in ddd])
    ddd3=[x[0] for x in ddd]
    print("+-"*len(ddd)+"-+")
    for i in range(maxx2):
        sss=""
        for dd in ddd3:
            if len(dd)>i:
                sss+=dd[i]+" "
            else:
                sss+="  "
        print(sss)

    return "ok"


rrr={}
a="d"
for dd in ddd:
    #print(dd[0])
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0] in ddd3 and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1":
        #print(dd)
        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):  #使用不复权数据
            with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())

        if ooo!=[] and len(ooo)>=200:  # 因为最低取10天的
            for oo in ooo[-200:]:
                if oo[0] not in rrr.keys():
                    rrr[oo[0]]={"A":0, "O":0, "V":0}
                if float_000(oo[12])>0:
                    rrr[oo[0]]["A"]+=1
                elif float_000(oo[12])==0:
                    rrr[oo[0]]["O"]+=1
                else:
                    rrr[oo[0]]["V"]+=1


###ddd2=[[x[0],x[1]["A"]/x[1]["V"]] for x in list(rrr.items())[:100]]
ddd2=[[x[0],x[1]["A"]] for x in rrr.items()]  # 上涨
ddd2.sort(key=lambda x: x[0])
r=list_chart(ddd2[-175:], "@", "主板上涨股票数量")
print(r)


ddd2=[[x[0],x[1]["V"]] for x in rrr.items()]  # 下跌
ddd2.sort(key=lambda x: x[0])
r=list_chart(ddd2[-175:], "@", "主板下跌股票数量")
print(r)


##ddd2=[[x[0],x[1]["A"],x[1]["V"]] for x in rrr.items()]
##ddd2.sort(key=lambda x: x[0])
##r=list_chart2(ddd2[-80:])
##print(r)

print("--end--")
