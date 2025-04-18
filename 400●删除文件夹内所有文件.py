import os
import shutil


def del_file(filepath):
    """
    删除某一目录下的所有文件或文件夹
    :param filepath: 路径
    :return:
    """
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


del_file(f"img_d5_成交额\\")
del_file(f"img_d5_换手率\\")

#del_file(f"img_md5_0\\")

#del_file(f"img_md5_1\\")

print("--end--")
