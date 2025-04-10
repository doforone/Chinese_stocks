##
##import baostock as bs
##import pandas as pd
##
##import time
##import json
##from PIL import Image, ImageDraw,ImageFont
##
##print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
##
##ttt=time.strftime("%Y-%m-%d", time.localtime(time.time()))
##print(ttt)


import json
from PIL import Image, ImageDraw,ImageFont
import datetime
import os
import shutil
import random


aaa=[]
filepath=f"img_d2\\"
#filepath=f"img_md5_1\\"
filepath=f"img_d5_成交额\\"

fff = os.listdir(filepath)
for ff in fff:
    file_path = os.path.join(filepath, ff)
    if os.path.isfile(file_path):
        #os.remove(file_path)
        aaa.append(ff)
    elif os.path.isdir(file_path):
        #shutil.rmtree(file_path)
        pass

bbb=random.sample(aaa,20)
for bb in bbb:
    print(bb)
