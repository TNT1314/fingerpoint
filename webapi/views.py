#! usr/bin/env python
# encoding: utf-8
from django.shortcuts import render

# Create your views here.

import os
import copy
import json

from collections import OrderedDict
from django.conf import settings
from django.shortcuts import render
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder

from rest_framework.response import Response
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.decorators import api_view, renderer_classes


def finger_point_test_html_01(request):
    return render(request, 'fingerpoint.html')


@api_view(['GET', 'POST'])
def finger_point_test_api_01(request):
    """
        Finger image test

        参数:
            deviceid: 设备编号
            file: 文件
        返回:
            {
                "mesage": "失败！",
                "code": "10001",
                "data": {}
            }
    """

    rsp_data = dict()

    req_data = request.data if request.data else request.query_params

    if req_data:
        if 'deviceid' in req_data and req_data['deviceid'] == '110102006229':
            upload_path = os.path.join(u"{}/upload".format(settings.BASE_DIR))

            if not os.path.exists(upload_path):
                os.makedirs(upload_path)

            image_file = req_data['image'] if 'image' in req_data else None
            if image_file:
                # 打开特定的文件进行二进制的写操作
                destination = open(u"{}/{}".format(upload_path, image_file.name), 'wb+')
                for chunk in image_file.chunks():  # 分块写入文件
                    destination.write(chunk)
                destination.close()

            self_data = copy.deepcopy(req_data)
            del self_data['image']

            rsp_data['code'] = '10000'
            rsp_data['mesage'] = u'Upload Success.'
            rsp_data['chinese_test'] = u'中文测试'
            rsp_data['data'] = OrderedDict()
            rsp_data['data'] = self_data
            rsp_data['data']['file_url'] = u"/media/{}".format(image_file.name)

        else:

            rsp_data['code'] = '10001'
            rsp_data['mesage'] = 'Upload Fail.'
            rsp_data['chinese_test'] = u'中文测试'
            rsp_data['data'] = OrderedDict()
            rsp_data['data'] = copy.deepcopy(req_data)
    else:
        rsp_data['code'] = u'10001'
        rsp_data['mesage'] = 'Upload Error.diviceid error.'
        rsp_data['chinese_test'] = u'中文测试'
        rsp_data['data'] = OrderedDict()
        rsp_data['data'] = copy.deepcopy(req_data)

    return Response(rsp_data)


@api_view(['GET', 'POST'])
@renderer_classes((StaticHTMLRenderer,))
def finger_point_test_api_02(request):
    """
        Finger image test

        参数:
            deviceid: 设备编号
            file01: 文件
        返回:
            {
                "mesage": "失败！",
                "code": "10001",
                "data": {}
            }
    """

    rsp_data = OrderedDict()
    rsp_data['data'] = OrderedDict()
    req_data = request.data if request.data else request.query_params

    if req_data:
        if 'deviceid' in req_data:
            upload_path = os.path.join(u"{}/upload".format(settings.BASE_DIR))

            if not os.path.exists(upload_path):
                os.makedirs(upload_path)

            image_file = req_data['file'] if 'image' in req_data else None
            if image_file:
                # 打开特定的文件进行二进制的写操作
                destination = open(u"{}/{}".format(upload_path, image_file.name), 'wb+')
                for chunk in image_file.chunks():  # 分块写入文件
                    destination.write(chunk)
                destination.close()
                rsp_data['data']['file_url'] = u"/media/{}".format(image_file.name)

            rsp_data['code'] = '10000'
            rsp_data['mesage'] = 'Upload Success.'
            rsp_data['data']['request_data'] = dict()
            rsp_data['data']['request_data'] = copy.deepcopy(req_data)
            rsp_data['chinese_test'] = u'中文测试'
        else:
            rsp_data['code'] = '10001'
            rsp_data['mesage'] = 'Upload Fail.'
            rsp_data['data'] = copy.deepcopy(req_data)
            rsp_data['chinese_test'] = u'中文测试'
    else:
        rsp_data['code'] = '10001'
        rsp_data['mesage'] = 'Upload Error.diviceid error.'
        rsp_data['data'] = copy.deepcopy(req_data)
        rsp_data['chinese_test'] = u'中文测试'

    response_data = json.dumps(rsp_data, ensure_ascii=False, indent=2)

    return Response(response_data)


@api_view(['GET', 'POST'])
@renderer_classes((StaticHTMLRenderer,))
def finger_point_test_file_list(request):
    """
        Finger image test
    """

    rsp_data = OrderedDict()
    rsp_data['data'] = OrderedDict()

    upload_path = os.path.join(u"{}/upload".format(settings.BASE_DIR))

    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    upload_files = os.listdir(upload_path)

    upload_files_list = [
        u"""
            <div>
                <strong>{0}</strong>. <a href="/media/{1}">{1}</a><br/>
            </div>
        """.format((idex+1), filename) for idex, filename in enumerate(upload_files)]

    html_list = "".join(upload_files_list)
    html_text = u"""
        <div>
            <div>
                <h4>文件列表</h4>
                {}
            </div>
        </div>
    """.format(html_list)
    return Response(html_text)