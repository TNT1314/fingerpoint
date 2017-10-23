#! usr/bin/env python
# encoding: utf-8
from django.shortcuts import render

# Create your views here.

import os
from collections import OrderedDict
from django.conf import settings
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.files.uploadedfile import SimpleUploadedFile

def finger_point_test_html_01(request):
    return render(request, 'fingerpoint.html')


@api_view(['GET', 'POST'])
def finger_point_test_api_01(request):
    """
        Finger image test

        参数:
            deviceid: 设备编号
            file01: 文件1
            file02: 文件2
            file03: 文件3
            file04: 文件4
            file05: 文件5
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
        if req_data['deviceid'] == '110102006229':
            upload_path = os.path.join(u"{}/upload".format(settings.BASE_DIR))

            if not os.path.exists(upload_path):
                os.makedirs(upload_path)

            for x in range(5):
                image_file = req_data['file{:0>2d}'.format(x+1)]
                if image_file:
                    # 打开特定的文件进行二进制的写操作
                    destination = open(u"{}/{}".format(upload_path, image_file.name), 'wb+')
                    for chunk in image_file.chunks():  # 分块写入文件
                        destination.write(chunk)
                    destination.close()
                    rsp_data['data']['{:0>2d}_url'.format(x+1)] = u"/media/{}".format(image_file.name)

            rsp_data['code'] = '10000'
            rsp_data['mesage'] = u'成功！成功文件数量：{}。'.format(len(rsp_data['data']))
        else:
            rsp_data['code'] = '10001'
            rsp_data['mesage'] = '失败！'
    else:
        rsp_data['code'] = '10001'
        rsp_data['mesage'] = '失败！'
    return Response(rsp_data)