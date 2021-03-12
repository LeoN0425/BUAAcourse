# -*- coding:utf-8 -*-
# @Author: LeoN
# @Time: 2021/3/9 16:03

from calendar import Calendar
import re

class Address:
    def __init__(self,addressName,text,length):
        self.addressName=addressName
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
    def __init__(self,teacherName):
        self.teacherName=teacherName
        self.addressList=[]

    def addAddress(self,address):
        self.addressList.append(address)


class Course:
    def __init__(self,textSplits,day,start):
        self.textSplits=textSplits
        self.day=day
        self.start=start
        self.process()
        self.adapt()

    def addTeacher(self,teacher):
        self.teacherList.append(teacher)

    @staticmethod
    def getCourseParts(text):
        if len(text)<=5:
            return None
        splitText=text.split('\n')
        if len(splitText)<=3:
            return [splitText]
        numList=[0]
        splitTextParts=[]
        for num,str in enumerate(splitText):
            if re.search('第(.*)节$',str):
                numList.append(num+1)
        for i in range(len(numList)-1):
            splitTextParts.append(splitText[numList[i]:numList[i+1]])
        return splitTextParts

    def process(self):
        self.teacherList=[]
        self.name=self.textSplits[0]
        if len(self.textSplits)>=3:
            teacherName1=re.search('([\u4e00-\u9fa5]+)\[',self.textSplits[1])[1]
            teacherName2=re.search('，([\u4e00-\u9fa5]+)\[',self.textSplits[1])[1]
            numText1,numText2=re.findall('\[(.*?)\]',self.textSplits[1])
            addressName=self.textSplits[2].split(' ')[0]
            length=(len(self.textSplits[2].split(' ')[1])-1)/2
            teacher1=Teacher(teacherName1)
            teacher2=Teacher(teacherName2)
            teacher1.addAddress(Address(addressName,numText1,length))
            teacher2.addAddress(Address(addressName,numText2,length))
            self.addTeacher(teacher1)
            self.addTeacher(teacher2)

        else:
            intervalNum=re.search('^(.*?)\[',self.textSplits[1]).end()-1
            teacherName=self.textSplits[1][:intervalNum]
            splits=self.textSplits[1][intervalNum:].split(' ')

            if len(splits)>=3:
                addressName1=re.search('周(.*?)$',splits[0])[1]
                numText1=re.search('\[(.*?)\]',splits[0])[1]
                length1=(len(re.search('第(.*?)节',splits[1])[1])+1)/2
                addressName2=re.search('周(.*?)$',splits[1])[1]
                numText2=re.search('\[(.*?)\]',splits[1])[1]
                length2=(len(re.search('第(.*?)节',splits[2])[1])+1)/2
                teacher=Teacher(teacherName)
                teacher.addAddress(Address(addressName1,numText1,length1))
                teacher.addAddress(Address(addressName2,numText2,length2))

            else:
                addressName=re.search('周(.*?)$',splits[0])[1]
                numText=re.search('\[(.*?)\]',splits[0])[1]
                length=(len(re.search('第(.*?)节',splits[1])[1])+1)/2
                teacher=Teacher(teacherName)
                teacher.addAddress(Address(addressName,numText,length))

            self.addTeacher(teacher)

    def adapt(self):
        for teacher in self.teacherList:
            for address in teacher.addressList:
                for week in address.weekList:
                    Calendar(week,self.day,self.start,address.length,self.name,teacher.teacherName,address.addressName)
