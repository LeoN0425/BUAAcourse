# -*- coding:utf-8 -*-
# @Author: LeoN
# @Time: 2021/3/12 22:10

import xlrd
from adapter import Course,Calendar

if __name__ == '__main__':
    data=xlrd.open_workbook('刘臻辉课表.xls').sheet_by_index(0)
    for i in range(2,8):
        for j in range(2,9):
            str=data.cell(i,j).value
            str=str.replace('\n',' ')
            str=str.replace('</br>','\n')
            parts=Course.getCourseParts(str)
            if parts:
                for x in parts:
                    Course(x,j-1,i-1)
    Calendar.render('C:/Users/GeniusLEO/Desktop','我的日历')