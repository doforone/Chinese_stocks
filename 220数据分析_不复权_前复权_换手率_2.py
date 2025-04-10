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

a="d"  #K线频率
b=5  #汇总几个
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

        if os.path.exists(f'data/k_line_{a}/{dd[0]}_{a}.txt'):
            pass
        else:
            continue
        
        with open(f'data/k_line_{a}/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
            ooo=json.loads(f.read())[-1280*b:]
            #print(len(ooo))
            #ooo2={x[0]:x for x in ooo}
            #vvv={x[0]:[] for x in ooo}

        with open(f'data/k_line_{a}_前复权/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
            uuu=json.loads(f.read())[-1280*b:]
            #uuu2={x[0]:x for x in uuu}

        for i in range(len(ooo)-len(uuu)):
            uuu.append([])
        #print(len(uuu))

        idd=[]
        price_v=[]
        price2_v=[]
        volume_v=[]
        volume_a=[]  #----------

        openn=0
        low=0
        high=0
        closee=0
        amount=0
        volume=0
        turn=0
        high_low=(high-low)*2-abs(closee-openn)
                
        n=1
        h1=1
        h2=1
        p1=0
        p2=0
        for i in range(len(ooo)-1,-1,-1):  #==注意倒序
            if n%b==0:
                if uuu[i]==[] or uuu[i][2]==uuu[i][3]==uuu[i][4]==uuu[i][5]:
                    h2=0
                    
                if ooo[i][5]=="" or ooo[i][10]=="" or ooo[i][2]==ooo[i][3]==ooo[i][4]==ooo[i][5]:
                    h1=0

                idd.append(ooo[i][0])

                if h2==0:
                    price2_v.append(None)
                else:
                    p2+=float(uuu[i][5])
                    price2_v.append(p2/b)

                if h1==0:
                    price_v.append(None)
                    volume_v.append(None)
                    volume_a.append(None)  #----------
                else:
                    if float(ooo[i][4])!=0 and float(ooo[i][4])<low:
                        low=float(ooo[i][4])
                    if float(ooo[i][3])>high:
                        high=float(ooo[i][3])
                    closee=float(ooo[i][5])
                    amount+=float(ooo[i][8])  #成交金额
                    volume+=float(ooo[i][7])  #成交量

                    p1+=closee
                    turn+=float(ooo[i][10])
                    high_low=(high-low)*2-abs(closee-openn)
                    

                    #idd.append(ooo[i][0])
                    #price_v.append(amount/volume)
                    #high_low=(high-low)*2-abs(closee-openn)
                    #volume_v.append(volume/high_low)
                    #volume_v.append(amount/high_low)  #因为股票有送股，送股后股票变多，所以改为了用成交金额，这样更合理

                    price_v.append(p1/b)
                    volume_v.append(turn/high_low)  #因为换手率是按流通股算的，所以按换手率比较科学。
                    volume_a.append(turn)  #----------
                    
                h1=1
                h2=1

            elif n%b==1:
                #print(i)
                if uuu[i]==[] or uuu[i][2]==uuu[i][3]==uuu[i][4]==uuu[i][5]:
                    h2=0
                    
                if ooo[i][5]=="" or ooo[i][10]=="" or ooo[i][2]==ooo[i][3]==ooo[i][4]==ooo[i][5]:
                    h1=0

                if h1==1:
                    openn=float(ooo[i][2])
                    low=float(ooo[i][4])
                    high=float(ooo[i][3])
                    closee=float(ooo[i][5])
                    amount=float(ooo[i][8])
                    volume=float(ooo[i][7])

                    p1=closee
                    turn=float(ooo[i][10])
                    
                if h2==1:
                    p2=float(uuu[i][5])

            else:
                if uuu[i]==[] or uuu[i][2]==uuu[i][3]==uuu[i][4]==uuu[i][5]:
                    h2=0
                    
                if ooo[i][5]=="" or ooo[i][10]=="" or ooo[i][2]==ooo[i][3]==ooo[i][4]==ooo[i][5]:
                    h1=0
                    
                if h1==1:
                    if float(ooo[i][4])!=0 and float(ooo[i][4])<low:
                        low=float(ooo[i][4])
                    if float(ooo[i][3])>high:
                        high=float(ooo[i][3])
                    closee=float(ooo[i][5])
                    amount+=float(ooo[i][8])
                    volume+=float(ooo[i][7])

                    p1+=closee
                    turn+=float(ooo[i][10])
                    
                if h2==1:
                    p2+=float(uuu[i][5])

            n+=1


            
##        for oo in ooo[::-1]:  #==注意倒序
##            if oo[2]!="" and oo[3]!="" and oo[4]!="" and oo[5]!="" and oo[6]!="" and oo[7]!="":
##                if n%b==0:
##                    if float(oo[4])!=0 and float(oo[4])<low:
##                        low=float(oo[4])
##                    if float(oo[3])>high:
##                        high=float(oo[3])
##                    closee=float(oo[5])
##                    amount+=float(oo[8])  #成交金额
##                    volume+=float(oo[7])  #成交量
##                    if oo[10]=="":
##                        turn+=0
##                    else:
##                        turn+=float(oo[10])
##                    high_low=(high-low)*2-abs(closee-openn)
##                    
##                    if high_low!=0 and volume!=0 and amount!=0 and turn!=0:
##                        idd.append(oo[0])
##                        price_v.append(amount/volume)
##                        #high_low=(high-low)*2-abs(closee-openn)
##                        #volume_v.append(volume/high_low)
##                        #volume_v.append(amount/high_low)  #因为股票有送股，送股后股票变多，所以改为了用成交金额，这样更合理
##                        volume_v.append(turn/high_low)  #因为换手率是按流通股算的，所以按换手率比较科学。
##                        
##                elif n%b==1:
##                    openn=float(oo[2])
##                    low=float(oo[4])
##                    high=float(oo[3])
##                    closee=float(oo[5])
##                    amount=float(oo[8])
##                    volume=float(oo[7])
##                    if oo[10]=="":
##                        turn=0
##                    else:
##                        turn=float(oo[10])
##                    #high_low=(high-low)*2-abs(closee-openn)
##                    
##                else:
##                    if float(oo[4])!=0 and float(oo[4])<low:
##                        low=float(oo[4])
##                    if float(oo[3])>high:
##                        high=float(oo[3])
##                    closee=float(oo[5])
##                    amount+=float(oo[8])
##                    volume+=float(oo[7])
##                    if oo[10]=="":
##                        turn=0
##                    else:
##                        turn=float(oo[10])
##                    #high_low=(high-low)*2-abs(closee-openn)
##
##                n+=1


        #if len(price_v)<100 or price_v[-1]>100:
            #continue
        #else:
            #pass

        img = Image.open("000_1280.png")
        img = img.convert('RGBA')
        draw =ImageDraw.Draw(img)
        #draw =ImageDraw.Draw(img, mode="RGBA")

        draw.line((0, 308-30,1280,308-30), "#cccccc")
        draw.line((0, 308-60,1280,308-60), "#cccccc")
        draw.line((0, 308-90,1280,308-90), "#cccccc")
        draw.line((0, 308-120,1280,308-120), "#cccccc")
        draw.line((0, 308-150,1280,308-150), "#cccccc")
        draw.line((0, 308-180,1280,308-180), "#cccccc")
        draw.line((0, 308-210,1280,308-210), "#cccccc")
        draw.line((0, 308-240,1280,308-240), "#cccccc")
        draw.line((0, 308-270,1280,308-270), "#cccccc")
        draw.line((0, 308-300,1280,308-300), "#cccccc")
        #------------------------
        title_v=""
        #print("---------")
        #print(len(price_v))
        #print(len(price2_v))
        if (lenn:=len(price_v))>2:
            #maxx=max(price_v)
            #minn=min(price_v)

            ttt=[]
            for pp in price_v:
                if pp!=None:
                    ttt.append(pp)
            maxx1=max(ttt)
            minn1=min(ttt)

            ttt=[]
            for pp in price2_v:
                if pp!=None:
                    ttt.append(pp)
            maxx2=max(ttt)
            minn2=min(ttt)

            maxx=max([maxx1, maxx2])
            minn=min([minn1, minn2])

            HL=round(maxx/minn,3)
            #if price_v.index(minn)<5:  #===================
            if minn in price_v and price_v.index(minn)==0 and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3" and lenn>=200 and float(ooo[-1][5])<20 and HL>=4:  #===================
                #print(price_v)
                #print(lenn)
                #print(price_v.index(minn))
                title_v="_V"
            #price_v[price_v.index(maxx)]=minn  #------------
            #maxx=max(price_v)
        
            h_l_2=f"H/L: {round(maxx/minn,3)}"
            maxx_minn=maxx-minn
            i=0
            if lenn>1280:
                price_v=price_v[0:1280]
                price2_v=price2_v[0:1280]
                lenn=1280

            year=idd[-i-1][:4]  #取年份
            for pp in price_v[::-1]:
                if pp==None:
                    #draw.line((i, 308, i, 308), '#ffffff')
                    pass
                else:
                    draw.line((i, 308, i, 308-int(((pp-minn)/maxx_minn)*300)), 'black')
                
                if year!=idd[-i-1][:4]:
                #if i==lenn-50 or i==lenn-100:
                    if pp==None:
                        #draw.line((i, 308, i, 308), '#ffffff')
                        pass
                    else:
                        draw.line((i, 308-int(((pp-minn)/maxx_minn)*300),i,0), "#ff0000")
                    year=idd[-i-1][:4]
                i+=1
                
            i=0
            for pp in price2_v[::-1]:
                if pp==None:
                    #draw.line((i, 308, i, 308), '#ffffff')
                    pass
                else:
                    draw.line((i, 308, i, 308-int(((pp-minn)/maxx_minn)*300)), fill = (255, 204, 0, 255))
                    #draw.line((i, 308, i, 308-int(((pp-minn)/maxx_minn)*300)), "#0000ff")
                    #print("-------")

                i+=1
        #=========================

        #------------------------
        if (lenn:=len(volume_a))>2:
        #if (lenn:=len(volume_a))>99:
            ttt=[]
            for vv in volume_a:
                if vv!=None:
                    ttt.append(vv)
                    
            maxx=max(ttt)
            minn=min(ttt)
           
            maxx_minn=maxx-minn
            i=0
            
            if lenn>1280:
                volume_v=volume_v[0:1280]
                lenn=1280

            year=idd[-i-1][:4]  #取年份
            for vv in volume_a[::-1]:
                if vv==None:
                    pass
                else:
                    #draw.line((i, 312, i, 312+int(((vv-minn)/maxx_minn)*150)), '#3366ff')
                    draw.line((i, 312+200, i, 312+200+int(((vv)/maxx)*100)), '#3366ff')

                if year!=idd[-i-1][:4]:
                    if vv==None:
                        pass
                    else:
                        draw.line((i, 312+200+int(((vv-minn)/maxx_minn)*100),i,619), "#ff0000")
                    year=idd[-i-1][:4]
                    
                i+=1
        #=========================

        #------------------------
        title_a=""
        if (lenn:=len(volume_v))>2:
        #if (lenn:=len(volume_v))>99:
            ttt=[]
            for vv in volume_v:
                if vv!=None:
                    ttt.append(vv)
                    
            maxx=max(ttt)
            minn=min(ttt)
            #if volume_v.index(maxx)==0:  #===================
            if maxx in volume_v and volume_v.index(maxx)==0 and dd[0][:6]!="sh.688" and dd[0][:4]!="sz.3" and lenn>=200 and float(ooo[-1][5])<20 and HL>=4:  #===================
                title_a="_A"
                
            #amount_v[volume_v.index(maxx)]=minn  #-----------
            #maxx=max(volume_v)
            
            h_l_1=f"H/L: {round(maxx/minn,3)}"
            maxx_minn=maxx-minn
            i=0
            
            if lenn>1280:
                volume_v=volume_v[0:1280]
                lenn=1280

            year=idd[-i-1][:4]  #取年份
            for vv in volume_v[::-1]:
                #draw.line((i, 629, i, 629-int(((dd-minn)/maxx_minn)*300)), 'black')
                #draw.line((i, 329, i, 329+int(((dd-minn)/maxx_minn)*300)), 'black')
                if vv==None:
                    #draw.line((i, 312, i, 312), '#ffffff')
                    pass
                else:
                    draw.line((i, 312, i, 312+int(((vv-minn)/maxx_minn)*200)), 'black')
                    #draw.line((i, 312, i, 312+int(((vv-minn)/maxx_minn)*300)), fill = (0, 0, 0, 127))
                    pass

                if year!=idd[-i-1][:4]:
                #if i==lenn-50 or i==lenn-100:
                    if vv==None:
                        #draw.line((i, 312,i,619), "#ffffff")
                        pass
                    else:
                        draw.line((i, 312+int(((vv-minn)/maxx_minn)*200),i,619-100), "#ff0000")
                    year=idd[-i-1][:4]
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
            img.save(f"img_{a}2/{title_a}{title_v}{dd[0]}_{dd[1].replace('*','x')}（{classs}）_{b}{a}.png", "png")


print("--end--")
