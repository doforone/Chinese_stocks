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


rrr0={"累积":0, "次数":0}
rrr1={"累积":0, "次数":0}
rrr2={"累积":0, "次数":0}
rrr3={"累积":0, "次数":0}
rrr4={"累积":0, "次数":0}
rrr5={"累积":0, "次数":0}
rrr6={"累积":0, "次数":0}
rrr7={"累积":0, "次数":0}
rrr8={"累积":0, "次数":0}
rrr9={"累积":0, "次数":0}

for dd in ddd:
    uuu=[]
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1" and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3" and dd[0] not in ddd4 and dd[1].find("ST")==-1:
        #print(dd[0])
        if os.path.exists(f'data/k_line_d_前复权_计算获得/{dd[0]}_d.txt'):
            with open(f'data/k_line_d_前复权_计算获得/{dd[0]}_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                uuu=json.loads(f.read())[-900:]

            mn=7
            for i,uu in enumerate(uuu[mn:-1]):
                if uuu[i+mn-2][7]<0 and uuu[i+mn-1][7]>0:
                    if uu[7]>=9:
                        rrr9["累积"]+=uuu[i+mn+1][7]
                        rrr9["次数"]+=1
                    elif uu[7]>=8:
                        rrr8["累积"]+=uuu[i+mn+1][7]
                        rrr8["次数"]+=1
                    elif uu[7]>=7:
                        rrr7["累积"]+=uuu[i+mn+1][7]
                        rrr7["次数"]+=1
                    elif uu[7]>=6:
                        rrr6["累积"]+=uuu[i+mn+1][7]
                        rrr6["次数"]+=1
                    elif uu[7]>=5:
                        rrr5["累积"]+=uuu[i+mn+1][7]
                        rrr5["次数"]+=1
                    elif uu[7]>=4:
                        rrr4["累积"]+=uuu[i+mn+1][7]
                        rrr4["次数"]+=1
                    elif uu[7]>=3:
                        rrr3["累积"]+=uuu[i+mn+1][7]
                        rrr3["次数"]+=1
                    elif uu[7]>=2:
                        rrr2["累积"]+=uuu[i+mn+1][7]
                        rrr2["次数"]+=1
                    elif uu[7]>=1:
                        rrr1["累积"]+=uuu[i+mn+1][7]
                        rrr1["次数"]+=1
                    elif uu[7]>=0:
                        rrr0["累积"]+=uuu[i+mn+1][7]
                        rrr0["次数"]+=1

print("所有统计均没有考虑交易手续费，及第二日的最低价是否低于前一日的收盘价——即第二日K线是否覆盖前日收盘价。")
print(f"当日上涨超过9%，第二日累积涨跌：{rrr9['累积']:.2f}，次数：{rrr9['次数']}，平均：{rrr9['累积']/rrr9['次数']:.2f}%")
print(f"当日涨跌在9%与8%(含)之间，第二日累积涨跌：{rrr8['累积']:.2f}，次数：{rrr8['次数']}，平均：{rrr8['累积']/rrr8['次数']:.2f}%")
print(f"当日涨跌在8%与7%(含)之间，第二日累积涨跌：{rrr7['累积']:.2f}，次数：{rrr7['次数']}，平均：{rrr7['累积']/rrr7['次数']:.2f}%")
print(f"当日涨跌在7%与6%(含)之间，第二日累积涨跌：{rrr6['累积']:.2f}，次数：{rrr6['次数']}，平均：{rrr6['累积']/rrr6['次数']:.2f}%")
print(f"当日涨跌在6%与5%(含)之间，第二日累积涨跌：{rrr5['累积']:.2f}，次数：{rrr5['次数']}，平均：{rrr5['累积']/rrr5['次数']:.2f}%")
print(f"当日涨跌在5%与4%(含)之间，第二日累积涨跌：{rrr4['累积']:.2f}，次数：{rrr4['次数']}，平均：{rrr4['累积']/rrr4['次数']:.2f}%")
print(f"当日涨跌在4%与3%(含)之间，第二日累积涨跌：{rrr3['累积']:.2f}，次数：{rrr3['次数']}，平均：{rrr3['累积']/rrr3['次数']:.2f}%")
print(f"当日涨跌在3%与2%(含)之间，第二日累积涨跌：{rrr2['累积']:.2f}，次数：{rrr2['次数']}，平均：{rrr2['累积']/rrr2['次数']:.2f}%")
print(f"当日涨跌在2%与1%(含)之间，第二日累积涨跌：{rrr1['累积']:.2f}，次数：{rrr1['次数']}，平均：{rrr1['累积']/rrr1['次数']:.2f}%")
print(f"当日涨跌在1%与0%(含)之间，第二日累积涨跌：{rrr0['累积']:.2f}，次数：{rrr0['次数']}，平均：{rrr0['累积']/rrr0['次数']:.2f}%")


print("-- End --")
