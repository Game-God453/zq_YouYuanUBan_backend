# -*- coding: utf-8 -*-
import os
import uuid

import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())

# 填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为 https://oss-cn-hangzhou.aliyuncs.com。
endpoint = "https://oss-cn-beijing.aliyuncs.com"

# 填写Endpoint对应的Region信息，例如cn-hangzhou。注意，v4签名下，必须填写该参数
region = "cn-beijing"

# yourBucketName填写存储空间名称。
bucket_name = "gx-big-event"  # 替换为你的Bucket名称
bucket = oss2.Bucket(auth, endpoint, bucket_name, region=region)

def generate_unique_filename(original_filename):
    """
    生成唯一的文件名，保留原始文件的扩展名。
    :param original_filename: 原始文件名
    :return: 唯一的文件名
    """
    # 获取文件的扩展名
    _, file_extension = os.path.splitext(original_filename)

    # 生成 UUID 作为文件名，并拼接扩展名
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    return unique_filename



@csrf_exempt  # 如果前端和后端不在同一域名下，可能需要禁用CSRF保护
def upload_image(request):
    if request.method == "POST":
        # 获取前端上传的文件
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({
                'data': None,
                'message': "没有文件上传！",
                'status': 400
            })

        # 获取文件名并构造OSS中的Object名称
        object_name = generate_unique_filename(file.name)  # 可以根据需要修改Object名称
        print(f"Uploading file: {object_name}")

        # 上传图片到OSS
        try:
            result = bucket.put_object(object_name, file)
            print('http status: {0}'.format(result.status))
            print('request_id: {0}'.format(result.request_id))
            print('ETag: {0}'.format(result.etag))
            print('date: {0}'.format(result.headers['date']))

            # 返回上传成功的url
            url = f"https://{bucket_name}.{endpoint[endpoint.rfind('/') + 1:]}/{object_name}"
            return JsonResponse({
                'data': url,
                'message': "文件上传成功！",
                'status': 200
            }),url
        except Exception as e:
            print(f"Error uploading file: {e}")
            return JsonResponse({
                'data': None,
                'message': "文件上传失败！",
                'status': 400
            }),None
    else:
        return JsonResponse({
            'data': None,
            'message': "无效请求！",
            'status': 405
        }),None