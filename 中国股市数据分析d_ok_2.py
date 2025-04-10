import baostock as bs
import pandas as pd

import json
from PIL import Image, ImageDraw,ImageFont

with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

with open('data/行业分类2.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd2=json.loads(f.read())

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

a="d"
for dd in ddd:
    if dd[4]=="1" and dd[5]=="1" and dd[3]=="":
        print(dd)
    else:
        continue
    
    #### 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg

    rs = bs.query_history_k_data_plus(dd[0],
        "date,code,open,high,low,close,volume,amount",
        start_date='1900-01-01', end_date='2099-12-31',
        frequency=a, adjustflag="3")
    
    print('query_history_k_data_plus respond error_code:'+rs.error_code)
    print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

    volume_v=[]
    price_v=[]

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        d=rs.get_row_data()
        if d[2]!="" and d[3]!="" and d[4]!="" and d[5]!="" and d[6]!="" and d[7]!="":
            idd=d[0]
            openn=float(d[2])
            high=float(d[3])
            low=float(d[4])
            closee=float(d[5])
            
            if d[6]=="":
                volume=0
            else:
                volume=float(d[6])

            if d[7]=="":
                amount=0
            else:
                amount=float(d[7])

            high_low=(high-low)*2-abs(closee-openn)
            if high_low!=0 and volume!=0 and amount!=0:
                volume_v.append(volume/high_low)
                price_v.append(amount/volume)

                # 获取一条记录，将记录合并在一起
                #data_list.append(rs.get_row_data())
                data_list.append(d)

##    with open(f'data/k_line/{dd[0]}_{a}.txt', 'w', encoding='utf-8', newline='\r\n') as f:
##        f.write(json.dumps(data_list, indent=4, ensure_ascii=False)+"\r\n")
        
    #result = pd.DataFrame(data_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####   
    #result.to_csv("D:\\history_A_stock_k_data.csv", index=False)
    #result.to_csv("sh_6005190.csv", index=True)
    #print(result)

    if len(price_v)<100 or price_v[-1]>100:
        continue
    else:
        pass

    img = Image.open("111.png")
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
    #if (lenn:=len(volume_v))>2:
    if (lenn:=len(volume_v))>99:
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
        for vv in volume_v:
            #draw.line((i, 629, i, 629-int(((dd-minn)/maxx_minn)*300)), 'black')
            #draw.line((i, 329, i, 329+int(((dd-minn)/maxx_minn)*300)), 'black')
            draw.line((i, 312, i, 312+int(((vv-minn)/maxx_minn)*300)), 'black')
            i+=1
            if i==lenn-50 or i==lenn-100:
                draw.line((i, 312+int(((vv-minn)/maxx_minn)*300),i,619), "#ff0000")
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
        for pp in price_v:
            draw.line((i, 308, i, 308-int(((pp-minn)/maxx_minn)*300)), 'black')
            i+=1
            if i==lenn-50 or i==lenn-100:
                draw.line((i, 308-int(((pp-minn)/maxx_minn)*300),i,0), "#ff0000")
    #=========================

    #=========================
    if len(price_v)>2:
        setFont = ImageFont.truetype('fonts/msyh.ttf', 16)
        fillColor = "#000000"
        width, height = img.size
        #ttt1=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ddd[0][0]/1000))
        ttt1=data_list[0][0]
        ttt2=data_list[-1][0]

        if dd[0] in ddd2.keys():
            classs=ddd2[dd[0]]
        else:
            classs=""
            
        text_size = setFont.getsize(f"{dd[0]} {dd[1]}（{classs}）_{a} ({ttt1}, {ttt2}) ({h_l_2}) {data_list[-1][5]}")
        text_size2 = setFont.getsize(f"({h_l_1})")
        #print(text_size)
        draw.text(((width-text_size[0])/2, 0), f"{dd[0]} {dd[1]}（{classs}）_{a} ({ttt1}, {ttt2}) ({h_l_2}) {data_list[-1][5]}", font=setFont, fill=fillColor)
        draw.text(((width-text_size2[0])/2, height-20), f"({h_l_1})", font=setFont, fill=fillColor)
        
        #Image1.show()
        img.save(f"img_3/{dd[0]}_{a}.png", "png")

                
#### 登出系统 ####
bs.logout()
