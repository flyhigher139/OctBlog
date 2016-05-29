#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

def submit_url_to_baidu(baidu_url, url):
    res = requests.post(baidu_url, data=url)
    return res