from PIL import Image, ImageDraw, ImageFont

def create_image_with_wrapped_text(text, font_path='fonts/msyh.ttf', image_size=(1080, 1080), output_path='991_文字自动排版以适应图片.png'):
    # 计算文字
    #print(text.encode())
    row_spacing=1.6  # 行间距
    img_width_scale=.84  # 一行文字占用的图片宽度是总宽度的比例
    if text.find("\n")==-1:
        column=(row_spacing*len(text))**(1/2)  # 计算一列有多少个字,利用面积开方
        if column.is_integer()==False:
            column+=1
        column=int(column)
        font_size=int((1080*img_width_scale)/column)
        text="\n".join([text[i:i+column] for i in range(0, len(text), column)])
    else:
        ddd=text.split("\n")
        ddd2=[len(dd) for dd in ddd]
        maxx=max(ddd2)
        if maxx>22 or len(ddd)>13:
            print("行字数超过22个字,或行数超过13行")
            print("结束!!!")
            return
        else:
            if maxx>len(ddd)*row_spacing:
                font_size=int((1080*img_width_scale)/maxx)
            else:
                font_size=int((1080*img_width_scale)/(len(ddd)*row_spacing))
    
    # 创建一个空白图片
    img = Image.new('RGB', image_size, color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # 字体大小设定
    #font_size = w_size
    font = ImageFont.truetype(font_path, font_size)
    
    # 绘制多行文本
    draw.multiline_text(
        xy=(50, int(font_size*(row_spacing-1))),                # 文本位置
        text=text,                  # 要绘制的文本
        fill=(33, 33, 33),             # 文本颜色
        font=font,                  # 字体和大小
        spacing=int(font_size*(row_spacing-1)),                 # 行间距
        align="left"                # 左对齐
    )
    
    # 保存图片
    img.save(output_path)
    #img.show()
    print("输出成功")


# 调用函数
#text="""现代经济不同于古代经济，现代经济由科学技术推动，是一个增量游戏，不是存量与零和游戏。"""

print("请输入文字，以生成图片：")
text=input()

create_image_with_wrapped_text(text, 'fonts/msyhbd.ttc')

