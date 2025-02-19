# # import random
# # import string
# #
# #
# # from django.test import TestCase
# #
# # # Create your tests here.
# #
# # def generate_random_string(length=6):
# #     # 定义字符池，包含大小写字母和数字
# #     characters = string.ascii_letters + string.digits
# #     # 使用random.choices随机选择字符
# #     random_string = ''.join(random.choices(characters, k=length))
# #     return random_string
# #
# # # 调用函数生成6个字符的字符串
# # result = generate_random_string(12)
# # print(result)
#
# import uuid
# import os
#
#
# def generate_unique_filename(original_filename):
#     """
#     生成唯一的文件名，保留原始文件的扩展名。
#     :param original_filename: 原始文件名
#     :return: 唯一的文件名
#     """
#     # 获取文件的扩展名
#     _, file_extension = os.path.splitext(original_filename)
#
#     # 生成 UUID 作为文件名，并拼接扩展名
#     unique_filename = f"{uuid.uuid4()}{file_extension}"
#     return unique_filename
#
#
# # 示例用法
# original_filename = "example.jpg"
# unique_filename = generate_unique_filename(original_filename)
# print("Original Filename:", original_filename)
# print("Unique Filename:", unique_filename)
from user.tools.aliyun_fileupdate import endpoint

endpoint = "https://oss-cn-beijing.aliyuncs.com"
result = endpoint[endpoint.rfind('/') + 1:]
print(result)  # 输出: resource