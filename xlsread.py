# -*- coding:utf-8 -*-
# @Author: LeoN
# @Time: 2021/3/9 16:03

import xlrd
from calender import Calender
import re

class Address:
    def __init__(self,addressname,text,length):
        self.addressName=addressname
        self._getWeeks(text)
        self.length=int(length)

    def _getWeeks(self,text):
        weekList=[]
        for i in text.split('，'):
            if i.isdigit():
                weekList.append(int(i))
            else:
                start,end=list(map(int,i.split('-')))
                for num in range(start,end+1):
                    weekList.append(num)
        self.weekList=weekList


class Teacher:
    def __init__(self,teachername):
        self.teacherName=teachername
        self.addressList=[]

    def addAddress(self,address):
        self.addressList.append(address)


class Course:
    def __init__(self,text,day,start):
        self.text=text
        self.day=day
        self.start=start
        self.teacherList=[]
        self.getName()
        self.getTeacherList()
        self.adapter()

    def addTeacher(self,teacher):
        self.teacherList.append(teacher)

    @staticmethod
    def getCourseParts(text):
        pattern='\d节</br>'
        if re.search(pattern,text):
            iter=re.finditer(pattern,text)
            list=[]
            start=0
            for res in iter:
                end=res.span()[1]
                list.append(text[start:end])
                start=end
            list.append(text[start:])
            return list
        elif text:
            return [text]
        else:
            return None

    def getName(self):
        namePt='^(.*?)</br>'
        name=re.search(namePt,self.text)[1]
        self.name=name

    def getTeacherList(self):
        pattern='</br>(.*)</br>'
        if re.search(pattern,self.text):
            splits=self.text.split('</br>')
            teacherName1=re.search('([\u4e00-\u9fa5]+)\[',splits[1])[1]
            teacherName2=re.search('，([\u4e00-\u9fa5]+)\[',splits[1])[1]
            numText1,numText2=re.findall('\[(.*?)\]',splits[1])
            addressName=splits[2].split('\n')[0]
            length=(len(splits[2].split('\n')[1])-1)/2
            teacher1=Teacher(teacherName1)
            teacher2=Teacher(teacherName2)
            teacher1.addAddress(Address(addressName,numText1,length))
            teacher2.addAddress(Address(addressName,numText2,length))
            self.addTeacher(teacher1)
            self.addTeacher(teacher2)

        else:
            splits=self.text.split('\n')
            teacherName=re.search('</br>(.*)\[',splits[0])[1]
            if len(splits)>=3:
                addressName1=re.search('周(.*?)$',splits[0])[1]
                numText1=re.search('\[(.*)\]',splits[0])[1]
                length1=(len(re.search('第(.*)节',splits[1])[1])+1)/2
                addressName2=re.search('周(.*?)$',splits[1])[1]
                numText2=re.search('\[(.*)\]',splits[1])[1]
                length2=(len(re.search('第(.*)节',splits[2])[1])+1)/2
                teacher=Teacher(teacherName)
                teacher.addAddress(Address(addressName1,numText1,length1))
                teacher.addAddress(Address(addressName2,numText2,length2))

            else:
                addressName=re.search('周(.*?)$',splits[0])[1]
                numText=re.search('\[(.*)\]',splits[0])[1]
                length=(len(re.search('第(.*)节',splits[1])[1])+1)/2
                teacher=Teacher(teacherName)
                teacher.addAddress(Address(addressName,numText,length))
            self.addTeacher(teacher)

    def adapter(self):
        for teacher in self.teacherList:
            for address in teacher.addressList:
                for week in address.weekList:
                    Calender(week,self.day,self.start,address.length,self.name,teacher.teacherName,address.addressName)

if __name__ == '__main__':
    f=xlrd.open_workbook('刘臻辉课表.xls')
    data=f.sheet_by_index(0)
    for i in range(2,8):
        for j in range(2,9):
            str=data.cell(i,j).value
            parts=Course.getCourseParts(str)
            if parts:
                for x in parts:
                    Course(x,j-1,i-1)
    Calender.render()