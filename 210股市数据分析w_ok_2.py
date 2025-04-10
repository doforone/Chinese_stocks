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

a="w"  #K线频率
b=1  #汇总几个
for dd in ddd:
    if dd[0][:3]!="of.":
        if dd[4]=="1" and dd[5]=="1" and dd[3]=="":
            print(dd)
        else:
            continue

        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):
            pass
        else:
            continue
        
        with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
            ooo=json.loads(f.read())

        idd=[]
        price_v=[]
        volume_v=[]

        openn=0
        low=0
        high=0
        closee=0
        amount=0
        volume=0
        high_low=(high-low)*2-abs(closee-openn)
                
        n=0
        for oo in ooo:
            if oo[2]!="" and oo[3]!="" and oo[4]!="" and oo[5]!="" and oo[6]!="" and oo[7]!="":
                if n%b==0:
                    if high_low!=0 and volume!=0 and amount!=0:
                        idd.append(oo[0])
                        price_v.append(amount/volume)
                        #high_low=(high-low)*2-abs(closee-openn)
                        volume_v.append(volume/high_low)
                        
                    openn=float(oo[2])
                    low=float(oo[4])
                    high=float(oo[3])
                    closee=float(oo[5])
                    amount=float(oo[7])  #天：为8
                    volume=float(oo[6])  #天：为7
                    high_low=(high-low)*2-abs(closee-openn)
                else:
                    if float(oo[4])!=0 and float(oo[4])<low:
                        low=float(oo[4])
                    if float(oo[3])>high:
                        high=float(oo[3])
                    closee=float(oo[5])
                    amount+=float(oo[7])  #天：为8
                    volume+=float(oo[6])  #天：为7
                    high_low=(high-low)*2-abs(closee-openn)

                n+=1


        #if len(price_v)<100 or price_v[-1]>100:
            #continue
        #else:
            #pass

        img = Image.open("000.png")
        draw =ImageDraw.Draw(img)
        
        draw.line((0, 308-30,1920,308-30), "#cccccc")
        draw.line((0, 308-60,1920,308-60), "#cccccc")
        draw.line((0, 308-90,1920,308-90), "#cccccc")
        draw.line((0, 308-120,1920,308-120), "#cccccc")
        draw.line((0, 308-150,1920,308-150), "#cccccc")
        draw.line((0, 308-180,1920,308-180), "#cccccc")
        draw.line((0, 308-210,1920,308-210), "#cccccc")
        draw.line((0, 308-240,1920,308-240), "#cccccc")
        draw.line((0, 308-270,1920,308-270), "#cccccc")
        draw.line((0, 308-300,1920,308-300), "#cccccc")
        #------------------------
        if (lenn:=len(volume_v))>2:
        #if (lenn:=len(volume_v))>99:
            maxx=max(volume_v)
            minn=min(volume_v)
            #amount_v[volume_v.index(maxx)]=minn  #-----------
            #maxx=max(volume_v)
            
            h_l_1=f"H/L: {round(maxx/minn,3)}"
            maxx_minn=maxx-minn
            i=0
            
            if lenn>1900:
                volume_v=volume_v[-1900:]
                lenn=1900

            year=idd[i][:4]  #取年份
            for vv in volume_v:
                #draw.line((i, 629, i, 629-int(((dd-minn)/maxx_minn)*300)), 'black')
                #draw.line((i, 329, i, 329+int(((dd-minn)/maxx_minn)*300)), 'black')
                draw.line((i, 312, i, 312+int(((vv-minn)/maxx_minn)*300)), 'black')

                if year!=idd[i][:4]:
                #if i==lenn-50 or i==lenn-100:
                    draw.line((i, 312+int(((vv-minn)/maxx_minn)*300),i,619), "#ff0000")
                    year=idd[i][:4]
                i+=1
        #=========================
        #------------------------
        if (lenn:=len(price_v))>2:
            maxx=max(price_v)
            minn=min(price_v)
            #price_v[price_v.index(maxx)]=minn  #------------
            #maxx=max(price_v)
        
            h_l_2=f"H/L: {round(maxx/minn,3)}"
            maxx_minn=maxx-minn
            i=0
        
            if lenn>1900:
                price_v=price_v[-1900:]
                lenn=1900

            year=idd[i][:4]  #取年份
            for pp in price_v:
                draw.line((i, 308, i, 308-int(((pp-minn)/maxx_minn)*300)), 'black')
                
                if year!=idd[i][:4]:
                #if i==lenn-50 or i==lenn-100:
                    draw.line((i, 308-int(((pp-minn)/maxx_minn)*300),i,0), "#ff0000")
                    year=idd[i][:4]
                i+=1
        #=========================

        #=========================
        if len(price_v)>2:
            setFont = ImageFont.truetype('fonts/msyh.ttf', 16)
            fillColor = "#000000"
            width, height = img.size
            #ttt1=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ddd[0][0]/1000))
            ttt1=ooo[0][0]
            ttt2=ooo[-1][0]

            if dd[0] in ddd2.keys():
                classs=ddd2[dd[0]]
            else:
                classs=""
                
            text_size = setFont.getsize(f"{dd[0]} {dd[1]}（{classs}）_{b}{a} ({ttt1}, {ttt2}) ({h_l_2}) {ooo[-1][5]}")
            text_size2 = setFont.getsize(f"({h_l_1})")
            #print(text_size)
            draw.text(((width-text_size[0])/2, 0), f"{dd[0]} {dd[1]}（{classs}）_{b}{a} ({ttt1}, {ttt2}) ({h_l_2}) {ooo[-1][5]}", font=setFont, fill=fillColor)
            draw.text(((width-text_size2[0])/2, height-20), f"({h_l_1})", font=setFont, fill=fillColor)
            
            #Image1.show()
            img.save(f"img_{a}/{dd[0]}_{dd[1].replace('*','')}_{b}{a}.png", "png")


print("--end--")
