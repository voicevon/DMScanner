#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
from pylibdmtx.pylibdmtx import decode


class DMDecode:
    '''
    DM编码识别。将包含DM编码的二维码图片信息识别并返回。
    识别失败或者没有编码，则返回空empty。
    DM编码识别使用pylibdmtx库。详见：https://pypi.org/project/pylibdmtx/
    '''
    def decode(self, img):
        # imgcv = cv2.imread(img, cv2.IMREAD_UNCHANGED)
        # gray = cv2.cvtColor(imgcv, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("gray", gray)
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # ret, thresh = cv2.threshold(img, 0, 255,
        #                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # # cv2.imshow("thresh", thresh)

        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',end = '    ')
        print(img.shape[0])
        cv2.imwrite('error_img.jpg',img)
        info = decode(img)
        print('bbbbbbbbbbbbbbbbbbbbbbb')
        if info.__len__() == 0:
            print("Error : Len == 0")
            return "Error"
        print('ccccccccccccccccccccccccc')
        try:
            msg = info[0].data.decode()
        except BaseException:
            print("Error : exception")
            return "Error"

        print('ffffffffffffffffffffffffffffff')
        return msg


DMDecoder = DMDecode()

if __name__ == '__main__':
    img = cv2.imread('sss.png')
    msg = DMDecode().decode(img)
    print(msg)
