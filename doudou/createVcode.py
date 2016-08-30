# -*- coding:utf-8 -*-
# 验证码生成模块

import random, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import hashlib
import datetime

chars = ''.join((hashlib.md5(str(datetime.datetime.now()) + str(random.random())).hexdigest()))

def create_valicode(size=(200,60), chars=chars, mode='RGB', bg_color=(255,255,255),
                    fg_color=(255,0,0), font_size=36,length=5,draw_points=True,
                    draw_lines=True,point_chance=2):
    """
    >>>>>>>>>>>>> 验证码相关配置 <<<<<<<<<<<<<
    size: 图片的大小，格式（宽，高），默认为(120, 30)
    chars: 允许的字符集合，格式字符串
    mode: 图片模式，默认为RGB
    bg_color: 背景颜色，默认为白色
    fg_color: 前景色，验证码字符颜色
    font_size: 验证码字体大小
    font_type: 验证码字体，默认为 Monaco.ttf
    length: 验证码字符个数
    draw_points: 是否画干扰点
    draw_lines: 是否画干扰线
    point_chance: 干扰点出现的概率，大小范围[0, 50]
    """
    width, height = size

    #创建画布
    img = Image.new(mode, size, bg_color)

    #创建画笔
    draw = ImageDraw.Draw(img)

    #生成随机颜色
    def create_color():
        return (random.randint(0,255),
        random.randint(0,255),
        random.randint(0,255))

    def get_chars():
        #生成指定长度验证码字符串,返回列表格式
        return random.sample(chars, length)

    def create_points():
        #绘制干扰噪点
        chance = min(30, max(0, int(point_chance)))

        for w in xrange(width):
            for h in xrange(height):
                tmp = random.randint(0,30)
                if tmp > 30 - chance:
                    draw.point((w, h), fill=create_color())

    def create_lines():
        #绘制干扰线
        lines_color = create_color()

        for i in range(0, 8):
            x1 = random.randint(0, width)
            x2 = random.randint(0, width)
            y1 = random.randint(0, height)
            y2 = random.randint(0, height)
            draw.line([(x1, y1), (x2, y2)], lines_color)

    def create_chars():
        #绘制验证码字符
        c_chars = get_chars()
        strs = '%s' % ''.join(c_chars)

        basedir = os.path.dirname(os.path.dirname(__file__))
        #print basedir
        s_font = os.path.join(basedir, 'doudou/apps/static/DroidSans.ttf')
        font = ImageFont.truetype(s_font, font_size)
        font_width, font_height= font.getsize(strs)
        start = 13
        for i in range(len(strs)):
            x = start + (width - font_width) / 3 * i
            y = (height - font_height) / 3
            draw.text((x, y),strs[i], font=font, fill=create_color())

        return strs

    if draw_points:
        create_points()

    if draw_lines:
        create_lines()

    strs = create_chars()

    #创建虑镜,边界加强
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    return img, strs

