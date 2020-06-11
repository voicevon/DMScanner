#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class ImgPSColor:
    '''
    图片处理。目的是将原始图像处理成一个个可识别图像。
    需要注意的是，目前考虑“空”处理。也就是如果有空位置，返回“empty”。
    '''
    def imgPS(self, url):
        # 读取原始图像
        img = cv2.imread(url, 1)
        # 找出黑白灰部分，也就是“底”
        HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        '''
        HSV模型中颜色的参数分别是：色调（H），饱和度（S），明度（V）
        下面两个值是要识别的颜色范围
        灰色：
        H：0--180
        S：0--43
        V：46--220
        黑：
        H：0--180
        S：0--255
        V：0--46
        白：
        H：0--180
        S：0--30
        V：221--225
        蓝色：
        H:100--124
        S:43--255
        V:46--255
        '''
        Min_BoardColor = np.array([0, 0, 0])  # 要识别的颜色的下限
        Max_BoardColor = np.array([180, 225, 225])  # 要识别的颜色的上限
        # mask是把HSV图片中在颜色范围内的区域变成白色，其他区域变成黑色
        mask = cv2.inRange(HSV, Min_BoardColor, Max_BoardColor)
        # 下面是用卷积进行滤波
        kernel_4 = np.ones((4, 4), np.uint8)  # 4x4的卷积核
        dilation = cv2.dilate(mask, kernel_4, iterations=1)
        # dilation = cv2.dilate(dilation, kernel_4, iterations=1)
        # cv2.imshow("mask", dilation)
        # cv2.waitKey(0)
        # 将滤波后的图像变成二值图像放在binary中
        ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)
        # 在binary中发现轮廓，轮廓按照面积从小到大排列
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 找到范围内的，就应该是“底”，把底挨着找出来，就是需要的位置。
        # iMianJi = 0
        for i in range(0, len(contours)):  # 遍历所有的轮廓
            # x, y, w, h = cv2.boundingRect(contours[i])
            # cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2, cv2.LINE_AA)
            # iMianJi = cv2.contourArea(contours[i])
            # cv2.putText(img, "%d" % (iMianJi), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0),2)
            if 13400 < cv2.contourArea(contours[i]) and cv2.contourArea(contours[i]) < 13500:
                # iMianJi = cv2.contourArea(contours[i])
                pan = contours[i]
        # cv2.imshow("img", img)
        # cv2.waitKey(0)
        # 判断最大面积，如果最大面积小于下限，说明红边被遮挡了，这时候是识别不出棋盘的
        # print(iMianJi)

        x, y, w, h = cv2.boundingRect(pan)  # 将轮廓分解为识别对象的左上角坐标和宽、高
        # 在图像上画上矩形（图片、左上角坐标、右下角坐标、颜色、线条宽度）
        # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255,), 3)
        print("w:{0}  h:{1}".format(w, h))
        xNew = x
        yNew = y
        xEnd = x+w
        yEnd = y+h
        # 获取到了单个码
        singleDMDM = img[yNew:yEnd, xNew:xEnd]
        # cv2.imshow("singleDMDM", singleDMDM)
        # cv2.waitKey(0)
        msg = self.imgSigle(singleDMDM)
        return msg

    def imgSigle(self, imgSigle):
        # cv2.imshow("imgSigle", imgSigle)
        # 灰度处理。处理前应该做些锐化或者直方图处理
        sgray = cv2.cvtColor(imgSigle, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(sgray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        edges = cv2.Canny(binary, 50, 150, apertureSize=3)
        # cv2.imshow("edges", edges)
        lines = cv2.HoughLines(edges, 1, np.pi/180, 35)
        if lines is None:
            print("not find any line")
            return
        hudu = 0
        for line in lines:
            rho = line[0][0]  # 第一个元素是距离rho
            theta = line[0][1]  # 第二个元素是角度theta
            print("rho:{0}  theta:{1}".format(rho, theta))
            # print (rho)
            # print (theta)
            if (theta < (np.pi/4.0)) or (theta > (3.*np.pi/4.0)):  # 垂直直线
                # pt1 = (int(rho/np.cos(theta)), 0)               # 该直线与第一行的交点
                # # 该直线与最后一行的焦点
                # pt2 = (int((rho-imgSigle.shape[0]*np.sin(theta))/np.cos(theta)), imgSigle.shape[0])
                # cv2.line(imgSigle, pt1, pt2, (255))             # 绘制一条白线
                hudu = theta
            # else:                                                  # 水平直线
            #     pt1 = (0, int(rho/np.sin(theta)))               # 该直线与第一列的交点
            #     # 该直线与最后一列的交点
            #     pt2 = (imgSigle.shape[1], int((rho-imgSigle.shape[1]*np.cos(theta))/np.sin(theta)))
            #     cv2.line(imgSigle, pt1, pt2, (255), 1)           # 绘制一条直线
        # cv2.imshow("houghline", imgSigle)
        imgRd = self.imgRatated(imgSigle, hudu)
        # sgrayRdRd = cv2.cvtColor(imgRd, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite("dd.png", imgRd)
        # cv2.imshow("imgRatated", imgRd)
        # cv2.waitKey(0)
        # #####################################################################################################
        # 图片选正了以后，就开始进行强化、切片处理了。
        # 3 为Block size, 5为param1值
        # th2 = cv2.adaptiveThreshold(sgrayRdRd, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 5)
        sgrayRD = cv2.cvtColor(imgRd, cv2.COLOR_BGR2GRAY)
        ret, binaryRd = cv2.threshold(sgrayRD, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # cv2.imshow("binaryRd", binaryRd)
        # cv2.waitKey(0)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        binaryRd = cv2.morphologyEx(binaryRd, cv2.MORPH_CLOSE, kernel)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        binaryRd = cv2.morphologyEx(binaryRd, cv2.MORPH_CLOSE, kernel)
        # cv2.imshow("binaryRd", binaryRd)
        # cv2.waitKey(0)
        contours, hierarchy = cv2.findContours(binaryRd, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 找到范围内的，就应该是“底”，把底挨着找出来，就是需要的位置。
        # iMianJi = 0
        for i in range(0, len(contours)):  # 遍历所有的轮廓
            # x, y, w, h = cv2.boundingRect(contours[i])
            # cv2.rectangle(imgRd, (x, y), (x+w, y+h), (255, 0, 0), 2, cv2.LINE_AA)
            # iMianJi = cv2.contourArea(contours[i])
            # cv2.putText(imgRd, "%d" % (iMianJi), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            if 1800 < cv2.contourArea(contours[i]) and cv2.contourArea(contours[i]) < 2500:
                # iMianJi = cv2.contourArea(contours[i])
                pan = contours[i]
        # cv2.imshow("imgRd", imgRd)
        # cv2.waitKey(0)
        x, y, w, h = cv2.boundingRect(pan)  # 将轮廓分解为识别对象的左上角坐标和宽、高
        # 在图像上画上矩形（图片、左上角坐标、右下角坐标、颜色、线条宽度）
        # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255,), 3)
        print("w:{0}  h:{1}".format(w, h))
        xNew = x
        yNew = y
        xEnd = x+w
        yEnd = y+h
        # 获取到了单个码
        singleDMDM = imgRd[yNew:yEnd, xNew:xEnd]
        self.deCodeSingleImg(singleDMDM)

    def deCodeSingleImg(self, singleImg):
        '''
        单图像解析预备。
        主要是图像的分析，然后生成标准图像。
        '''
        height, width = singleImg.shape[:2]
        print("w:{0}  h:{1}".format(width, height))
        # cv2.imshow("singleImg", singleImg)
        # cv2.waitKey(0)
        sigleStandardImg = self.SuoFang(singleImg, 126, 126)
        sgray = cv2.cvtColor(sigleStandardImg, cv2.COLOR_BGR2GRAY)
        ret, binaryRd = cv2.threshold(sgray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        cv2.imshow("binaryRd", binaryRd)
        cv2.waitKey(0)
        # 白0 黑1
        # 生成一张标准 14×14 ，内容全是白
        # num_list = [[0]*14]*14
        binaryRd = 255 - binaryRd
        num_list = [[0] * 14 for i in range(14)]
        for i in range(0, 14):
            for j in range(0, 14):
                if i == 0:
                    num_list[i][j] = (j+1) % 2
                elif i == 13:
                    num_list[i][j] = 1
                elif j == 0:
                    num_list[i][j] = 1
                elif j == 13:
                    num_list[i][j] = i % 2
                else:
                    # 取当前位置的值
                    num_list[i][j] = self.getBorW(binaryRd, i, j)

        for i in range(0, 14):
            print(num_list[i])
        # 根据解析生成新的图片
        imgDMCode = self.getDMImg(num_list)
        cv2.imshow("imgDMCode", imgDMCode)
        cv2.imwrite("sd.png", imgDMCode)
        cv2.imshow("sigleStandardImg", sigleStandardImg)
        cv2.imshow("binaryRd", binaryRd)
        cv2.waitKey(0)

    def imgRatated(self, img, hudu):
        JiaoDu = hudu * 180 / np.pi - 90
        print("jiaodu:{0}".format(JiaoDu))
        height, width = img.shape[:2]
        M = cv2.getRotationMatrix2D((width/2, height/2), JiaoDu, 1)
        dst = cv2.warpAffine(img, M, (width, height))
        return dst

    def getBorW(self, img, x, y):
        xNew = y*9
        yNew = x*9
        xEnd = xNew+9
        yEnd = yNew+9
        # 获取到了单个码。白：255 黑：0
        singleCode = img[yNew:yEnd, xNew:xEnd]
        cv2.rectangle(img, (xNew, yNew), (xEnd, yEnd), (0, 255, 0), 1)
        # print("x:{0}  Y:{1}".format(x, y))
        avg = np.mean(singleCode)
        # cv2.imshow("img", img)
        # cv2.imshow("singleCode", singleCode)
        # print("avg:{0}  i:{1}  j:{2}".format(avg, x, y))
        # cv2.waitKey(0)
        if avg > 110:
            # print(0)
            return 0
        else:
            # print(1)
            return 1

    def getDMImg(self, num):
        print("开始绘图——")
        num = [[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
               [1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1],
               [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
               [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
               [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
               [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1],
               [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0],
               [1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
               [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1],
               [1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0],
               [1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
               [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        img = np.zeros([146, 146, 1], dtype=np.uint8)
        # img = [[255] * 136 for i in range(136)]
        for i in range(0, 146):
            for j in range(0, 146):
                img[i][j] = 255
        for i in range(0, 14):
            for j in range(0, 14):
                if num[i][j] == 0:
                    # 白
                    for ii in range(0, 9):
                        for jj in range(0, 9):
                            img[i*9 + ii + 10][j*9 + jj + 10] = 255
                else:
                    # 黑
                    for ii in range(0, 9):
                        for jj in range(0, 9):
                            img[i*9 + ii + 10][j*9 + jj + 10] = 0
        return img

    def SuoFang(self, img, w, h):
        '''
        原始图片，缩放后的宽度，高度
        '''
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # resize参数中是“宽，高”，刚好和shape出来的高、宽顺序相反
        res = cv2.resize(img, (w, h), interpolation=cv2.INTER_CUBIC)
        return res


if __name__ == '__main__':
    imgsimgs = ImgPSColor().imgPS('a7.png')
