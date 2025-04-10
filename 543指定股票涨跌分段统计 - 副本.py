##白点数据，运行环境python3.8


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

##      参数名称	参数描述	说明
## 0    date	交易所行情日期	格式：YYYY-MM-DD
## 1    code	证券代码	格式：sh.600000。sh：上海，sz：深圳
## 2    open	今开盘价格	精度：小数点后4位；单位：人民币元
## 3    high	最高价	精度：小数点后4位；单位：人民币元
## 4    low	最低价	精度：小数点后4位；单位：人民币元
## 5    close	今收盘价	精度：小数点后4位；单位：人民币元
## 6    preclose	昨日收盘价	精度：小数点后4位；单位：人民币元  #复权后的数据
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
    if a=="":
        return 0.0
    else:
        return float(a)

a="d"
AV=1.03
rrr={9:0,8:0,7:0,6:0,5:0,4:0,3:0,2:0,1:0,0:0,-1:0,-2:0,-3:0,-4:0,-5:0,-6:0,-7:0,-8:0,-9:0,-10:0}

for dd in ddd:
##    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0] in ddd3 \
##       and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
    if dd[0]=="sh.000001":

        if os.path.exists(f'data/k_line_{a}_前复权/{dd[0]}_{a}.txt'):
            with open(f'data/k_line_{a}_前复权/{dd[0]}_{a}.txt', 'r', \
                      encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())

        if ooo!=[]:
##            uuu=[[x[0], float_000(x[6]), float_000(x[2]), float_000(x[4]),
##                  float_000(x[3]), float_000(x[5]),
##                  float(x[3])-min([float(x[4]),float(x[6])]),
##                  float_000(x[12]), float_000(x[7]), float_000(x[8]),
##                  float_000(x[10])] for x in ooo]

##            uuu=[[x[0], float_000(x[6]), float_000(x[2]), float_000(x[4]),
##                  float_000(x[3]), float_000(x[5]),
##                  float(x[3])-min([float(x[4]),float(x[6])]),
##                  abs((float(x[5])-float(x[6]))/float(x[6])), float_000(x[7]), float_000(x[8]),
##                  float_000(x[10])] for x in ooo]

            #uuu=[[x[0], float_000(x[8])/float_000(x[7])] for x in ooo]
##            uuu=[float_000(x[8])/float_000(x[7]) for x in ooo if float_000(x[7])>0]

            for oo in ooo:
                oo_12=float_000(oo[12])
                if oo_12>=9:
                    rrr[9]+=1
                elif oo_12>=8:
                    rrr[8]+=1
                elif oo_12>=7:
                    rrr[7]+=1
                elif oo_12>=6:
                    rrr[6]+=1
                elif oo_12>=5:
                    rrr[5]+=1
                elif oo_12>=4:
                    rrr[4]+=1
                elif oo_12>=3:
                    rrr[3]+=1
                elif oo_12>=2:
                    rrr[2]+=1
                elif oo_12>=1:
                    rrr[1]+=1
                elif oo_12>=0:
                    rrr[0]+=1
                elif oo_12>=-1:
                    rrr[-1]+=1
                elif oo_12>=-2:
                    rrr[-2]+=1
                elif oo_12>=-3:
                    rrr[-3]+=1
                elif oo_12>=-4:
                    rrr[-4]+=1
                elif oo_12>=-5:
                    rrr[-5]+=1
                elif oo_12>=-6:
                    rrr[-6]+=1
                elif oo_12>=-7:
                    rrr[-7]+=1
                elif oo_12>=-8:
                    rrr[-8]+=1
                elif oo_12>=-9:
                    rrr[-9]+=1
                else:
                    rrr[-10]+=1


#print(rrr)
for rr in rrr.keys():
    print(f"{str(rr).rjust(3)}: {rrr[rr]}")
                    
##print(f"{AV} ------------:")
##rrr2=sorted(rrr, key=lambda x: x[3], reverse=True)
##
##for rr2 in rrr2[:100]:
##    print(rr2)

print("--end--")
