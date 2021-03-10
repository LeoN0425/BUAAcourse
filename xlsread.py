# -*- coding:utf-8 -*-
# @Author: LeoN
# @Time: 2021/3/9 16:03

import xlrd
from calender import Calender
import re

# f=xlrd.open_workbook('刘臻辉课表.xls')
# data=f.sheet_by_index(0)
# for i in range(2,8):
#     print(data.row_values(i,2))

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

    def addTeacher(self,teacher):
        self.teacherList.append(teacher)

    @staticmethod
    def getCourseParts(text):
        pattern='\d节</br>'
        iter=re.finditer(pattern,text)
        list=[]
        start=0
        for res in iter:
            end=res.span()[1]
            list.append(text[start:end])
            start=end
        list.append(text[start:])
        return list

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
            print(splits[0])
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
                for i in teacher.addressList:
                    print(i.length)
            else:
                addressName=re.search('周(.*?)$',splits[0])[1]
                numText=re.search('\[(.*)\]',splits[0])[1]
                length=(len(re.search('第(.*)节',splits[1])[1])+1)/2
                teacher=Teacher(teacherName)
                teacher.addAddress(Address(addressName,numText,length))
                print(teacher.addressList)
            self.addTeacher(teacher)

    def render(self):
        for teacher in self.teacherList:
            for address in teacher.addressList:
                pass


c='成本管理</br>郑  筠[1-8]周(三)211\n第8，9节</br>信息资源管理</br>何玉敏[9-11，13-16]周，赵吉昌[12]周</br>(一)306'
d='信息资源管理</br>何玉敏[9-11，13-16]周，赵吉昌[12]周</br>(一)306\n第8，9节'
a=Course(d,1,2)
a.getTeacherList()