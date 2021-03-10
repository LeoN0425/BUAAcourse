# -*- coding:utf-8 -*-
# @Author: LeoN
# @Time: 2021/3/3 22:37


import collections
import re
import datetime

a='16周C201第3,啊节'
pattern='^第(\d[\u4e00-\u9fa5]*)节$'

s='第5陈沙发节'
print(re.findall(pattern,s))
start=datetime.datetime(2021,2,28)
res=start+datetime.timedelta(days=7*1+3)
print(res.strftime('%Y%m%d'))

