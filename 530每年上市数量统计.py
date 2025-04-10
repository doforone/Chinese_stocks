#  白点数据，运行环境python3.8

import json


with open('data/sh_sz.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

"""
[
    "sz.000950",
    "重药控股",
    "1999-09-16",
    "",
    "1",
    "1"
]
"""

rrr={}
for dd in ddd:
    if (a:=dd[2][:4]) in rrr.keys():
        rrr[a]+=1
    else:
        rrr[a]=1

rrr2=sorted(rrr.items(),key=lambda kv: kv[0], reverse=False)
#print(rrr2)

for rr2 in rrr2:
    print(f"{rr2[0]}年：{rr2[1]}支")

print("--end--")
