import baostock as bs
import pandas as pd

import json
import datetime
import os
import time

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


with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

a="d"
for dd in ddd:
    #print(dd[0])
    if dd[0][:3]!="of.":
    #if dd[0][:3]=="sh.":
        print(dd[0])
        #time.sleep(0.1)
        if os.path.exists(f'data/K_line_d_后复权/{dd[0]}_{a}.txt'):
            with open(f'data/K_line_d_后复权/{dd[0]}_{a}.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
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
        rs = bs.query_history_k_data_plus(dd[0],
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,psTTM,pcfNcfTTM,pbMRQ,isST",
            start_date=t_str, end_date='2099-12-31',
            frequency=a, adjustflag="1")

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

        with open(f'data/K_line_d_后复权/{dd[0]}_{a}.txt', 'w', encoding='utf-8', newline='\r\n') as f:
            #f.write(json.dumps(data_list, indent=4, ensure_ascii=False)+"\r\n")
            f.write(json.dumps(ooo, indent=0, ensure_ascii=False)+"\r\n")
            
        #result = pd.DataFrame(data_list, columns=rs.fields)

        #### 结果集输出到csv文件 ####   
        #result.to_csv("D:\\history_A_stock_k_data.csv", index=False)
        #result.to_csv("sh_6005190.csv", index=True)
        #print(result)

#### 登出系统 ####
bs.logout()
