# 白点数据，运行环境Python3.8
# -*- coding: UTF-8 -*-

import json
from PIL import Image, ImageDraw,ImageFont


with open('data/行业分类.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

rrr={}
for dd in ddd:
    if dd[3] in rrr.keys():
        rrr[dd[3]]+=1
    else:
        rrr[dd[3]]=1

sss=sorted(rrr.items(),key=lambda kv: kv[1], reverse=True)
for ss in sss:
    print(f"{ss[0]}：{ss[1]}")

print("--end--")
