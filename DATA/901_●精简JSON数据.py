# 白点数据，运行环境Python3.8
# -*- coding: UTF-8 -*-

from urllib import request, parse
from urllib.parse import quote
import urllib.parse

import json
import datetime
import os
import time
import base64
import hashlib
import random

import datetime
from datetime import timedelta
#from datetime import datetime, timezone

#============================时间到强制结束线程
import threading
import inspect
import ctypes

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
 
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

#=============================

def get_htmll(urll, p=0, dataa=None):     #请求页面，这个函数要用线程，长时间不响应就杀死线程，参数5秒有时不起作用
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
    try:
        req = request.Request(urll, headers=headers)
        with request.urlopen(req, timeout=6) as resp:  # ================
            #htmll=resp.read().decode("GBK","ignore")
            htmll=resp.read().decode("utf-8","replace")
            #with open('aaa.txt', 'a', encoding='utf-8', newline='\r\n') as f:
                #f.write(htmll)
            return htmll
    except Exception as e:
        print(e)
        htmll=""
        with open(f'err.txt', 'a', encoding='utf-8', newline='\r\n') as f:
            f.write(str(p)+"\r\n")
        return htmll


def get_htmll2(urll, p, dataa=None):     #请求页面，这个函数要用线程，长时间不响应就杀死线程，参数5秒有时不起作用
    #headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Mobile Safari/537.36'}
    
    #data={"areaSn":"","entType":"02","entName":"","pageIndex":p}
    #data={"jjrSel":"","p":p}
    data=dataa
    data=urllib.parse.urlencode(data,encoding='utf-8')
    data=bytes(data,'utf-8')
    
    try:
        #req = request.Request(urll, headers=headers)
        req = request.Request(urll, headers=headers, data=data, method="POST")
        with request.urlopen(req, timeout=6) as resp:  # ===================
            #htmll=resp.read().decode("GBK","ignore")
            htmll=resp.read().decode("utf-8","replace")
            #with open('aaa.txt', 'a', encoding='utf-8', newline='\r\n') as f:
                #f.write(htmll)
            return htmll
    except Exception as e:
        print(e)
        htmll=""
        with open(f'err.txt', 'a', encoding='utf-8', newline='\r\n') as f:
            f.write(str(p)+"\r\n")
        return htmll


f0=lambda x: 0.0 if x=="" else float(x)


def tt_d(x):  # 时间戳转日期
    timestamp = x  # 假设这是一个时间戳
    # 使用 fromtimestamp() 方法将时间戳转换为日期时间对象
    #date_time = datetime.datetime.fromtimestamp(timestamp)
    date_time = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
    #date_time = datetime.datetime.fromtimestamp(timestamp, tz=pytz.timezone('Asia/Shanghai'))
    # 然后可以使用 strftime() 方法将日期时间格式化为特定的日期字符串
    #formatted_date = date_time.strftime('%Y-%m-%d %H:%M:%S')
    formatted_date = date_time.strftime('%Y-%m-%d')
    return formatted_date  # 输出格式化后的日期字符串


folder_path = "K_line_d\\"

file_names = os.listdir(folder_path)
#file_names.sort(reverse=True)
#random.shuffle(file_names)
##file_names=[v for v in file_names if ((ex:=v.split(".")[-1])=="html" or ex=="py")]
##file_names.sort()
##ddd_vip={fun.md5(v)[:16]:v for v in file_names}


#### 日K线参数名称及定义 ####
##"2023-07-27,1836.00,1838.03,1854.79,1828.70,20340,3749635290.00,1.43,0.52,9.48,0.16"
##茅台日期         开盘        收盘         最高        最低        成交量（手）成交额（元）振幅% 涨跌幅% 涨跌额 流通换手率
##   0              1           2            3          4            5           6           7    8      9     10
## 振幅%=（最高-最低）/昨收；涨跌幅%=（收盘-昨收）/昨收；涨跌额=收盘-昨收
## 不复权的涨跌幅也是计算的不复权的


# 0日期  1开盘  2最低  3最高  4收盘  5涨跌额  6涨跌幅  7成交量  8成交额  9换手率

for ff in file_names:
    print(ff)
    with open(f'{folder_path}{ff}', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ddd=json.loads(f.read())
        
    with open(f'K_line_d\\{ff}', 'w', encoding='utf-8', newline='\r\n') as f:  # ======= 不复权,后复权,前复权
        #f.write(json.dumps(ddd2, indent=4, ensure_ascii=False)+"\r\n")
        #f.write(json.dumps(ddd2, ensure_ascii=False))
        f.write(json.dumps(ddd, indent=0, ensure_ascii=False)+"\r\n")


print("--end--")
