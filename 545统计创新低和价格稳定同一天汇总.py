import baostock as bs
import pandas as pd

import json
from PIL import Image, ImageDraw,ImageFont
import datetime
import os

with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

with open('data/行业分类2.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd2=json.loads(f.read())

with open('data/每年都有分红的股票.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd3=json.loads(f.read())

##date	交易所行情日期	格式：YYYY-MM-DD	
##code	证券代码	格式：sh.600000。sh：上海，sz：深圳	
##open	开盘价格	精度：小数点后4位；单位：人民币元	
##high	最高价	精度：小数点后4位；单位：人民币元	
##low	最低价	精度：小数点后4位；单位：人民币元	
##close	收盘价	精度：小数点后4位；单位：人民币元	
##volume	成交数量	单位：股	
##amount	成交金额	精度：小数点后4位；单位：人民币元	
##adjustflag	复权状态	不复权、前复权、后复权	
##turn	换手率	精度：小数点后6位；单位：%	
##pctChg	涨跌幅（百分比）	精度：小数点后6位	涨跌幅=[(区间最后交易日收盘价-区间首个交易日前收盘价)/区间首个交易日前收盘价]*100%

#日期【0】  昨收【1】  开盘【2】  最低【3】  最高【4】  收盘【5】
#振幅【6】  涨跌【7】  成交量【8】  成交额【9】  换手率【10】


def float_000(a):
    if a=="":
        return 0.0
    else:
        return float(a)


a="w"  #K线频率
rrr={}
for dd in ddd:
    if dd[0][:3]!="of." and dd[0] in ddd3 and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":  #正常使用
    #if dd[0]=="sh.000001" or dd[0]=="sz.399001":
    #if 1==1:
        if dd[4]=="1" and dd[5]=="1" and dd[3]=="":  #股票  正常使用
        #if dd[4]=="2" and dd[5]=="1" and dd[3]=="":  #指数
        #if 1==1:
            print(dd)
        else:
            continue

        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):  #不复权数据
            pass
        else:
            continue
        
        with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
            ooo=json.loads(f.read())
            P_minn=float_000(ooo[0][4])
            if (float_000(ooo[0][3])-float_000(ooo[0][4]))*2-abs(float_000(ooo[0][5])-float_000(ooo[0][2]))==0:
                dP_maxx=0
            else:
                dP_maxx=float_000(ooo[0][7])/((float_000(ooo[0][3])-float_000(ooo[0][4]))*2-abs(float_000(ooo[0][5])-float_000(ooo[0][2])))
            for oo in ooo:
                if oo[0] in rrr.keys():
                    rrr[oo[0]][2]+=1
                else:
                    rrr[oo[0]]=[0,0,1]

                if float_000(oo[4])<P_minn:
                    P_minn=float_000(oo[4])
                    rrr[oo[0]][0]+=1

                if (sP:=((float_000(oo[3])-float_000(oo[4]))*2-abs(float_000(oo[5])-float_000(oo[2]))))!=0:
                    if float_000(oo[7])/sP>dP_maxx:
                        dP_maxx=float_000(oo[7])/sP
                        rrr[oo[0]][1]+=1


with open('545.txt', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(json.dumps(rrr, indent=4, ensure_ascii=False)+"\r\n")

print("--end--")
