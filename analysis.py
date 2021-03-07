# -*- coding:utf-8 -*-
# @Author: LeoN
# @Time: 2021/3/3 22:40

from PIL import Image
from collections import Counter

image=Image.open('捕获.JPG')
width,height=image.size

def getLineSplit(image,line):
    width=image.size[0]
    resList=[]
    tmp=0
    for i in range(width-1):
        if image.getpixel((i,line))==image.getpixel((i+1,line)):
            if tmp==0:
                link=i
            tmp+=1
        else:
            if tmp>=50:
                resList.append(link)
            tmp=0
    return resList

def getColSplit(image,col):
    height=image.size[1]
    resList=[]
    tmp=0
    for i in range(height-1):
        if image.getpixel((col,i))==image.getpixel((col,i+1)):
            if tmp==0:
                link=i
            tmp+=1
        else:
            if tmp>=20:
                resList.append(link)
            tmp=0
    return resList

def getImageSplit(image):
    lineSplitList=[]
    for i in range(0,image.size[1],1):
        lineSplit=getLineSplit(image,i)
        if len(lineSplit)>5:
            lineSplitList.append(tuple(lineSplit))
    lineCounts=Counter(lineSplitList)
    imageLineSplit=lineCounts.most_common()[0][0]
    colSplitList=[]
    for i in range(0,image.size[0],1):
        colSplit=getColSplit(image,i)
        if len(colSplit)>5:
            colSplitList.append(tuple(colSplit))
    colCounts=Counter(colSplitList)
    imageColSplit=colCounts.most_common()[0][0]
    imageLineSplit=list(imageLineSplit)
    imageLineSplit.append(image.size[0])
    imageColSplit=list(imageColSplit)
    imageColSplit.append(image.size[1])
    return imageLineSplit,imageColSplit

getImageSplit(image)
def getPartImage(image):
    lineSplit,colSplit=getImageSplit(image)
    imageParts=[]
    for i in range(len(lineSplit)-1):
        for j in range(len(colSplit)-1):
            res=image.crop((lineSplit[i],colSplit[j],lineSplit[i+1],colSplit[j+1]))
            imageParts.append(res)
    return imageParts
for num,i in enumerate(getPartImage(image)):
    i.save('13/'+str(num)+'.jpg')





'''
    思路: 由上至下, 等距取点, 有3样数据可以出现7份较好数据即可
    化成7*6表格, 分别进行图像文本识别
    格式:
        课名
        任课老师
        周数
        教室
        节数
'''
