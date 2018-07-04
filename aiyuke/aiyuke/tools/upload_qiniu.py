#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/7/4 下午2:43
# @Author  : Wugang Li
# @File    : upload_qiniu.py
# @Software: PyCharm
# @license : Copyright(C), olei.me
# @Contact : i@olei.me


import qiniu.config
from qiniu import Auth,put_file, etag, urlsafe_base64_encode

def upload(local_image):
    access_key = "QxR4DsIF-JaA5-WY4j6JZVnGlS6KUnEubOE5C8HP"
    secret_key = "prMuv9EtxpfjzgOio3_MCiDrj9FEZiZB95na0CDT"
    # dirname = "aiyuke/"
    key = local_image
    # 验证七牛云身份
    q = Auth(access_key, secret_key)

    # 七牛云的存储名字
    bucket_name = "lwg-cunchu"

    # 上传
    token = q.upload_token(bucket_name, key, 3600)
    # local_image = "../aiyuke/{}".format(image_name)
    ret, info = put_file(token, key, local_image)
    print(info)
    assert ret['key'] == key
    assert ret['hash'] == etag(local_image)
