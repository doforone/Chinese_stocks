import baostock as bs
import pandas as pd

import json
import datetime
import os
import time

with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

a="5"
for dd in ddd:
    #print(dd[0])
    #if dd[0][:3]!="of.":
    if dd[0]=="sz.002809":
        print(dd[0])
        #time.sleep(0.1)
        if os.path.exists(f'data/k_line_5/{dd[0]}_{a}.txt'):
            with open(f'data/k_line_5/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ooo=json.loads(f.read())
            if ooo==[]:
                t_str="1900-01-01"
            else:
                t_str=(datetime.datetime.strptime(ooo[-1][0],'%Y-%m-%d')+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            ooo=[]
            t_str="1900-01-01"
        
        #### 获取沪深A股历史K线数据 ####
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg

        #日线
##        if t_str==time.strftime("%Y-%m-%d", time.localtime(time.time()+3600*24)):
##            print("---已下载---")
##            continue
        rs = bs.query_history_k_data_plus(dd[0],
            "date,time,code,open,high,low,close,volume,amount,adjustflag",
            start_date=t_str, end_date='2099-12-31',
            frequency=a, adjustflag="3")

    ##    #周线
    ##    rs = bs.query_history_k_data_plus(dd[0],
    ##        "date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg",
    ##        start_date='1900-01-01', end_date='2099-12-31',
    ##        frequency=a, adjustflag="3")
        
        print('query_history_k_data_plus respond error_code:'+rs.error_code)
        print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

        #### 打印结果集 ####
        #data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            #data_list.append(rs.get_row_data())
            ooo.append(rs.get_row_data())

        with open(f'data/k_line_5/{dd[0]}_{a}.txt', 'w', encoding='utf-8', newline='\r\n') as f:
            #f.write(json.dumps(data_list, indent=4, ensure_ascii=False)+"\r\n")
            f.write(json.dumps(ooo, indent=0, ensure_ascii=False)+"\r\n")
            
        #result = pd.DataFrame(data_list, columns=rs.fields)

        #### 结果集输出到csv文件 ####   
        #result.to_csv("D:\\history_A_stock_k_data.csv", index=False)
        #result.to_csv("sh_6005190.csv", index=True)
        #print(result)

#### 登出系统 ####
bs.logout()
