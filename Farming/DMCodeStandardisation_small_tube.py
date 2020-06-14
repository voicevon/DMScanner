#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
# import random
import numpy as np
from DMDecode import DMDecoder


class DMCodeStandardisation:
    '''
    分割的图片返回解码结果。
    该处理分成了几步：
    1.原始图像的提前
    2.网格化识别
    3.生成标准图像
    4.标准图像解码
    '''
    def GetDMCodeImg(self, img):
        '''
        根据传入的图像，返回标准DMCode图像。
        '''
        # 第零步，判断是否有码，也就是是否是空的*******************************
        haveCode = self.isHaveAnyCode(img)
        print(haveCode)
        if haveCode is False:
            return "NoneNoneNo"
        # 第一步，放大图像××××××××××××××××××××××××××××××××××××××××××××××××××××
        height, width = img.shape[:2]
        img = self.SuoFang(img, int(width * 3.5), int(height * 3.5))
        # 第二步，图像转正×××××××××××××××××××××××××××××××××××××××××××××××××××××××
        imgUpright = self.getUprightImg(img)
        # cv2.imshow("imgUpright", imgUpright)
        # cv2.waitKey(0)
        # 第三步，二维码图像截取
        imgCode = self.getCodeImg(imgUpright)
        # cv2.imshow("imgCode", imgCode)
        # cv2.waitKey(0)
        # return
        # 第四步，直方图处理
        StandardImg = self.SuoFang(imgCode, 280, 280)
        sgray = cv2.cvtColor(StandardImg, cv2.COLOR_BGR2GRAY)
        dst = cv2.equalizeHist(sgray)
        # ThresholdValue = [108, 95, 100, 110, 120, 130]
        for i in range(120, 80, -5):
            # 第五步，图像识别为数组。
            codeArray = self.getCodeArrayByImg(dst, i)
            # 第六步，数组生成标准DMCode图像
            imgR = self.getSandartImg(codeArray)
            # cv2.imwrite("sss.png", imgR)
            # 第七步，标准图识别
            iCode = DMDecoder.decode(imgR)
            # print("ThresholdValue:{0}".format(ThresholdValue[i]))
            print("i={0} code={1}".format(i, iCode))
            if iCode != "Error":
                return iCode
        return "ErrorError"

    def getCodeImg(self, img):
        '''
        获取DMcode的图像区域，需要截取出准确的图像。
        '''
        sgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # dst = cv2.equalizeHist(sgray)
        # cv2.imshow("sgray", sgray)
        # cv2.imshow("dst", dst)
        # 这里的参数可能需要调整
        ret, binaryRd = cv2.threshold(sgray,  120, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        # 开操作。去白点。消除毛边
        binaryRd = cv2.morphologyEx(binaryRd, cv2.MORPH_OPEN, kernel)
        binaryRd = cv2.morphologyEx(binaryRd, cv2.MORPH_OPEN, kernel2)
        # binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel2)
        # 闭操作。去黑点，联通区域
        # binary = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        binaryRd = cv2.morphologyEx(binaryRd, cv2.MORPH_CLOSE, kernel)
        binaryRd = cv2.morphologyEx(binaryRd, cv2.MORPH_CLOSE, kernel2)
        # cv2.imshow("binary", binary)
        # cv2.waitKey(0)
        # binary = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel2)
        # cv2.imshow("binary", binary)
        # cv2.waitKey(0)
        # cv2.imshow("binary", binary)
        # cv2.waitKey(0)
        # cv2.imshow("binaryRd", binaryRd)
        # cv2.waitKey(0)
        contours, hierarchy = cv2.findContours(binaryRd, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours.sort(key=cv2.contourArea, reverse=True)
        # for i in range(0, len(contours)):
        #     print(cv2.contourArea(contours[i]))
        x, y, w, h = cv2.boundingRect(contours[0])  # 将轮廓分解为识别对象的左上角坐标和宽、高
        # 在图像上画上矩形（图片、左上角坐标、右下角坐标、颜色、线条宽度）
        # print("W:{} H:{}".format(w, h))
        yNew = y + h - w
        wNew = w
        if h > w:
            wNew = h
        # if w > h:
        #     CodeImg = img[y+3:y+3+w, x:x+w]
        # else:
        #     CodeImg = img[y+3:y+3+w, x:x+w]
        CodeImg = img[yNew:yNew+wNew, x:x+wNew]
        # if w < h:
        #     # cv2.rectangle(img, (x, y), (x+w, y+w), (0, 255, 0), 1)
        #     CodeImg = img[y+2:y+2+w, x:x+w]
        # else:
        #     # cv2.rectangle(img, (x, y), (x+h, y+h), (0, 255, 0), 1)
        #     CodeImg = img[y+2:y+2+h, x:x+h]
        # print("w:{0}  h:{1}".format(w, h))
        # cv2.imshow("img", img)
        # cv2.imshow("CodeImg", CodeImg)
        # cv2.waitKey(0)
        return CodeImg

    def getCodeArrayByImg(self, img, ThresholdValue):
        '''
        通过图片获取对应的DMcode二维编码值。
        '''
        # 白0 黑1
        # 生成一张标准 14×14 ，内容全是白
        # num_list = [[0]*14]*14
        # dst = 255 - dst
        lbimg = cv2.medianBlur(img, 3)
        lbimg = cv2.medianBlur(lbimg, 5)
        lbimg = cv2.medianBlur(lbimg, 7)
        ret, binaryRd = cv2.threshold(img,  ThresholdValue, 255, cv2.THRESH_BINARY)
        binaryRd = 255 - binaryRd
        # cv2.imshow("img", img)
        # cv2.imshow("lbimg", lbimg)
        # # cv2.imshow("dst", dst)
        # # cv2.imwrite("sssd.png", binaryRd)
        # cv2.waitKey(0)
        # cv2.imshow("binaryRd", binaryRd)
        kerne0 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        # 闭操作。去黑点
        binaryRd = cv2.morphologyEx(binaryRd, cv2.MORPH_CLOSE, kerne0)
        binaryRd = cv2.morphologyEx(binaryRd, cv2.MORPH_CLOSE, kernel)
        binaryRd = cv2.morphologyEx(binaryRd, cv2.MORPH_CLOSE, kernel2)
        # binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel2)
        # cv2.imshow("binary", binaryRd)
        # cv2.waitKey(0)
        # binary = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel2)
        # cv2.imshow("binary", binary)
        # cv2.waitKey(0)
        # 开操作。去白点
        # binaryRd = cv2.morphologyEx(binaryRd, cv2.MORPH_OPEN, kernel)
        # binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel2)
        # cv2.imshow("binary", binaryRd)
        # cv2.waitKey(0)
        # 为了分割更准确，要找到凸点。也就是定位点。
        # 然后通过定位点，确定X、Y的起点以及步长。
        xyAndStep = self.getXYandStep(binaryRd)
        # print("xyAndStep:{0}".format(xyAndStep))
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
                    num_list[i][j] = self.getBorW(binaryRd, i, j, xyAndStep)

        # for i in range(0, 14):
        #     print(num_list[i])
        return num_list

    def getXYandStep(self, img):
        '''
        确定图像的网格起点以及步长
        '''
        # X起点和步长  Y起点和步长
        iReturn = [0.0, 0.0, 0.0, 0.0]
        imgLU = img[0:40, 0:40]
        imgRU = img[0:60, 220:280]
        imgRD = img[240:280, 240:280]
        # cv2.imshow("img", img)
        # cv2.imshow("imgLU", imgLU)
        # cv2.imshow("imgRU", imgRU)
        # cv2.imshow("imgRD", imgRD)
        # cv2.waitKey(0)
        xB = 0
        xE = 0
        yB = 0
        yE = 0
        # 处理左上角，获取X的起点位置
        xBZ = 0
        xBcont = 0
        for x in range(0, 40):
            imgLine = imgLU[x:x+1, 0:40]
            # cv2.imshow("imgLine", imgLine)
            # cv2.waitKey(0)
            avg = np.mean(imgLine)
            # print(avg)
            if avg < 200 and avg > 100:
                isBlack = False
                for j in range(0, 40):
                    if imgLine[0][j] < 255:
                        xBcont = xBcont + 1
                        xBZ += j
                        isBlack = True
                    else:
                        if isBlack is True:
                            break
                # if xBcont == 0:
                #     xB = 11
                # else:
                #     xB = xBZ/xBcont
                # # print("XB:{0} XZ:{1} xBcont:{2}".format(xB, xBZ, xBcont))
                # break
        if xBcont == 0:
            xB = 11
        else:
            xB = xBZ/xBcont
        # print("XB:{0} XBZ:{1} xBcont:{2}".format(xB, xBZ, xBcont))
        if xB > 20:
            xB = 11
        # 处理右上，获取X终点位置。理论上切出来的是“白黑白”区域。
        # 白：255 黑：0
        xBZ = 0
        xBcont = 0
        for x in range(0, 60):
            imgLine = imgRU[x:x+1, 0:60]
            # cv2.imshow("imgLine", imgLine)
            # cv2.waitKey(0)
            avg = np.mean(imgLine)
            # print(avg)
            if avg < 100:
                break
            if avg < 200 and avg > 100:
                isBlack = False
                for j in range(0, 60):
                    if imgLine[0][59-j] < 255:
                        xBcont = xBcont + 1
                        xBZ += 59-j
                        isBlack = True
                    else:
                        if isBlack is True:
                            break
                # if xBcont == 0:
                #     xE = 251
                # else:
                #     xE = 240 + xBZ/xBcont
                # # print("xE:{0} XZ:{1} xBcont:{2}".format(xE, xBZ, xBcont))
                # break
        if xBcont == 0:
            xE = 251
        else:
            xE = 220 + xBZ/xBcont
        # print("xE:{0} xE:{1} xBcont:{2}".format(xE, xE, xBcont))
        iReturn[0] = xB-(xE-xB)/24
        iReturn[1] = (xE-xB)/12
        # 处理右上，获取Y的起点位置
        xBZ = 0
        xBcont = 0
        for x in range(0, 60):
            imgLine = imgRU[0:60, 59-x:60-x]
            # cv2.imshow("imgLine", imgLine)
            # cv2.waitKey(0)
            avg = np.mean(imgLine)
            # print(avg)
            if avg < 100:
                break
            if avg < 200 and avg > 100:
                isBlack = False
                for j in range(0, 60):
                    if imgLine[j][0] < 255:
                        xBcont = xBcont + 1
                        xBZ += j
                        isBlack = True
                    else:
                        if isBlack is True:
                            break
                # if xBcont == 0:
                #     yB = 11
                # else:
                #     yB = xBZ/xBcont
                # # print("yB:{0} XZ:{1} xBcont:{2}".format(yB, xBZ, xBcont))
                # break
        if xBcont == 0:
            yB = 11
        else:
            yB = xBZ/xBcont
        # print("yB:{0} XBZ:{1} xBcont:{2}".format(yB, xBZ, xBcont))
        # 处理右下，获取Y的终点位置
        xBZ = 0
        xBcont = 0
        for x in range(0, 40):
            imgLine = imgRD[0:40, 39-x:40-x]
            # cv2.imshow("imgLine", imgLine)
            # cv2.waitKey(0)
            avg = np.mean(imgLine)
            # print(avg)
            if avg < 200 and avg > 100:
                isBlack = False
                for j in range(0, 40):
                    if imgLine[39-j][0] < 255:
                        xBcont = xBcont + 1
                        xBZ += 39-j
                        isBlack = True
                    else:
                        if isBlack is True:
                            break
                # if xBcont == 0:
                #     yE = 251
                # else:
                #     yE = 240 + xBZ/xBcont
                # print("yE:{0} XZ:{1} xBcont:{2}".format(yE, xBZ, xBcont))
                # break
        if xBcont == 0:
            yE = 251
        else:
            yE = 240 + xBZ/xBcont
        # print("yE:{0} XBZ:{1} xBcont:{2}".format(yE, xBZ, xBcont))
        iReturn[2] = yB-(yE-yB)/24-(yE-yB)/12
        iReturn[3] = (yE-yB)/12
        # cv2.imshow("imgLU", imgLU)
        # cv2.imshow("imgRU", imgRU)
        # cv2.imshow("imgRD", imgRD)
        # cv2.waitKey(0)
        # print(iReturn)
        return iReturn

    def getBorW(self, img, x, y, startAndStep):
        '''
        判断一个区域内是黑色还是白色。
        '''
        yNew = int(startAndStep[2] + x*startAndStep[3])+3
        xNew = int(startAndStep[0] + y*startAndStep[1])+3
        yEnd = int(yNew+startAndStep[3])-7
        xEnd = int(xNew+startAndStep[1])-7
        # 获取到了单个码。白：255 黑：0
        # print("X:Y:Xe:Ye:{0} {1} {2} {3}".format(xNew, yNew, xEnd, yEnd))
        singleCode = img[yNew:yEnd, xNew:xEnd]
        # cv2.rectangle(img, (xNew, yNew), (xEnd, yEnd), (0, 255, 0), 1)
        # print("x:{0}  Y:{1}".format(x, y))
        avg = np.mean(singleCode)
        # cv2.imshow("img", img)
        # cv2.imshow("singleCode", singleCode)
        # print("avg:{0}  i:{1}  j:{2}".format(avg, x, y))
        # cv2.waitKey(0)
        if avg > 70:
            # print(0)
            # 白
            return 0
        else:
            # 黑
            # print(1)
            return 1

    def getSandartImg(self, codeArray):
        print("开始绘图>>>>>>>>>>>")
        # num = [[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        #        [1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1],
        #        [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
        #        [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
        #        [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
        #        [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1],
        #        [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0],
        #        [1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        #        [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        #        [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1],
        #        [1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0],
        #        [1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        #        [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        #        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        img = np.zeros([146, 146, 1], dtype=np.uint8)
        # img = [[255] * 136 for i in range(136)]
        for i in range(0, 146):
            for j in range(0, 146):
                img[i][j] = 255
        for i in range(0, 14):
            for j in range(0, 14):
                if codeArray[i][j] == 0:
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

    def imgRatated(self, img, jiaodu):
        '''
        图片旋转，按照给定的角度进行旋转。
        '''
        # print("jiaodu:{0}".format(jiaodu))
        height, width = img.shape[:2]
        M = cv2.getRotationMatrix2D((width / 2, height / 2), jiaodu, 1)
        dst = cv2.warpAffine(img, M, (width, height))
        return dst

    def getUprightImg(self, img):
        '''
        获取转正后的图像
        '''
        sgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dst = cv2.equalizeHist(sgray)
        # cv2.imshow("sgray", sgray)
        # cv2.imshow("dst", dst)
        ret, binary = cv2.threshold(dst, 170, 255,
                                    cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        # 闭操作。去黑点
        # binary = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        # binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel2)
        # cv2.imshow("binary", binary)
        # cv2.waitKey(0)
        # binary = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel2)
        # cv2.imshow("binary", binary)
        # cv2.waitKey(0)
        # 开操作。去白点
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel2)
        # binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel2)
        # cv2.imshow("b inary", binary)
        # cv2.waitKey(0)
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours.sort(key=cv2.contourArea, reverse=True)
        codeContour = contours[0]
        for i in range(0, len(contours)):
            (x, y), radius = cv2.minEnclosingCircle(contours[i])
            # print("x:{0} y:{1} R:{2}".format(x, y, radius))
            if (abs(x - 300) + abs(y - 300)) < 100 and radius > 170 and radius < 230:
                # print("Find code area")
                codeContour = contours[i]
                break
            # center = (int(x), int(y))
            # radius = int(radius)
            # cv2.circle(img, center, radius, (255, 0, 0), 2)
        # imgRd = self.imgRatated(img, hudu, PtXiangXian)
        rect = cv2.minAreaRect(codeContour)
        # 角度:[-90,0)
        angle = rect[2]
        imgRd = self.imgRatated(img, angle)
        binaryRd = self.imgRatated(binary, angle)
        contours, hierarchy = cv2.findContours(binaryRd, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours.sort(key=cv2.contourArea, reverse=True)
        codeContour = contours[0]
        for i in range(0, len(contours)):
            (x, y), radius = cv2.minEnclosingCircle(contours[i])
            # print("x:{0} y:{1} R:{2}".format(x, y, radius))
            if (abs(x - 300) + abs(y - 300)) < 100 and radius > 140 and radius < 200:
                # print("Find code area")
                codeContour = contours[i]
                break
            # center = (int(x), int(y))
            # radius = int(radius)
            # cv2.circle(img, center, radius, (255, 0, 0), 2)
        # imgRd = self.imgRatated(img, hudu, PtXiangXian)
        rect = cv2.minAreaRect(codeContour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # cv2.drawContours(imgRd, [box], 0, (0, 0, 255), 2)
        # cv2.imshow("imgRd", imgRd)
        # cv2.waitKey(0)
        # 中心坐标
        x, y = rect[0]
        # 长宽,总有 width>=height
        width, height = rect[1]
        # print("width:{0} height:{1}".format(width, height))
        x1 = int(x) - int(int(width)/2)  # 左上
        y1 = int(y) - int(int(height)/2)
        x2 = int(x) + int(int(width)/2)  # 右上
        # y2 = int(y) - int(int(height)/2)
        # x3 = int(x) + int(int(width)/2)  # 右下
        y3 = int(y) + int(int(height)/2)
        # x4 = int(x) - int(int(width)/2)  # 左下
        # y4 = int(y) + int(int(height)/2)
        # cv2.rectangle(imgRd, (x1, y1), (x1+20, y1+20), (0, 255, 0), 1, cv2.LINE_4)
        # cv2.rectangle(imgRd, (x2-20, y2), (x2, y2+20), (0, 255, 0), 1, cv2.LINE_4)
        # cv2.rectangle(imgRd, (x3-20, y3-20), (x3, y3), (0, 255, 0), 1, cv2.LINE_4)
        # cv2.rectangle(imgRd, (x4, y4-20), (x4+20, y4), (0, 255, 0), 1, cv2.LINE_4)
        imgUp = binaryRd[y1+10:y1+20, x1:x2]
        imgDown = binaryRd[y3-20:y3-10, x1:x2]
        imgLeft = binaryRd[y1:y3, x1+10:x1+20]
        imgRight = binaryRd[y1:y3, x2-20:x2-10]
        # imgUp1 = imgRd[y1:y1+20, x1:x2]
        # imgDown1 = imgRd[y3-20:y3, x1:x2]
        # imgLeft1 = imgRd[y1:y3, x1:x1+20]
        # imgRight1 = imgRd[y1:y3, x2-20:x2]
        # 获取两条定位边
        UD = 'd'
        if np.mean(imgUp) > np.mean(imgDown):
            UD = 'u'
        LR = 'l'
        if np.mean(imgRight) > np.mean(imgLeft):
            LR = 'r'
        if LR == 'l':
            if UD == 'd':
                JiaoZheng = 0
            else:
                JiaoZheng = 90
        else:
            if UD == 'd':
                JiaoZheng = 270
            else:
                JiaoZheng = 180
        # JiaoZheng = 270
        # minAvg = np.mean(imgUp)
        # if minAvg > np.mean(imgDown):
        #     JiaoZheng = 0
        #     minAvg = np.mean(imgDown)
        # if minAvg > np.mean(imgLeft):
        #     JiaoZheng = 90
        #     minAvg = np.mean(imgLeft)
        # if minAvg > np.mean(imgRight):
        #     JiaoZheng = 180
        imgRd = self.imgRatated(imgRd, JiaoZheng)
        # cv2.imshow("imgUpUp", imgUp)
        # cv2.imshow("imgDown", imgDown)
        # cv2.imshow("imgLeft", imgLeft)
        # cv2.imshow("imgRight", imgRight)
        # cv2.imshow("imgRd", imgRd)
        # cv2.imshow("binaryRd", binaryRd)
        # cv2.waitKey(0)
        return imgRd

    def cross_point(self, line1, line2):
        '''
        计算交点函数
        '''
        x1 = line1[0]  # 取四点坐标
        y1 = line1[1]
        x2 = line1[2]
        y2 = line1[3]

        x3 = line2[0]
        y3 = line2[1]
        x4 = line2[2]
        y4 = line2[3]

        k1 = (y2 - y1) * 1.0 / (x2 - x1)  # 计算k1,由于点均为整数，需要进行浮点数转化
        b1 = y1 * 1.0 - x1 * k1 * 1.0  # 整型转浮点型是关键
        if (x4 - x3) == 0:  # L2直线斜率不存在操作
            k2 = None
            b2 = 0
        else:
            k2 = (y4 - y3) * 1.0 / (x4 - x3)  # 斜率存在操作
            b2 = y3 * 1.0 - x3 * k2 * 1.0
        if k2 is None:
            x = x3
        else:
            x = (b2 - b1) * 1.0 / (k1 - k2)
        y = k1 * x * 1.0 + b1 * 1.0
        return [x, y]

    def isHaveAnyCode(self, img):
        '''
        简单的判断是否包含码。
        判断逻辑很简单，二值化以后，判断中心区域是否有“白点”
        '''
        sgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(sgray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        singleDMDM = binary[int(img.shape[0]/4):int(img.shape[0]/4*3), int(img.shape[1]/4):int(img.shape[1]/4*3)]
        # cv2.imshow("binary", binary)
        # cv2.waitKey(0)
        # cv2.imshow("singleDMDM", singleDMDM)
        # cv2.waitKey(0)
        avg = np.mean(singleDMDM)
        # print("avg:{0}".format(avg))
        if avg > 50:
            return True
        else:
            return False


DMCodeStandardisationer = DMCodeStandardisation()

if __name__ == '__main__':
    # for i in range(0, 5):
    #     for j in range(0, 5):
    #         print('{0}-{1}.jpg'.format(i, j))
    #         img = cv2.imread('{0}-{1}.jpg'.format(i, j))
    #         DMcodeImgImg = DMCodeStandardisation().GetDMCodeImg(img)
    # cv2.imshow("DMcodeImgImg", DMcodeImgImg)
    # cv2.waitKey(0)0-4.jpg 1-2
    img = cv2.imread('0-0.jpg')
    DMcodeImgImg = DMCodeStandardisation().GetDMCodeImg(img)
