# -*- coding: UTF-8 -*-

#==========================
import time
import json
import random
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


xxx=[]
yyy1=[]
yyy2=[]
yyy3=[]
yyy4=[]
yyy5=[]
yyy6=[]
yyy7=[]
yyy8=[]

#=====================
with open('545.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

xxx=[x for x in sorted(ddd.keys())]
yyy1=[ddd[x][0] for x in xxx]
yyy2=[ddd[x][1] for x in xxx]
yyy3=[ddd[x][2] for x in xxx]
for i in range(len(xxx)):
    print(f"{xxx[i]}，价格最低数：{yyy1[i]}，单位成交额创新高数{yyy2[i]}，股票总数{yyy3[i]}")
##    print()
##    print(xxx[i])
##    print("".rjust(yyy1[i],"-"))
##    print("".rjust(yyy2[i],"*"))


##zzz=sorted(ddd.items(), key=lambda x:x[1][1]/x[1][2], reverse=True)
##
##for zz in zzz:
##    print(zz)
