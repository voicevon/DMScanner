#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zxing


class DMDecodeDMDecodeZ:
    '''
    DM编码识别。将包含DM编码的二维码图片信息识别并返回。
    识别失败或者没有编码，则返回空empty。
    DM编码识别使用zxing库。详见：https://github.com/dlenski/python-zxing
    '''
    def decode(self, img):
        reader = zxing.BarCodeReader()
        barcode = reader.decode(img, True, "DATA_MATRIX")  # BarcodeFormat.DATA_MATRIX QR_CODE
        return barcode


if __name__ == '__main__':
    msg = DMDecodeDMDecodeZ().decode('none.png')
    print(msg)
