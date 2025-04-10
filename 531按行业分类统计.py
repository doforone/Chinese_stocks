#  白点数据，运行环境python3.8

import json


with open('data/行业分类.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

"""
    [
        "2022-08-01",
        "sh.603355",
        "莱克电气",
        "家用电器",
        "申万一级行业"
    ]
"""

rrr={}
for dd in ddd:
    if dd[3] in rrr.keys():
        rrr[dd[3]]+=1
    else:
        rrr[dd[3]]=1

rrr2=sorted(rrr.items(),key=lambda kv: kv[1], reverse=True)
#print(rrr2)

for rr2 in rrr2:
    print(f"{rr2[0].rjust(4,'　')}：{rr2[1]}支")


print("--end--")
