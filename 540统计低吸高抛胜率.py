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

#### 日K线参数名称及定义 ####
##       参数名称	参数描述	说明
##  0    date	交易所行情日期	格式：YYYY-MM-DD
##  1    code	证券代码	格式：sh.600000。sh：上海，sz：深圳
##  2    open	今开盘价格	精度：小数点后4位；单位：人民币元
##  3    high	最高价	精度：小数点后4位；单位：人民币元
##  4    low	最低价	精度：小数点后4位；单位：人民币元
##  5    close	今收盘价	精度：小数点后4位；单位：人民币元
##  6    preclose	昨日收盘价	精度：小数点后4位；单位：人民币元
##  7    volume	成交数量	单位：股
##  8    amount	成交金额	精度：小数点后4位；单位：人民币元
##  9    adjustflag	复权状态	不复权、前复权、后复权
## 10    turn	换手率	精度：小数点后6位；单位：%
## 11    tradestatus	交易状态	1：正常交易 0：停牌
## 12    pctChg	涨跌幅（百分比）	精度：小数点后6位
## 13    peTTM	滚动市盈率	精度：小数点后6位
## 14    psTTM	滚动市销率	精度：小数点后6位
## 15    pcfNcfTTM	滚动市现率	精度：小数点后6位
## 16    pbMRQ	市净率	精度：小数点后6位
## 17    isST	是否ST	1是，0否

## 日期【0】  昨收【1】  开盘【2】  最低【3】  最高【4】  收盘【5】
## 振幅【6】  涨跌【7】  成交量【8】  成交额【9】  换手率【10】

def float_000(a):
    return 0.0 if a=="" else float(a)

# 说明，每次买入固定金额的股票，所以我们只累计本次卖出后的收益率，
# 我们不考虑资金收益的复用和资金是否充分流动及开盘买入或卖出时的价格缺口，
# 同样我们也不考虑交易成本。

a="d"
moneyy=10000  #初始资金
incomee0=1  #总自然收益，等于回测时间段的最后收盘价/最初开盘价
incomee1=1  #总策略收益
dayy=0
n=0  #总交易次数
for dd in ddd:
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0] not in ddd3 and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3":  # 可调整控制

        if os.path.exists(f'data/k_line_{a}_前复权/{dd[0]}_{a}.txt'):  # 用前复权数据
            with open(f'data/k_line_{a}_前复权/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())

        if ooo!=[]:
            if (lenn:=len(ooo))>8:  # 一般上市新股前5天没有涨跌停，所以5+3
                cang=0  # 初始空仓
                T_moneyy=10000  # 初始金额，不考虑100手的问题——于统计计算来说不是问题，每只股票的初始资金相同
                T_n=0  #本交易次数
                for i in range(8,lenn):
                    if cang==0:
                        if float_000(ooo[i-3][12])>0 and 0>float_000(ooo[i-2][12])>float_000(ooo[i-1][12]):  # 因为每天买或卖只一次，所以用涨跌幅，参数可调
                            cang=T_moneyy/float_000(ooo[i][2])  # 开盘价买入，不考虑集合竞价因素及开盘价是否跳多还是跳空
                    else:
                        if float_000(ooo[i-1][12])>9.0 or i==lenn-1:  # 上涨卖出，参数可调
                            T_moneyy=float_000(ooo[i][2])*cang  # 开盘价卖出
                            cang=0
                            T_n+=1
                            n+=1
                incomee0+=float_000(ooo[-1][2])/float_000(ooo[7][2])
                incomee1+=T_moneyy/10000  # 策略收益，10000为本只股票的初始资金
                dayy+=lenn-8
            print(f"{dd[0]}，{dd[1]}({ddd2[dd[0]]})，交易天数：{lenn-8}，策略交易占比【{round(T_n/(lenn-8),2)}】，\
策略收益【{round(T_moneyy/10000,2)}】，自然收益【{round(float_000(ooo[-1][2])/float_000(ooo[7][2]),2)}】")
            
print(f"总计:股票上市天数累计：{dayy}，策略交易占比【{round(n/(dayy),2)}】，策略收益【{round(incomee1,2)}】，自然收益【{round(incomee0,1)}】")

print("--end--")
