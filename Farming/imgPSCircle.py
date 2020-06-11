#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class ImgPSCircle:
    '''
    图片处理。目的是将原始图像处理成一个个可识别图像。
    需要注意的是，目前考虑“空”处理。也就是如果有空位置，返回“empty”。
    '''
    def imgPS(self, url):
        # 读取原始图像
        img = cv2.imread(url, 1)
        # cv2.imshow("img", img)
        # cv2.waitKey(0)
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
        Min_BoardColor = np.array([0, 0, 0])  # 要识别棋盘的颜色的下限
        Max_BoardColor = np.array([180, 225, 225])  # 要识别棋盘的颜色的上限
        # mask是把HSV图片中在颜色范围内的区域变成白色，其他区域变成黑色
        mask = cv2.inRange(HSV, Min_BoardColor, Max_BoardColor)
        '''
        第一个参数：image 8-bit的单通道灰度图；
        第二个参数：method 使用的方法，当前可以使用的方法只有CV_HOUGH_GRADENT
        第四个参数：dp 累加器分辨率到图像分辨率的反比例。例如：如果dp=1，累加器有着和输入图像一样的分辨率；如果dp=2，累加器有着输入图像的width和height一半的值；
        第五个参数：minDist 介于检测到的圆的中心的最小距离。如果这个参数太小，在真的圆形周围会检测到很多假的圆。如果太大，一些圆会被miss掉
        第六个参数：param1 canny边缘检测高阈值。当使用CV_HOUGH_GRADIENT，这个参数表示传递给canny检测器的高限阈值，（低限阈值是这个值的一半）。这个值越大检测圆边界时，要求的亮度梯度越大，一些灰灰的不明显的边界就会略去。
        第七个参数：param2 圆心检测阈值，在CV_HOUGH_GRADIENT中，这个参数是在检测阶段中圆心的累加器阈值，这个值越小，越多假的圆会被检测到，（对应于越大的累加值，越先返回，也就是进行排序，累加值越大，说明圆的可能性越高）
        后两个参数：允许检测到的圆的最大和最小半径
        '''
        fondcircles = cv2.HoughCircles(mask,
                                       cv2.HOUGH_GRADIENT,
                                       1,
                                       100,
                                       param1=100,
                                       param2=30,
                                       minRadius=30,
                                       maxRadius=70)
        if fondcircles is not None:
            circle = np.uint16(np.around(fondcircles))
            # print(circle)
            for i in circle[0, :]:
                cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 1)
                
        cv2.imshow("mask", mask)
        cv2.imshow("circle", img)
        cv2.waitKey(0)


if __name__ == '__main__':
    imgsimgs = ImgPSCircle().imgPS('a4.png')
