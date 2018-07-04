#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/7/4 下午1:48
# @Author  : Wugang Li
# @File    : run.py
# @Software: PyCharm
# @license : Copyright(C), olei.me
# @Contact : i@olei.me

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "ol"])
execute(['scrapy', 'crawl', 'ayk'])
