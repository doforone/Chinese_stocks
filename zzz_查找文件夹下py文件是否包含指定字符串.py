##import os
##
##def search_files(rootdir, search_str):
##    for dirpath, dirnames, filenames in os.walk(rootdir):
##        for filename in filenames:
##            #print(filename)
##            if filename.endswith('.py') and filename.find("$")==-1:
##                filepath = os.path.join(dirpath, filename)
##                with open(filepath, 'r', encoding='utf-8') as f:
##                    content = f.read()
##                    if search_str in content:
##                        print(f'{filepath} 包含指定字符串：{search_str}')
##
### 指定要查找的文件夹路径和要查找的字符串
##rootdir = '/'
##search_str = 'all_A_V_D7.txt'
##
##search_files(rootdir, search_str)



import os

def search_files(rootdir, search_str):
    for filename in os.listdir(rootdir):
        if filename.endswith('.py') and filename.find("$")==-1:
            filepath = os.path.join(rootdir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                if search_str in content:
                    print(f'{filepath} 包含指定字符串：{search_str}')

# 指定要查找的文件夹路径和要查找的字符串
rootdir = '.'
search_str = 'all_A_V_D7.txt'

search_files(rootdir, search_str)

