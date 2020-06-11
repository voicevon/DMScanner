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
            return "None"
        # 第一步，放大图像××××××××××××××××××××××××××××××××××××××××××××××××××××
        height, width = img.shape[:2]
        img = self.SuoFang(img, width * 10, height * 10)
        # 第二步，图像转正×××××××××××××××××××××××××××××××××××××××××××××××××××××××
        imgUpright = self.getUprightImg(img)
        cv2.imshow("imgUpright", imgUpright)
        cv2.waitKey(0)
        # 第三步，二维码图像截取
        imgCode = self.getCodeImg(imgUpright)
        # cv2.imshow("imgCode", imgCode)
        # cv2.waitKey(0)
        # 第四步，直方图处理
        StandardImg = self.SuoFang(imgCode, 280, 280)
        sgray = cv2.cvtColor(StandardImg, cv2.COLOR_BGR2GRAY)
        dst = cv2.equalizeHist(sgray)
        ThresholdValue = [100, 130, 120]
        for i in range(0, 3):
            # 第五步，图像识别为数组。
            codeArray = self.getCodeArrayByImg(dst, ThresholdValue[i])
            # 第六步，数组生成标准DMCode图像
            imgR = self.getSandartImg(codeArray)
            # cv2.imwrite("sss.png", imgR)
            # 第七步，标准图识别
            iCode = DMDecoder.decode(imgR)
            print("ThresholdValue:{0}".format(ThresholdValue[i]))
            print(iCode)
            if iCode != "Error":
                return iCode
        return "Error"

    def getCodeImg(self, img):
        '''
        获取DMcode的图像区域，需要截取出准确的图像。
        '''
        sgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # dst = cv2.equalizeHist(sgray)
        # cv2.imshow("sgray", sgray)
        # cv2.imshow("dst", dst)
        ret, binaryRd = cv2.threshold(sgray,  90, 255, cv2.THRESH_BINARY)
        # cv2.imshow("binaryRd", binaryRd)
        # cv2.waitKey(0)
        contours, hierarchy = cv2.findContours(binaryRd, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours.sort(key=cv2.contourArea, reverse=True)
        # for i in range(0, len(contours)):
        #     print(cv2.contourArea(contours[i]))
        x, y, w, h = cv2.boundingRect(contours[0])  # 将轮廓分解为识别对象的左上角坐标和宽、高
        # 在图像上画上矩形（图片、左上角坐标、右下角坐标、颜色、线条宽度）
        print("W:{} H:{}".format(w, h))
        CodeImg = img[y+3:y+3+w, x:x+w]
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
        ret, binaryRd = cv2.threshold(img,  ThresholdValue, 255, cv2.THRESH_BINARY)
        binaryRd = 255 - binaryRd
        # cv2.imshow("binaryRd", binaryRd)
        # cv2.imshow("dst", dst)
        # cv2.imwrite("daa.png", binaryRd)
        # cv2.waitKey(0)
        # 为了分割更准确，要找到凸点。也就是定位点。
        # 然后通过定位点，确定X、Y的起点以及步长。
        xyAndStep = self.getXYandStep(binaryRd)
        print("xyAndStep:{0}".format(xyAndStep))
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

        for i in range(0, 14):
            print(num_list[i])
        return num_list

    def getXYandStep(self, img):
        '''
        确定图像的网格起点以及步长
        '''
        iReturn = [0.0, 0.0, 0.0, 0.0]
        imgLU = img[0:40, 0:40]
        imgRU = img[0:40, 240:280]
        imgRD = img[240:280, 240:280]
        # cv2.imshow("img", img)
        # cv2.imshow("imgLU", imgLU)
        # cv2.imshow("imgRU", imgRU)
        # cv2.imshow("imgRD", imgRD)
        xB = 0
        xE = 0
        yB = 0
        yE = 0
        for x in range(0, 40):
            imgLine = imgLU[x:x+1, 0:40]
            # cv2.imshow("imgLine", imgLine)
            # cv2.waitKey(0)
            avg = np.mean(imgLine)
            # print(avg)
            if avg < 255:
                xBZ = 0
                xBcont = 0
                for j in range(0, 40):
                    if imgLine[0][j] < 255:
                        xBcont = xBcont + 1
                        xBZ += j
                if xBcont == 0:
                    xB = 11
                else:
                    xB = xBZ/xBcont
                # print("XB:{0} XZ:{1} xBcont:{2}".format(xB, xBZ, xBcont))
                break
        for x in range(0, 40):
            imgLine = imgRU[x:x+1, 0:40]
            # cv2.imshow("imgLine", imgLine)
            # cv2.waitKey(0)
            avg = np.mean(imgLine)
            # print(avg)
            if avg < 255:
                xBZ = 0
                xBcont = 0
                for j in range(0, 40):
                    if imgLine[0][j] < 255:
                        xBcont = xBcont + 1
                        xBZ += j
                if xBcont == 0:
                    xE = 251
                else:
                    xE = 240 + xBZ/xBcont
                # print("xE:{0} XZ:{1} xBcont:{2}".format(xE, xBZ, xBcont))
                break
        iReturn[0] = xB-(xE-xB)/24
        iReturn[1] = (xE-xB)/12
        for x in range(0, 40):
            imgLine = imgRU[0:40, 39-x:40-x]
            # cv2.imshow("imgLine", imgLine)
            # cv2.waitKey(0)
            avg = np.mean(imgLine)
            # print(avg)
            if avg < 255:
                xBZ = 0
                xBcont = 0
                for j in range(0, 40):
                    if imgLine[j][0] < 255:
                        xBcont = xBcont + 1
                        xBZ += j
                if xBcont == 0:
                    yB = 11
                else:
                    yB = xBZ/xBcont
                # print("yB:{0} XZ:{1} xBcont:{2}".format(yB, xBZ, xBcont))
                break
        for x in range(0, 40):
            imgLine = imgRD[0:40, 39-x:40-x]
            # cv2.imshow("imgLine", imgLine)
            # cv2.waitKey(0)
            avg = np.mean(imgLine)
            # print(avg)
            if avg < 255:
                xBZ = 0
                xBcont = 0
                for j in range(0, 40):
                    if imgLine[j][0] < 255:
                        xBcont = xBcont + 1
                        xBZ += j
                if xBcont == 0:
                    yE = 251
                else:
                    yE = 240 + xBZ/xBcont
                # print("yE:{0} XZ:{1} xBcont:{2}".format(yE, xBZ, xBcont))
                break
        iReturn[2] = yB-(yE-yB)/24-(yE-yB)/12
        iReturn[3] = (yE-yB)/12
        # cv2.waitKey(0)
        # print(iReturn)
        return iReturn

    def getBorW(self, img, x, y, startAndStep):
        '''
        判断一个区域内是黑色还是白色。
        '''
        yNew = int(startAndStep[2] + x*startAndStep[3])
        xNew = int(startAndStep[0] + y*startAndStep[1])
        yEnd = int(yNew+startAndStep[3])
        xEnd = int(xNew+startAndStep[1])
        # 获取到了单个码。白：255 黑：0
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

    def imgRatated(self, img, hudu, P1):
        '''
        图片旋转，按照给定的角度进行旋转。同时，根据交点的位置不同，会有角度补偿。
        交点位置顺序为：左下，左上，右上，右下
        '''
        JiaoDu = hudu * 180 / np.pi
        print("hudu:{1} JiaoDu Befor:{0}".format(JiaoDu, hudu))
        if P1 == 3:
            JiaoDu = JiaoDu + 180
        elif P1 == 2:
            JiaoDu = JiaoDu + 90
        elif P1 == 1:
            JiaoDu = JiaoDu + 0
        else:
            JiaoDu = JiaoDu + 270
        print("jiaodu:{0}".format(JiaoDu))
        height, width = img.shape[:2]
        M = cv2.getRotationMatrix2D((width / 2, height / 2), JiaoDu, 1)
        dst = cv2.warpAffine(img, M, (width, height))
        return dst

    def getUprightImg(self, img):
        '''
        获取转正后的图像
        '''
        sgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dst = cv2.equalizeHist(sgray)
        cv2.imshow("sgray", sgray)
        cv2.imshow("dst", dst)
        ret, binary = cv2.threshold(dst, 0, 255,
                                    cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        edges = cv2.Canny(binary, 150, 250, apertureSize=3)
        cv2.imshow("edges", edges)
        cv2.waitKey(0)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
        if lines is None:
            print("not find any line")
            return img
        hudu = 0
        line1 = [0, 0, 0, 0]
        line2 = [0, 0, 0, 0]
        for line in lines:
            rho = line[0][0]  # 第一个元素是距离rho
            theta = line[0][1]  # 第二个元素是角度theta
            print("rho:{0}  theta:{1}".format(rho, theta))
            if (theta < (np.pi / 4.0)) or (theta > (3. * np.pi / 4.0)):  # 垂直直线
                pt1 = (int(rho / np.cos(theta)), 0)  # 该直线与第一行的交点
                # 该直线与最后一行的焦点
                pt2 = (int(
                    (rho - img.shape[0] * np.sin(theta)) / np.cos(theta)),
                       img.shape[0])
                cv2.line(img, pt1, pt2, (255), 1)  # 绘制一条白线
                # hudu = theta
                line2[0] = pt1[0]
                line2[1] = pt1[1]
                line2[2] = pt2[0]
                line2[3] = pt2[1]
            else:  # 水平直线
                pt1 = (0, int(rho / np.sin(theta)))  # 该直线与第一列的交点
                # 该直线与最后一列的交点
                pt2 = (img.shape[1],
                       int((rho - img.shape[1] * np.cos(theta)) /
                           np.sin(theta)))
                cv2.line(img, pt1, pt2, (255), 1)  # 绘制一条直线
                line1[0] = pt1[0]
                line1[1] = pt1[1]
                line1[2] = pt2[0]
                line1[3] = pt2[1]
                hudu = theta
        cv2.imshow("houghline", img)
        cv2.waitKey(0)
        PtC = self.cross_point(line1, line2)
        print("PtC:{0}".format(PtC))
        PtXiangXian = 0
        if PtC[0] < img.shape[1]/2:
            if PtC[1] > img.shape[0]/2:
                PtXiangXian = 0
            else:
                PtXiangXian = 1
        else:
            if PtC[1] < img.shape[0]/2:
                PtXiangXian = 2
            else:
                PtXiangXian = 3
        print("PtXiangXian:{0}".format(PtXiangXian))
        imgRd = self.imgRatated(img, hudu, PtXiangXian)
        # cv2.imshow("imgRd", imgRd)
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
        avg = np.mean(singleDMDM)
        # print("avg:{0}".format(avg))
        if avg > 50:
            return True
        else:
            return False


DMCodeStandardisationer = DMCodeStandardisation()

if __name__ == '__main__':
    img = cv2.imread('c0.png')
    DMcodeImgImg = DMCodeStandardisation().GetDMCodeImg(img)
    # cv2.imshow("DMcodeImgImg", DMcodeImgImg)
    # cv2.waitKey(0)
