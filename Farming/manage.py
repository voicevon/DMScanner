#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
from imgCut import imgCuter
from DMCodeStandardisation import DMCodeStandardisationer



if __name__ == '__main__':
    '''
    二维码识别思路及过程：
    1、获取原始图片。
    2、原始图片切割成一系列单张小图片（可能包含二维码）。
    2、二维码解析成字符串，可能是Empty、编码、Error。
    3、解析字符串组成识别矩阵。
    注：
    1、二维码与位置的对应关系暂由manage负责处理。
    2、图像处理过程中，会返回所有位置的图像，不管该位置是否有二维码（暂定）。
    '''
    mode = 3     # 1 Calibrate camera  2 = debug. 3 = Release
    debug_index_string = "0"

    if mode == 1:
        pass

    if mode == 3:
        from slowdown import Camera_hub
        myhub = Camera_hub()
        # myhub.get_all_cameras()
        myhub.set_all_cameras()
        counter = 0

    while True:
        acmd = input("Press Enter to 开始检测(q退出):")
        if acmd == "q":
            print("系统退出!!!!!!!!!!!!!!!!!!!!!!!")
            break
        
        if mode == 3:
            image_files = myhub.start_camera_and_grab_images(counter)
            print(image_files)
            cv2.destroyWindow('splash')

        print("开始检测>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        code_list = ["NoAnalysis"] * 100
        # for i in range(0, 100):
        #     print("i:{0}  {1}".format(i, code_list[i]))
        # 读取原始图片，并将原始图片进行矫正
        # ===============矫正处理===========
        # 图像切割
        # ===============切割处理===========
        # 4 6 0 2
        if mode == 3:
            # Img0 = cv2.imread("images/f_" + str(counter) + "_4.png")
            # Img2 = cv2.imread("images/f_" + str(counter) + "_6.png")
            # Img1 = cv2.imread("images/f_" + str(counter) + "_0.png")
            # Img3 = cv2.imread("images/f_" + str(counter) + "_2.png")
            
            # For PC05
            Img0 = cv2.imread("images/f_" + str(counter) + "_4.png")   # Img0 is in top-right from topview
            Img1 = cv2.imread("images/f_" + str(counter) + "_6.png")   # Img1 is in top-left from topview 
            Img2 = cv2.imread("images/f_" + str(counter) + "_0.png")   # Img2 is in bottom-left from topview
            Img3 = cv2.imread("images/f_" + str(counter) + "_2.png")   # Img3 is in bottom-right from topview
            # For Thinkpad R400
            # Img0 = cv2.imread("images/f_" + str(counter) + "_6.png")
            # Img1 = cv2.imread("images/f_" + str(counter) + "_4.png")
            # Img2 = cv2.imread("images/f_" + str(counter) + "_4.png")
            # Img3 = cv2.imread("images/f_" + str(counter) + "_4.png")
        if mode == 2:
            Img0 = cv2.imread("images/f_" + debug_index_string + "_4.png")
            Img2 = cv2.imread("images/f_" + debug_index_string + "_6.png")
            Img1 = cv2.imread("images/f_" + debug_index_string + "_0.png")
            Img3 = cv2.imread("images/f_" + debug_index_string + "_2.png")
       
        imgList = imgCuter.cutImgToList(Img0, Img1, Img2, Img3)

        print(imgList.__len__())
        for i in range(0, imgList.__len__()):
            for j in range(0, imgList[i].__len__()):
                # if (i * imgList[i].__len__() + j) == 84:
                # print("111111111111111111111111111111111111")
                # cv2.imwrite("b.jpg", imgList[i][j])
                code_list[i * imgList[i].__len__() + j] = DMCodeStandardisationer.GetDMCodeImg(imgList[i][j])
                print("i:{0}  {1}".format(i * imgList[i].__len__() + j, code_list[i * imgList[i].__len__() + j]))
                # print("222222222222222222222222222222222222")
        for i in range(0, 10):
            # print("{0}  {1}  {2}  {3}  {4}  {5}  {6}  {7}  {8}  {9}".format(
            #     code_list[i * 10], code_list[i * 10 + 1], code_list[i * 10 + 2],
            #     code_list[i * 10 + 3], code_list[i * 10 + 4],
            #     code_list[i * 10 + 5], code_list[i * 10 + 6],
            #     code_list[i * 10 + 7], code_list[i * 10 + 8],
            #     code_list[i * 10 + 9]))

            print("{0}  {1}  {2}  {3}  {4}  {5}  {6}  {7}  {8}  {9}".format(
                code_list[i * 10 + 9], code_list[i * 10 + 8],
                code_list[i * 10 + 7], code_list[i * 10 + 6],
                code_list[i * 10 + 5], code_list[i * 10 + 4],
                code_list[i * 10 + 3], code_list[i * 10 + 2],
                code_list[i * 10 + 1], code_list[i * 10]))
        if mode == 3:
            counter += 1
