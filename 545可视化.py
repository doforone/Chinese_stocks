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

#exit()
#quit()
    
#============================
##print(xxx)
##print(yyy1)
##print(yyy2)
##print(yyy3)
##print(yyy4)
##print(yyy5)
##print(yyy6)
##print(yyy7)
##print(yyy8)

print(len(xxx))
print(len(yyy1))
print(len(yyy2))
print(len(yyy3))
print(len(yyy4))
print(len(yyy5))
print(len(yyy6))
print(len(yyy7))
print(len(yyy8))


fig=plt.figure(figsize=(12,8),dpi=72)

plt.rcParams["font.sans-serif"]=['SimHei']
plt.rcParams["axes.unicode_minus"]=False
##plt.rcParams['axes.facecolor'] = '#cc00ff'  #背景色


ax1=fig.add_subplot(111)

plt.xticks(rotation=90)

font = FontProperties(fname="fonts\\msyh.ttf", size=16)
plt.title("价格最低和单位成交额 @ 白点数据", fontsize=22, fontproperties=font, color="#000000", y=1)
#plt.xlabel("时间颗粒（月）：2008-01至2022-04", fontsize=20, fontproperties=font, color="#000000")
#plt.ylabel("单位：万亿人民币", fontsize=20, fontproperties=font, color="#000000")
#plt.xticks(xxx1, ['1月', '2月', '3月', '4月', '5月', '6月', '7月','1月', '2月','1月', '2月', '3月', '4月', '5月', '6月', '7月'], color='#ffff00', fontsize=15)
plt.yticks(color='#000000', fontsize=15)

ax1.set_ylabel('单位：支', color='#000000', fontsize=20)
#---------------------------
x_width=[i-0.2 for i in range(0,len(xxx))]
x2_width=[i+0.2 for i in x_width]
x3_width=[i+0.2 for i in x2_width]
ax1.bar(x_width, yyy1, color="#ff0000", width=0.2, label="价格最低")
ax1.bar(x2_width, yyy2, color="#0000ff", width=0.2, label="单位成交额最高")
ax1.bar(x3_width, yyy3, color="#000000", width=0.2, label="股票总数")
#ax1.bar(x_width, yyy2, color="#ff6600", width=0.4, label="民用汽车拥有量", bottom=yyy1)
##ax1.bar(x2_width, yyy2, color="#ff3300", width=0.4, \
##        label="机动车驾驶员人数")
#ax1.bar(x_width, yyy3, color="#ff00ff", width=0.4, label="涉外及港澳台居民登记结婚", bottom=[i+j for i, j in zip(yyy1,yyy2)])
#ax1.bar(x2_width, yyy4, color="#339900", width=0.4, label="离婚登记")
plt.xticks(range(0,len(xxx)),xxx)

##ax1.bar(xxx, yyy2, color="#00cc00", width=0.5, label="单位成交额新高", bottom=yyy1)
##ax1.bar(xxx, yyy3, color="#cc0000", width=0.5, label="股票总数", \
##        bottom=[i+j for i, j in zip(yyy1,yyy2)])
#---------------------------
##x_width=[i-0.2 for i in range(0,len(xxx))]
##x2_width=[i+0.4 for i in x_width]
##ax1.bar(x_width, yyy1, color="#666666", width=0.4, label="国内生产总值")
##ax1.bar(x2_width, yyy2, color="#999999", width=0.4, label="社会消费品零售总额")
##plt.xticks(range(0,len(xxx)),xxx)
#------------------------

##ax2=ax1.twinx()
##ax2.set_ylabel("单位：%", color="#000000", fontsize=20)
####ax2.plot(xxx, yyy5, color="#0000cc", linestyle='-', marker='o', linewidth=2, \
####         label="0-14岁人口占比")
##ax2.plot(xxx, yyy6, color="#333333", linestyle='-', marker='o', linewidth=2, \
##         label="15-64岁人口占比")
####ax2.plot(xxx, yyy7, color="#cc0000", linestyle='-', marker='o', linewidth=2, \
####         label="65岁及以上人口占比")
###ax2.plot(xxx, yyy4, color="#0000ff", linestyle='-', marker='o', linewidth=2, label="乡村人口同比增加")
###ax2.plot(xxx, yyy3, color="#0000ff", linestyle='-', marker='o', markersize=6, linewidth=2, label="国内生产总值")
###ax2.plot(xxx, yyy4, color="#cc0000", linestyle='-', marker='o', markersize=6, linewidth=2, label="社会消费品零售总额")
##ax2.tick_params(axis='y', color='#000000', labelsize=15, labelcolor='#000000')

##print("5555")
##for a, b, c, d in zip(xxx, yyy1, yyy2, yyy3):
####    if b!=None:
####        plt.text(a, b+0.1, '%.2f' % b, ha='left', va='bottom', fontsize=15, color='#0000cc')
##
##    if c!=None:
##        plt.text(a, c+0.1, '%.2f' % c, ha='left', va='bottom', fontsize=15, color='#333333')
##
####    if d!=None:
####        plt.text(a, d+0.1, '%.2f' % d, ha='left', va='bottom', fontsize=15, color='#cc0000')
##print("6666")
##ax=plt.gca()
###ax.axes.xaxis.set_visible(False)
###ax.axes.yaxis.set_visible(False)
###ax.axes.xaxis.set_ticks([0,4,8])
###ax.axes.yaxis.set_ticks([])

print("7777")
plt.legend(loc="upper left", fontsize=18)
plt.grid(True)
plt.xticks(rotation=90)
plt.tick_params(labelsize=18)

print("8888")
ax1.legend(loc="upper left", fontsize=18)
##ax2.legend(loc="upper right", fontsize=18)
#ax1.grid(b=True,axis="both")
#ax1.grid(b=True,axis="y")
ax1.grid(b=True)
#plt.xticks(rotation=90)
ax1.tick_params(labelsize=18)

print("9999")
#plt.savefig("000.png",dpi=10,bbox_inches = 'tight')
plt.savefig("545.png", dpi=72, bbox_inches = 'tight')
print("0000")

plt.show()

