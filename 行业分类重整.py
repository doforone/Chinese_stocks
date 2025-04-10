import baostock as bs
import pandas as pd

import json
from PIL import Image, ImageDraw,ImageFont


with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())
    
with open('data/行业分类.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd2=json.loads(f.read())

rrr={}
for dd in ddd2:
    #if dd[3]!="":
        rrr[dd[1]]=dd[3]

for dd in ddd:
    if dd[0][:3]!="of." and dd[4]=="1" and dd[5]=="1":
        if dd[0] not in rrr.keys():
            rrr[dd[0]]=""
        
with open(f'data/行业分类2.txt', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(json.dumps(rrr, indent=4, ensure_ascii=False)+"\r\n")
