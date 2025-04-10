import baostock as bs
import pandas as pd

import json

# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

# 获取证券基本资料
#rs = bs.query_stock_basic(code="sh.600000")
rs = bs.query_stock_basic(code_name="")  # 支持模糊查询
print('query_stock_basic respond error_code:'+rs.error_code)
print('query_stock_basic respond  error_msg:'+rs.error_msg)

# 打印结果集
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())

with open('data/sh_sz.txt', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(json.dumps(data_list, indent=4, ensure_ascii=False)+"\r\n")

#result = pd.DataFrame(data_list, columns=rs.fields)

# 结果集输出到csv文件
#result.to_csv("D:/stock_basic.csv", encoding="gbk", index=False)
#print(result)

# 登出系统
bs.logout()
