import json
from PIL import Image, ImageDraw,ImageFont
import datetime
import os
import shutil
import random


aaa=[]
filepath=f"img_d2\\"
#filepath=f"img_md5_1\\"
filepath=f"img_指定日期前\\"

fff = os.listdir(filepath)
for ff in fff:
    file_path = os.path.join(filepath, ff)
    if os.path.isfile(file_path):
        #os.remove(file_path)
        aaa.append(ff)
    elif os.path.isdir(file_path):
        #shutil.rmtree(file_path)
        pass

bbb=random.sample(aaa,8)
print(bbb)

img = Image.new("RGBA",(1440,1440),(255,255,255))

img2 = Image.open(f"{filepath}{bbb[0]}")
img2=img2.resize((640, 310))
img.paste(img2, (53, 40))

img2 = Image.open(f"{filepath}{bbb[1]}")
img2=img2.resize((640, 310))
img.paste(img2, (747, 40))

img2 = Image.open(f"{filepath}{bbb[2]}")
img2=img2.resize((640, 310))
img.paste(img2, (53, 390))

img2 = Image.open(f"{filepath}{bbb[3]}")
img2=img2.resize((640, 310))
img.paste(img2, (747, 390))

img2 = Image.open(f"{filepath}{bbb[4]}")
img2=img2.resize((640, 310))
img.paste(img2, (53, 740))

img2 = Image.open(f"{filepath}{bbb[5]}")
img2=img2.resize((640, 310))
img.paste(img2, (747, 740))

img2 = Image.open(f"{filepath}{bbb[6]}")
img2=img2.resize((640, 310))
img.paste(img2, (53, 1090))

img2 = Image.open(f"{filepath}{bbb[7]}")
img2=img2.resize((640, 310))
img.paste(img2, (747, 1090))

setFont = ImageFont.truetype('fonts/msyh.ttf', 30)
fillColor = "#cc0000"
draw =ImageDraw.Draw(img)

text_size = setFont.getsize(f"{bbb[0][:-4]}")
draw.text((53+(640-text_size[0])/2, 40+310+0), f"{bbb[0][:-4]}", \
          font=setFont, fill=fillColor)

text_size = setFont.getsize(f"{bbb[1][:-4]}")
draw.text((747+(640-text_size[0])/2, 40+310+0), f"{bbb[1][:-4]}", \
          font=setFont, fill=fillColor)

text_size = setFont.getsize(f"{bbb[2][:-4]}")
draw.text((53+(640-text_size[0])/2, 390+310+0), f"{bbb[2][:-4]}", \
          font=setFont, fill=fillColor)

text_size = setFont.getsize(f"{bbb[3][:-4]}")
draw.text((747+(640-text_size[0])/2, 390+310+0), f"{bbb[3][:-4]}", \
          font=setFont, fill=fillColor)

text_size = setFont.getsize(f"{bbb[4][:-4]}")
draw.text((53+(640-text_size[0])/2, 740+310+0), f"{bbb[4][:-4]}", \
          font=setFont, fill=fillColor)

text_size = setFont.getsize(f"{bbb[5][:-4]}")
draw.text((747+(640-text_size[0])/2, 740+310+0), f"{bbb[5][:-4]}", \
          font=setFont, fill=fillColor)

text_size = setFont.getsize(f"{bbb[6][:-4]}")
draw.text((53+(640-text_size[0])/2, 1090+310+0), f"{bbb[6][:-4]}", \
          font=setFont, fill=fillColor)

text_size = setFont.getsize(f"{bbb[7][:-4]}")
draw.text((747+(640-text_size[0])/2, 1090+310+0), f"{bbb[7][:-4]}", \
          font=setFont, fill=fillColor)

##img2 = Image.open(f"{filepath}{bb}")
####img2=img2.convert('RGB')
####w, h = img2.size
##img2=img2.resize((640, 310))
##img.paste(img2, (0, 0))
###img.paste((0,0,0),(10,20,300,400))
###img.show()

img.save(f"000\\{random.randint(100000,999999)}.png", "png")

print("--end--")

##x=""
##while x!="x":
##    x=input("请输入x退出：")
