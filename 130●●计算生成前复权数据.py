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

##        参数名称	参数描述	说明
##   0    date	交易所行情日期	格式：YYYY-MM-DD
##   1    code	证券代码	格式：sh.600000。sh：上海，sz：深圳
##   2    open	今开盘价格	精度：小数点后4位；单位：人民币元
##   3    high	最高价	精度：小数点后4位；单位：人民币元
##   4    low	最低价	精度：小数点后4位；单位：人民币元
##   5    close	今收盘价	精度：小数点后4位；单位：人民币元
##   6    preclose	昨日收盘价	精度：小数点后4位；单位：人民币元
##   7    volume	成交数量	单位：股
##   8    amount	成交金额	精度：小数点后4位；单位：人民币元
##   9    adjustflag	复权状态	不复权、前复权、后复权
##  10    turn	换手率	精度：小数点后6位；单位：%
##  11    tradestatus	交易状态	1：正常交易 0：停牌
##  12    pctChg	涨跌幅（百分比）	精度：小数点后6位
##  13    peTTM	滚动市盈率	精度：小数点后6位
##  14    psTTM	滚动市销率	精度：小数点后6位
##  15    pcfNcfTTM	滚动市现率	精度：小数点后6位
##  16    pbMRQ	市净率	精度：小数点后6位
##  17    isST	是否ST	1是，0否

##  日期【0】  昨收【1】  开盘【2】  最低【3】  最高【4】  收盘【5】  振幅【6】  涨跌【7】
##  成交量【8】  成交额【9】  换手率【10】  （收开【11】  昨均【12】  均价【13】  均幅【14】  市值【15】）
##  说明：振幅=最高*100/最低-100，收开=（收盘*100/开盘）-100
##  昨均=昨成交额/昨成交量，均幅=（（成交额/成交量）*100）/昨均-100
##  市值=收盘*（成交量*100）/换手率


f0=lambda x: 0.0 if x=="" else float(x)


a="d"
for dd in ddd:
    #print(dd[0])
    #if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0] in ddd3 and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1":
        print(dd)
        ooo=[]
        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):
            with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())

        if ooo!=[] and len(ooo)>5:
            uuu=vvv=[]
            ##  日期【0】  昨收【1】  开盘【2】  最低【3】  最高【4】  收盘【5】  振幅【6】  涨跌【7】  成交量【8】  成交额【9】  换手率【10】
            uuu=[[x[0], round(f0(x[6]),2), round(f0(x[2]),2), round(f0(x[4]),2), round(f0(x[3]),2), round(f0(x[5]),2), round(f0(x[3])*100/f0(x[4])-100,2),\
                 round(f0(x[12]),2), int(f0(x[7])), round(f0(x[8]),2), round(f0(x[10]),4)] for x in ooo]

            # 通过昨日收盘价反向生成前复权数据
            if uuu[-2][8]==0:
                v12=0
            else:
                v12=round(uuu[-2][9]/uuu[-2][8],2)

            if uuu[-1][8]==0:
                v13=0
            else:
                v13=round(uuu[-1][9]/uuu[-1][8],2)

            if v12==0:
                v14=0
            else:
                v14=round(v13*100/v12-100,2)

            if uuu[-1][10]==0:
                v15=0
            else:
                v15=round(uuu[-1][5]*(uuu[-1][8]*100)/uuu[-1][10],2)
            
            vvv=[[uuu[-1][0], round(uuu[-1][1],2), round(uuu[-1][2],2), round(uuu[-1][3],2), round(uuu[-1][4],2), round(uuu[-1][5],2),
                  uuu[-1][6], uuu[-1][7], uuu[-1][8], uuu[-1][9], uuu[-1][10],
                  round(uuu[-1][5]*100/uuu[-1][2]-100,2), v12, v13,
                  v14, v15  ]]
            
            # 以上按倒序取最后一个值
            lenn=len(ooo)
            s=1.0
            for i in range(-2,-lenn-1,-1):
                if uuu[i][5]!=uuu[i+1][1]:  # 收盘不等于下一个的昨收
                    s*=uuu[i+1][1]/uuu[i][5]
                if i==-lenn:

                    v12=round(uuu[i][1]*s,2)

                    if uuu[i][8]==0:
                        v13=0
                    else:
                        v13=round(uuu[i][9]/uuu[i][8],2)

                    if v12==0:
                        v14=0
                    else:
                        v14=round(v13*100/v12-100,2)

                    if uuu[i][10]==0:
                        v15=0
                    else:
                        v15=round(uuu[i][5]*(uuu[i][8]*100)/uuu[i][10],2)
                        
                    vvv.append([uuu[i][0], round(uuu[i][1]*s,2), round(uuu[i][2]*s,2), round(uuu[i][3]*s,2), round(uuu[i][4]*s,2), round(uuu[i][5]*s,2),
                                uuu[i][6], uuu[i][7], uuu[i][8], uuu[i][9], uuu[i][10],
                                round(uuu[i][5]*100/uuu[i][2]-100,2), v12, v13,
                                v14, v15])
                else:
                    if uuu[i-1][8]==0:
                        v12=0
                    else:
                        v12=round(uuu[i-1][9]/uuu[i-1][8],2)

                    if uuu[i][8]==0:
                        v13=0
                    else:
                        v13=round(uuu[i][9]/uuu[i][8],2)

                    if v12==0:
                        v14=0
                    else:
                        v14=round(v13*100/v12-100,2)

                    if uuu[i][10]==0:
                        v15=0
                    else:
                        v15=round(uuu[i][5]*(uuu[i][8]*100)/uuu[i][10],2)
                        
                    vvv.append([uuu[i][0], round(uuu[i][1]*s,2), round(uuu[i][2]*s,2), round(uuu[i][3]*s,2), round(uuu[i][4]*s,2), round(uuu[i][5]*s,2),
                                uuu[i][6], uuu[i][7], uuu[i][8], uuu[i][9], uuu[i][10],
                                round(uuu[i][5]*100/uuu[i][2]-100,2), v12, v13,
                                v14, v15])

            #print(vvv[-1])
            with open(f'data/K_line_d_前复权_计算获得/{dd[0]}_{a}.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                f.write(json.dumps(list(reversed(vvv)), indent=0, ensure_ascii=False)+"\r\n")


print("--end--")
