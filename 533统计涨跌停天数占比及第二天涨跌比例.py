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
    if a=="":
        return 0.0
    else:
        return float(a)

a="d"
A=0  #涨停计数
AA=0
AV=0
V=0  #跌停计数
VA=0
VV=0
n=0  #总交易天数

for dd in ddd:
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0] in ddd3 \
       and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":

        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):
            with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', \
                      encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())

        if ooo!=[]:
            uuu=[[x[0], float_000(x[6]), float_000(x[2]), float_000(x[4]),
                  float_000(x[3]), float_000(x[5]),
                  float(x[3])-min([float(x[4]),float(x[6])]),
                  float_000(x[12]), float_000(x[7]), float_000(x[8]),
                  float_000(x[10])] for x in ooo]

            A0=0  #本股票涨停计数
            AA0=0
            AV0=0
            V0=0  #本股票跌停计数
            VA0=0
            VV0=0
            #for i in range(len(uuu)-1):
            for i in range(len(uuu)-2):
                if uuu[i][7]>9.8:
                    A0+=1
                    A+=1
                    #if uuu[i+1][7]>0:
                    #if uuu[i+1][5]>uuu[i+1][2]:  #第二天收盘大于开盘
                    #由于高开低走及T+1的原因，改为第三天的开盘减去第二天的开盘
                    if uuu[i+2][2]>uuu[i+1][2]:
                        AA0+=1
                        AA+=1
                    #elif uuu[i+1][7]<0:
                    #elif uuu[i+1][5]<uuu[i+1][2]:
                    elif uuu[i+2][2]<uuu[i+1][2]:
                        AV0+=1
                        AV+=1
                elif uuu[i][7]<-9.8:
                    V0+=1
                    V+=1
                    #if uuu[i+1][7]>0:
                    #if uuu[i+1][5]>uuu[i+1][2]:  #第二天收盘大于开盘
                    #由于高开低走及T+1的原因，改为第三天的开盘减去第二天的开盘
                    if uuu[i+2][2]>uuu[i+1][2]:
                    #if uuu[i+1][2]>uuu[i][5]:  #当日尾盘买入，第二天开盘卖出
                        VA0+=1
                        VA+=1
                    #elif uuu[i+1][7]<0:
                    #elif uuu[i+1][5]<uuu[i+1][2]:
                    elif uuu[i+2][2]<uuu[i+1][2]:
                    #elif uuu[i+1][2]<uuu[i][5]:  #当日尾盘买入，第二天开盘卖出
                        VV0+=1
                        VV+=1

            n+=len(uuu)
            if A0==0: A0=0.01
            if V0==0: V0=0.01
##            print(f"{dd[0]}，{dd[1]}({ddd2[dd[0]]})，交易天数：{len(uuu)}，\
##涨停占比【{round(A0/len(uuu)*100,2)}%】，\
##第二日上涨占比▲{round(AA0/A0*100,2)}%，\
##第二日下跌占比▼{round(AV0/A0*100,2)}%，\
##跌停占比【{round(V0/len(uuu)*100,2)}%】，\
##第二日上涨占比▲{round(VA0/V0*100,2)}%，\
##第二日下跌占比▼{round(VV0/V0*100,2)}%\
##")
##            print("------------")
            
print(f"●交易天数累计：{n}，\
涨停占比【{round(A/n*100,2)}%】，\
第二日上涨占比▲{round(AA/A*100,2)}%，\
第二日下跌占比▼{round(AV/A*100,2)}%，\
跌停占比【{round(V/n*100,2)}%】，\
第二日上涨占比▲{round(VA/V*100,2)}%，\
第二日下跌占比▼{round(VV/V*100,2)}%\
")

print("--end--")
