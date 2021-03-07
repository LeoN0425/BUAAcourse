# -*- coding:utf-8 -*-
# @Author: LeoN
# @Time: 2021/3/3 22:37


import collections
import re

a='16周C201第3,啊节'
pattern='第(\d[^\u4e00-\u9fa5]*)节$'
if re.search(pattern,a):
    print(1)