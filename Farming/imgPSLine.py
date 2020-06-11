#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class ImgPS:
    '''
    图片处理。目的是将原始图像处理成一个个可识别图像。
    需要注意的是，目前考虑“空”处理。也就是如果有空位置，返回“empty”。
    '''
    def imgPS(self, url):
        # 读取原始图像
        img = cv2.imread(url, 1)
        # cv2.imshow("img", img)
        # cv2.waitKey(0)
        # 灰度处理
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("gray", gray)
        # cv2.waitKey(0)
        gaus = cv2.GaussianBlur(gray, (3, 3), 0)
        # cv2.imshow("gaus", gaus)
        edges = cv2.Canny(gaus, 50, 150, apertureSize=3)
        # cv2.imshow("edges", edges)
        # minLineLength = 1000
        # maxLineGap = 50
        lines = cv2.HoughLines(edges, 1, np.pi/180, 500)
        for line in lines:
            rho = line[0][0]  # 第一个元素是距离rho
            theta = line[0][1]  # 第二个元素是角度theta
            # print (rho)
            # print (theta)
            if (theta < (np.pi/4.0)) or (theta > (3.*np.pi/4.0)):  # 垂直直线
                pt1 = (int(rho/np.cos(theta)), 0)               # 该直线与第一行的交点
                # 该直线与最后一行的焦点
                pt2 = (int((rho-img.shape[0]*np.sin(theta))/np.cos(theta)), img.shape[0])
                cv2.line(img, pt1, pt2, (255))             # 绘制一条白线
            else:                                                  # 水平直线
                pt1 = (0, int(rho/np.sin(theta)))               # 该直线与第一列的交点
                # 该直线与最后一列的交点
                pt2 = (img.shape[1], int((rho-img.shape[1]*np.cos(theta))/np.sin(theta)))
                cv2.line(img, pt1, pt2, (255), 1)           # 绘制一条直线
        cv2.imshow("houghline", img)
        cv2.waitKey(0)
        return img


if __name__ == '__main__':
    imgsimgs = ImgPS().imgPS('1.jpg')
    # cmd =
