#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""视频点播结果查询接口python示例代码
接口文档: http://dun.163.com/api.html
python版本：python2.7
运行:
    1. 修改 SECRET_ID,SECRET_KEY,BUSINESS_ID 为对应申请到的值
    2. $ python text_check_callback_demo.py
"""
__author__ = 'yidun-dev'
__date__ = '2017/6/9'
__version__ = '0.1-dev'

import hashlib
import time
import random
import urllib
import urllib2
import json

class VideoQueryByTaskIdsDemo(object):
    """视频点播查询接口示例代码"""
    API_URL = "https://as.dun.163yun.com/v1/video/query/task"
    VERSION = "v3"

    def __init__(self, secret_id, secret_key, business_id):
        """
        Args:
            secret_id (str) 产品密钥ID，产品标识
            secret_key (str) 产品私有密钥，服务端生成签名信息使用
            business_id (str) 业务ID，易盾根据产品业务特点分配
        """
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.business_id = business_id

    def gen_signature(self, params=None):
        """生成签名信息
        Args:
            params (object) 请求参数
        Returns:
            参数签名md5值
        """
        buff = ""
        for k in sorted(params.keys()):
            buff += str(k)+ str(params[k])
        buff += self.secret_key
        return hashlib.md5(buff).hexdigest()

    def query(self,params):
        """请求易盾接口
        Args:
            params (object) 请求参数
        Returns:
            请求结果，json格式
        """
        params["secretId"] = self.secret_id
        params["businessId"] = self.business_id
        params["version"] = self.VERSION
        params["timestamp"] = int(time.time() * 1000)
        params["nonce"] = int(random.random()*100000000)
        params["signature"] = self.gen_signature(params)

        try:
            params = urllib.urlencode(params)
            request = urllib2.Request(self.API_URL, params)
            content = urllib2.urlopen(request, timeout=10).read()
            return json.loads(content)
        except Exception, ex:
            print "调用API接口失败:", str(ex)

if __name__ == "__main__":
    """示例代码入口"""
    SECRET_ID = "your_secret_id" # 产品密钥ID，产品标识
    SECRET_KEY = "your_secret_key" # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
    BUSINESS_ID = "your_business_id" # 业务ID，易盾根据产品业务特点分配
    video_query_api = VideoQueryByTaskIdsDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)
    
    taskIds = ['c679d93d4a8d411cbe3454214d4b1fd7', '49800dc7877f4b2a9d2e1dec92b988b6'] #查询参数 taskids
    params = {
        "taskIds": taskIds
    }
    ret = video_query_api.query(params)
    if ret["code"] == 200:
        for result in ret["result"]:
            if result["status"]!=0:
                print "获取结果异常,status=%s" % (result["status"])
                continue
            if result["level"]==0:
                print "正常, callback=%s" % (result["callback"])
            elif result["level"]==1 or result["level"]==2:
                for evidence in result["evidences"]:
                    beginTime=evidence["beginTime"]
                    endTime=evidence["endTime"]
                    type=evidence["type"]
                    url=evidence["url"]
                    for labelItem in evidence["labels"]:
                        label=labelItem["label"]
                        level=labelItem["level"]
                        rate=labelItem["rate"]
                print "%s, callback=%s, 证据信息：%s, 证据分类：%s" %("不确定" if result["level"]==1 else "确定" ,result["callback"],evidence,evidence["labels"])        
    else:
        print "ERROR: code=%s, msg=%s" % (ret["code"], ret["msg"])
