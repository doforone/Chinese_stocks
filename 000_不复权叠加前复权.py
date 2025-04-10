
import time
import json
import random
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ooo=json.loads(f.read())

with open('data/行业分类2.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    uuu=json.loads(f.read())

for oo in ooo:
    xxx=[]
    yyy1=[]
    yyy2=[]
    yyy3=[]
    yyy4=[]
    yyy5=[]
    yyy6=[]
    
    if oo[0][:3]!="of.":
        if oo[4]=="1" and oo[5]=="1" and oo[3]=="":  #股票
            print(oo)
        else:
            continue
        
        with open(f'data\\K_line_d\{oo[0]}_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
            ddd=json.loads(f.read())
            
        for dd in ddd:
            xxx.append(dd[0])
            yyy1.append(float(dd[5]))

        with open(f'data\\K_line_d_前复权\{oo[0]}_d.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
            ddd=json.loads(f.read())
            
        for dd in ddd:
            yyy2.append(float(dd[5]))

        print(len(xxx))
        print(len(yyy1))
        print(len(yyy2))
        print(len(yyy3))
        print(len(yyy4))
        print(len(yyy5))
        print(len(yyy6))


        plt.figure(figsize=(22,12),dpi=72)

        plt.rcParams["font.sans-serif"]=['SimHei']
        plt.rcParams["axes.unicode_minus"]=False

        ax=plt.gca()
        #ax.axes.xaxis.set_visible(False)
        #ax.axes.yaxis.set_visible(False)

        a=""
        x=[]
        for i in range(len(xxx)):
            if xxx[i][:4]!=a:
                x.append(i)
                a=xxx[i][:4]

        #ax.axes.xaxis.set_ticks([0,len(xxx)//4,len(xxx)//2,len(xxx)*3//4,len(xxx)-1])
        ax.axes.xaxis.set_ticks(x)
        #ax.axes.yaxis.set_ticks([])

        ##plt.bar(xxx1, yyy1, color="#000000", alpha = 1, width=1, label="社会融资规模增量")
        ##plt.bar(xxx1, yyy2, color="#ff0000", alpha = .5, width=1, label="人民币贷款增量")
        ##plt.bar(xxx1, yyy3, color="#00ff00", alpha = .5, width=1, label="企业债券增量")
        ##plt.bar(xxx1, yyy4, color="#0000ff", alpha = .5, width=1, label="政府债券增量")

        plt.plot(xxx, yyy1, color="#000000", linewidth=1, label="不复权")
        plt.fill_between(xxx, yyy1, color='#000000',alpha=0.5)
        plt.plot(xxx, yyy2, color="#ffff00", linewidth=1, label="前复权")
        plt.fill_between(xxx, yyy2, color='#ffff00',alpha=0.5)


        #plt.fill_between(x, yTop, yBottom ,color="lightgreen",label="Standard deviation")#填充色块

        font = FontProperties(fname="fonts\\msyh.ttf", size=16)

        if oo[0] in uuu.keys():
            classs=uuu[oo[0]]
        else:
            classs=""
            
        plt.title(f"{oo[0]} {oo[1]}（{classs}）_d 不复权叠加前复权 @ 白点数据", fontsize=22, fontproperties=font, color="#000000")
                
        plt.xlabel(f"{oo[0]} {oo[1]}（{classs}）", fontsize=20, fontproperties=font, color="#000000")
        plt.ylabel("", fontsize=20, fontproperties=font, color="#000000")



        plt.legend(loc="upper left", fontsize=18)
        plt.grid(True)
        plt.xticks(rotation=90)
        plt.tick_params(labelsize=18)


        #plt.savefig("000.png",dpi=10,bbox_inches = 'tight')
        plt.savefig(f"img_d_不复权叠加前复权/{oo[0]}_{oo[1].replace('*','x')}（{classs}）.png", dpi=72, bbox_inches = 'tight')

        #plt.show()

        #plt.close()
        plt.close('all')

print("--end--")

