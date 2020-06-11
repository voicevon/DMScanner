#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np


class imgCut:
    '''
    图像切割类，负责将原始图片切割成为一个个的小图像
    '''
    def cutImgToList(self, img0, img1, img2, img3):
        '''
        图像切割函数，负责将原始的传入图像，切割成为100个顺序的小图像，并将图像返回。
        理论上来说，每张图像都包含所需要的5×5个需要识别的位置。其中，img0包括前5行前5列，img1包括前5行后5列，以此类推
        注意：接收的图像已经经过“矫正处理”。
        '''
        img_list = []
        img0_new = self.getFiveMultiplyFive(img0, 0)
        img1_new = self.getFiveMultiplyFive(img1, 1)
        img2_new = self.getFiveMultiplyFive(img2, 2)
        img3_new = self.getFiveMultiplyFive(img3, 3)
        # cv2.imshow("img0", img0)
        # cv2.imshow("img0_new", img0_new)
        # cv2.imshow("img1_new", img1_new)
        # cv2.imshow("img2_new", img2_new)
        # cv2.imshow("img3_new", img3_new)
        # cv2.waitKey(0)
        for i in range(0, 5):
            img_list.append(img0_new[i])
            img_list.append(img1_new[i])
        for i in range(0, 5):
            img_list.append(img2_new[i])
            img_list.append(img3_new[i])
        return img_list

    def getFive(self, img, line):
        '''
        方法暂时废除了，考虑到有畸变。
        '''
        list_five = []
        height, width = img.shape[:2]
        for i in range(0, 5):
            # 在图像上画上矩形（图片、左上角坐标、右下角坐标、颜色、线条宽度）
            cutimg = img[int(height / 5 * line):int(height / 5 * (line + 1)),
                         int(width / 5 * i):int(width / 5 * (i + 1))]
            # cv2.rectangle(img, (int(width/5*i), int(height/5*line)), (int(width/5*(i+1)), int(height/5*(line+1))), (0, 255,), 3)
            list_five.append(cutimg)
            # cv2.imshow("img", img)
            # cv2.imshow("cutimg", cutimg)
            # cv2.waitKey(0)
        return list_five

    def getFiveMultiplyFive(self, img, num):
        height, width = img.shape[:2]
        # cv2.namedWindow('gray', 0)
        # cv2.imshow("gray", img)
        # cv2.waitKey(0)
        if num == 0:
            img = img[0:height-50, 400:2200]
        if num == 1:
            img = img[0:height-50, 300:2200]
        if num == 2:
            img = img[50:height, 300:2200]
        if num == 3:
            img = img[0:height, 300:2200]
        # cv2.namedWindow('imgnew', 0)
        # cv2.imshow("imgnew", img)
        # cv2.waitKey(0)
        list_Return = []
        # =================灰度处理======================
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.namedWindow('gray', 0)
        # cv2.imshow("gray", gray)
        # cv2.waitKey(0)
        # ret, thresh = cv2.threshold(gray, 150, 255,
        #                             cv2.THRESH_BINARY)
        # cv2.namedWindow('thresh', 0)
        # cv2.imshow("thresh", thresh)
        # cv2.waitKey(0)
        # cv2.namedWindow('binary', 0)
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        # kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        # 闭操作。去黑点
        # binary = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        # binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel2)
        # cv2.imshow("binary", binary)
        # cv2.waitKey(0)
        # binary = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel2)
        # cv2.imshow("binary", binary)
        # cv2.waitKey(0)
        # 开操作。去白点
        # binary = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        # binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel2)
        # binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        # 闭操作。去黑点
        # binary = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel2)
        # cv2.imshow("binary", binary)
        # cv2.waitKey(0)
        # ============颜色处理========================
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
        Min_BoardColor = np.array([0, 30, 0])  # 要识别的颜色的下限
        Max_BoardColor = np.array([180, 225, 180])  # 要识别的颜色的上限
        # mask是把HSV图片中在颜色范围内的区域变成白色，其他区域变成黑色
        mask = cv2.inRange(HSV, Min_BoardColor, Max_BoardColor)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        # 开操作。去白点
        # binary = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        # binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel2)
        # binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        # 闭操作。去黑点
        binary = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        # cv2.namedWindow('mask', 0)
        # cv2.imshow("mask", binary)
        # cv2.waitKey(0)
        # ==================图像反转=============================
        # binaryC = 255 - mask
        # cv2.namedWindow('binaryC', 0)
        # cv2.imshow("binaryC", binaryC)
        # cv2.waitKey(0)
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)
        iCunt = 0
        listSix = []
        listAll = []
        for i in range(0, len(contours)):
            if cv2.contourArea(contours[i]) < 30000: #or cv2.contourArea(contours[i]) > 40000:
                continue
            # print(cv2.contourArea(contours[i]))
            M = cv2.moments(contours[i])  # 计算第一条轮廓的各阶矩,字典形式
            if M["m00"] == 0:
                continue
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])
            # print("x:{0} y:{1}".format(center_x, center_y))
            Cpoint = (center_x, center_y)
            listSix.append(Cpoint)
            # print("iCunt % 6 = {0}".format(iCunt % 6))
            # print("listSix::>>{0}".format(listSix))
            if iCunt % 6 == 4:
                # print(listSix)
                listSix.sort()
                # print(listSix)
                # listSix.pop()
                # print(listSix)
                listAll.insert(0, listSix)
                listSix = []
                iCunt = 0
                # continue
            else:
                iCunt = iCunt + 1
            # cv2.drawContours(img, contours[i], 0, (0, 255, 0), 1)  # 绘制轮廓，填充
            # cv2.circle(img, (center_x, center_y), 7, (0, 0, 213), -1)  # 绘制中心点
            # cv2.rectangle(img, (center_x-90, center_y-90), (center_x+90, center_y+90), (134, 2, 34), 1)
            # font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(img, str(cv2.contourArea(contours[i])), (center_x, center_y), font, 1, (0, 255, 255), 2)
        # cv2.imshow("gray", gray)
        # listSix.sort()
        # listAll.insert(0, listSix)
        # cv2.namedWindow('img', 0)
        # cv2.imshow("img", img)
        # cv2.imshow("thresh", thresh)
        # cv2.imshow("binary", binary)
        # cv2.imshow("binaryCbinaryC", binaryC)
        # cv2.waitKey(0)
        for i in range(0, 5):
            # print(listAll[i])
            imgFive = []
            for j in range(0, 5):
                imgOne = img[listAll[i][j][1]-90:listAll[i][j][1]+90, listAll[i][j][0]-90:listAll[i][j][0]+90]
                imgFive.append(imgOne)
                cv2.imwrite("{0}-{1}.jpg".format(i, j), imgOne)
                # cv2.imshow("imgOne", imgOne)
                # cv2.waitKey(0)
            list_Return.append(imgFive)
        return list_Return


imgCuter = imgCut()

if __name__ == '__main__':
    img = cv2.imread('f_7_0.png')
    CuttedImg = imgCut().getFiveMultiplyFive(img, 2)
    # cv2.imshow("CuttedImg", CuttedImg)
    # cv2.waitKey(0)
