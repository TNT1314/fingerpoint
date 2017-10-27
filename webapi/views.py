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
    rsp_data['data'] = OrderedDict()
    req_data = request.data if request.data else request.query_params

    if req_data:
        if 'deviceid' in req_data and req_data['deviceid'] == '110102006229':
            upload_path = os.path.join(u"{}/upload".format(settings.BASE_DIR))

            if not os.path.exists(upload_path):
                os.makedirs(upload_path)

            image_file = req_data['file']
            if image_file:
                # 打开特定的文件进行二进制的写操作
                destination = open(u"{}/{}".format(upload_path, image_file.name), 'wb+')
                for chunk in image_file.chunks():  # 分块写入文件
                    destination.write(chunk)
                destination.close()
                rsp_data['data']['file_url'] = u"/media/{}".format(image_file.name)

            rsp_data['code'] = '10000'
            rsp_data['mesage'] = u'Upload Success.'
            rsp_data['data'] = rsp_data
            rsp_data['chinese_test'] = u'中文测试'
        else:
            rsp_data['code'] = '10001'
            rsp_data['mesage'] = 'Upload Fail.'
            rsp_data['data'] = copy.deepcopy(req_data)
            rsp_data['chinese_test'] = u'中文测试'
    else:
        rsp_data['code'] = u'10001'
        rsp_data['mesage'] = 'Upload Error.diviceid error.'
        rsp_data['data'] = copy.deepcopy(req_data)
        rsp_data['chinese_test'] = u'中文测试'
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
        if req_data['deviceid'] == '110102006229':
            upload_path = os.path.join(u"{}/upload".format(settings.BASE_DIR))

            if not os.path.exists(upload_path):
                os.makedirs(upload_path)

            image_file = req_data['file']
            if image_file:
                # 打开特定的文件进行二进制的写操作
                destination = open(u"{}/{}".format(upload_path, image_file.name), 'wb+')
                for chunk in image_file.chunks():  # 分块写入文件
                    destination.write(chunk)
                destination.close()
                rsp_data['data']['file_url'] = u"/media/{}".format(image_file.name)

            rsp_data['code'] = '10000'
            rsp_data['mesage'] = 'Upload Success.'
            rsp_data['data'] = rsp_data
            rsp_data['chinese_test'] = '中文测试'
        else:
            rsp_data['code'] = '10001'
            rsp_data['mesage'] = 'Upload Fail.'
            rsp_data['data'] = copy.deepcopy(req_data)
            rsp_data['chinese_test'] = '中文测试'
    else:
        rsp_data['code'] = '10001'
        rsp_data['mesage'] = 'Upload Error.diviceid error.'
        rsp_data['data'] = copy.deepcopy(req_data)
        rsp_data['chinese_test'] = '中文测试'

    response_data = json.dumps(rsp_data, ensure_ascii=False, indent=2)

    back_body = """
        <!DOCTYPE html>
        <html lang='en'>
            <head>
                <meta charset='UTF-8'>
            </head>
            <body>{}</body>
        </html>
    """.format(response_data)

    return Response(back_body)