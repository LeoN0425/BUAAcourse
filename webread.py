# -*- coding:utf-8 -*-
# @Author: LeoN
# @Time: 2021/3/12 17:15

import time
from selenium import webdriver
from adapter import Course,Calendar

class WebReader:
    loginURL='https://sso.buaa.edu.cn/login?service=http%3A%2F%2Fjwxt.buaa.edu.cn%3A8080%2Fieas2.1%2Fwelcome%3Ffalg%3D1'
    courseURL='http://jwxt.buaa.edu.cn:8080/ieas2.1/kbcx/queryGrkb'

    def __init__(self,id,pwd,driverPath,path,name):
        self.id=id
        self.pwd=pwd
        self.driver=webdriver.Chrome(driverPath)
        self.path=path
        self.name=name

    def login(self):
        self.driver.get(self.loginURL)
        time.sleep(2)
        self.driver.switch_to.frame('loginIframe')
        inputUserName=self.driver.find_element_by_id("unPassword")
        inputPassWord=self.driver.find_element_by_id('pwPassword')
        button=self.driver.find_element_by_xpath('//*[@id="content-con"]/div[1]/div[7]/input')
        inputUserName.send_keys(self.id)
        inputPassWord.send_keys(self.pwd)
        button.click()
        time.sleep(1)
        self.driver.get(self.courseURL)

    def getCalendar(self):
        template='/html/body/div[1]/div/div[8]/div[2]/table/tbody/tr['
        for i in range(2,8):
            for j in range(3,10):
                xpath=template+str(i)+']/td['+str(j)+']'
                string=self.driver.find_element_by_xpath(xpath).text
                parts=Course.getCourseParts(string)
                if parts:
                    for x in parts:
                        Course(x,j-2,i-1)
            Calendar.render(path,name)

    def run(self):
        self.login()
        self.getCalendar()
        self.driver.close()

if __name__ == '__main__':
    ID=''                 #统一认证账号
    PWD=''                #密码
    driverPath=''         #'chromediver.exe'的路径
    path=''               #生成ics日历文件的所在文件夹路径
    name=''               #生成ics日历文件的名称
    webReader=WebReader(ID,PWD,driverPath,path,name)
    webReader.run()
