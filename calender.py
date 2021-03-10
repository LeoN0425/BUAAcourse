# -*- coding:utf-8 -*-
# @Author: LeoN
# @Time: 2021/3/10 23:19

import datetime

class Calender:
    num=0
    startDay=datetime.datetime(2021,2,28)
    def __init__(self,week,day,start,length,course,teacher,address):
        self.week=week
        self.day=day
        self.start=start
        self.length=length
        self.course=course
        self.teacher=teacher
        self.address=address

