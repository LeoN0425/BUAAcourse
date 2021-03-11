# -*- coding:utf-8 -*-
# @Author: LeoN
# @Time: 2021/3/10 23:19

import datetime

class Calender:
    num=0
    startDay=datetime.datetime(2021,2,28)
    allCalender=[]
    time_dict={1:480,2:590,3:840,4:950,5:1140,6:1240}
    BEGIN_TEXT='BEGIN:VCALENDAR\nPRODID:LeoN\nVERSION:2.0\nCALSCALE:GREGORIAN' \
               '\nMETHOD:PUBLISH\nX-WR-CALNAME:BUAA2021SPRING\nX-WR-TIMEZONE:Asia/Shanghai'
    END_TEXT='\nEND:VCALENDAR'
    TEMPLATE='\nBEGIN:VEVENT\nDTSTAMP:20210311T171600Z\nUID:leon0425\nCREATED:20210311T171600Z' \
             '\nLAST-MODIFIED:20210311T171600Z\nSTATUS:CONFIRMED\nTRANSP:OPAQUE'

    def __init__(self,week,day,start,length,course,teacher,address):
        self.week=week
        self.day=day
        self.start=start
        self.length=length
        self.course=course
        self.teacher=teacher
        self.address=address
        self.sequence=str(Calender.num)
        Calender.num+=1
        Calender.allCalender.append(self)

    @classmethod
    def render(self):
        RENDER_TEXT=self.BEGIN_TEXT
        for calender in self.allCalender:
            RENDER_TEXT+=self.TEMPLATE
            startTime=(self.startDay+datetime.timedelta(days=7*(calender.week-1)+
                                calender.day,minutes=self.time_dict[calender.start]))
            endTime=(startTime+datetime.timedelta(minutes=calender.length*50-5))
            START=startTime.strftime('%Y%m%dT%H%M%S')
            END=endTime.strftime('%Y%m%dT%H%M%S')
            SUMMARY=calender.course
            LOCATION=calender.address
            DESCRIPTION=calender.teacher
            INSERT_TEXT='\nDTSTART:'+START+'\nDTEND:'+END+'\nSEQUENCE:'+calender.sequence+'\nSUMMARY:'+\
                        SUMMARY+'\nLOCATION:'+LOCATION+'\nDESCRIPTION:'+DESCRIPTION
            RENDER_TEXT+=INSERT_TEXT
            RENDER_TEXT+='\nEND:VEVENT'
        RENDER_TEXT+=self.END_TEXT
        with open('日历.txt','w') as f:
            f.write(RENDER_TEXT)
