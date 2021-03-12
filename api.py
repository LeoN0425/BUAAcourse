# -*- coding:utf-8 -*-
# @Author: LeoN
# @Time: 2021/3/3 23:32

import os
import re
from aip import AipOcr
from myAPI import *

client=AipOcr(APP_ID,API_KEY,SECRET_KEY)
with open('13/25.jpg','rb') as f:
    image=f.read()
    res=client.basicAccurate(image)['words_result']

def getTextList(res):
    list=[]
    for i in res:
        list.append(i['words'])
    return list

list=getTextList(res)
print(list)
def getParts(list):
    pattern='第(\d[^\u4e00-\u9fa5]*)节$'
    parts=[]
    item=[]
    tmpstr=''
    for i in range(len(list)):
        tmpstr+=list[i]
        if item and i>0:
            if re.search(pattern,list[i]) or re.search(pattern,list[i-1]+list[i]):
                item.append(tmpstr)
                parts.append(item)
                item=[]
                tmpstr=''
        else:
            item.append(tmpstr)
            tmpstr=''
    return parts

print(getParts(list))