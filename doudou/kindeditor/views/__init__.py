# -*- coding:utf-8 -*-
# __author__ = 'Wells Jia'
# KindEditor视图

from doudou.kindeditor import kindedit

from flask.ext.login import login_required

from flask import request, url_for, jsonify, make_response

from werkzeug.utils import secure_filename

from datetime import datetime

from hashlib import md5

import json, time

import os, re

# KindEditor文件存储空间path
fileSpacePath = os.path.join(kindedit.root_path, 'uploadFile')

if not os.path.exists(fileSpacePath) and not os.path.isdir(fileSpacePath):
    os.makedirs(fileSpacePath)

# 图片扩展名
imageExt = ['gif', 'jpg', 'jpeg', 'png', 'bmp']

# 目录名称
Pathname = ['', 'image', 'flash', 'media', 'file']


# 定义允许上传的文件扩展名
extArray = dict(image=['gif', 'jpg', 'jpeg', 'png', 'bmp'], flash=['swf', 'flv'], \
                media=['swf', 'flv', 'mp3', 'wav', 'wma', 'wmv', 'mid', 'avi', 'mpg', 'asf', 'rm', 'rmvb'], \
                file=['doc', 'docx', 'xls', 'xlsx', 'ppt', 'htm', 'html', 'txt', 'zip', 'rar', 'gz', 'bz2'])


# 定义上传文件最大尺寸(默认5M) 暂时不可用
# max_size = 5242880

# 定义上传文件保存路径
save_path_base = os.path.abspath(fileSpacePath) + '/'


# 自定义比较函数
def cmp_func(a, b, order):
    if a['is_dir'] and not b['is_dir']:
        return -1
    elif not a['is_dir'] and b['is_dir']:
        return 1
    else:
        if order == 'size':
            if a['filesize'] > b['filesize']:
                return 1
            elif a['filesize'] < b['filesize']:
                return -1
            else:
                return 0
        elif order == 'type':
            return cmp(a['filetype'], b['filetype'])
        else:
            return cmp(a['filename'], b['filename'])


# 自定义返回函数
def alert(msg):
    result = dict(error=1, message=msg)

    res = make_response(json.dumps(result))
    res.headers['Content-Type'] = 'text/html'

    return res


@kindedit.route('/fileManagerJson')
@login_required
def kindSpace():
    # 获取目录名
    dir_name = request.args.get('dir', None).strip()

    if dir_name not in Pathname:
        return alert(u'目录参数错误')

    if dir_name:

        # 生成dir_name目录路径
        root_path = os.path.join(fileSpacePath, dir_name)

        # 生成dir_name Url
        root_url = ''.join(url_for('kindedit.static', filename=dir_name) + '/')

        if not os.path.exists(root_path) and not os.path.isdir(root_path):
            os.makedirs(root_path)
    else:
        root_path = fileSpacePath
        root_url = ''.join(url_for('kindedit.static'))

    if not request.args['path']:
        # current_path 当前请求的路径
        current_path = ''.join(root_path + '/')

        # current_url 当前请求路径的Url
        current_url = root_url

        # 当前请求的目录名称
        current_dir_path = ''

        # 上一级目录名称
        moveup_dir_path = ''
    else:
        # current_path 当前请求的路径
        current_path = ''.join(root_path + '/' + request.args['path'])

        # current_url 当前请求路径的Url
        current_url = ''.join(root_url + request.args['path'])

        # 当前请求的目录名称
        current_dir_path = request.args['path']

        # 上一级目录名称
        moveup_dir_path = '/'.join(current_dir_path.split('/')[:-2]) + '/' if current_dir_path.split('/')[:-2] else ''

    regex = re.compile(r'.*?(/$)')
    # regex = re.compile(r'/\/$/') 注：测试js插件报错提示

    # 判断当前文件路径是否以/结尾
    if not regex.match(current_path):
        return alert('Parameter is not valid.')

    # 判断当前文件路径中是否存在..
    regex = re.compile(r'.\.\.')
    if regex.match(current_path):
        return alert('Access is not allowed.')

    if not os.path.exists(current_path) and not os.path.isdir(current_path):
        return 'Directory does not exist.'

    file_list = []

    # 获取current_path中的文件
    fileLists = os.listdir(current_path)

    if fileLists:
        i = 0
        while i <= (len(fileLists) - 1):
            if fileLists[i] == '.':
                continue

            Ifile = current_path + fileLists[i]

            if os.path.isdir(Ifile):
                tmp = dict(is_dir=True, \
                           has_file=(len(os.listdir(Ifile)) > 0), \
                           filesize=0, \
                           is_photo=False, \
                           filetype='', \
                           filename=fileLists[i],
                           datetime=datetime.fromtimestamp(os.path.getmtime(Ifile)).strftime('%Y-%m-%d %H:%M:%S'))
                file_list.append(tmp)
            else:
                file_ext = (lambda x: x[x.rfind('.'):][1:].lower())(Ifile)
                tmp = dict(is_dir=False, \
                           has_file=False, \
                           filesize=os.path.getsize(Ifile), \
                           dir_path='', \
                           is_photo=file_ext in imageExt, \
                           filetype=file_ext, \
                           filename=fileLists[i],
                           datetime=datetime.fromtimestamp(os.path.getmtime(Ifile)).strftime('%Y-%m-%d %H:%M:%S'))
                file_list.append(tmp)

            i += 1

    # 排序形式
    order = request.args.get('order', 'name').lower()

    # 对文件列表进行排序
    file_list = sorted(file_list, cmp=lambda a, b: cmp_func(a, b, order))


    # 构造返回数据
    result = {}
    result['moveup_dir_path'] = moveup_dir_path
    result['current_dir_path'] = current_dir_path
    result['current_url'] = current_url
    result['total_count'] = len(file_list)
    result['file_list'] = file_list

    return jsonify(result)


@kindedit.route('uploadJson', methods=['POST'])
@login_required
def upload_json():
    # 判断文件上传
    if request.files:
        upFile = request.files['imgFile']
        # 原文件名
        file_name = secure_filename(upFile.filename)

        # 文件后缀
        fileExt = (lambda x: x[x.rfind('.'):][1:].lower())(file_name)

        if not file_name:
            return alert(u'请选择文件')

        if not os.path.exists(save_path_base) and not os.path.isdir(save_path_base):
            return alert(u'上传目录不存在')

        dir_name = request.args.get('dir', 'image').strip()

        if not extArray.has_key(dir_name):
            return alert(u'目录名不正确')

        if fileExt not in extArray[dir_name]:
            return alert(u'上传文件格式不允许')

        if dir_name:
            save_path = os.path.join(save_path_base, dir_name) + '/'
            save_url = url_for('kindedit.static', filename=dir_name) + '/'

            if not os.path.exists(save_path) and not os.path.isdir(save_path):
                os.makedirs(save_path)

        ymd = datetime.today().strftime('%Y%m%d')

        save_path += (ymd + '/')
        save_url += (ymd + '/')

        if not os.path.exists(save_path) and not os.path.isdir(save_path):
            os.makedirs(save_path)

        # 构造保存的文件名
        filename = md5(file_name + str(int(time.time()))).hexdigest() + '.' + fileExt

        # 保存文件
        try:
            upFile.save(save_path + filename)
        except Exception, e:
            return alert(u'上传文件失败')

        file_url = save_url + filename

        result = dict(error=0, url=file_url)

        res = make_response(json.dumps(result))
        res.headers['Content-Type'] = 'text/html'

        return res
    else:
        return alert(u'请选择文件')