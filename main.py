import cv2

class Camera():
    
    def __init__(self):
        pass
    
    def capture_image(self,index):
        cam = cv2.VideoCapture(index)
        cv2.namedWindow("test" + str(index))

        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            return

        cv2.imshow("test", frame)
        img_name = "opencv_frame_{}.png".format(index)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))



if __name__ == '__main__':
    print('cv2.__version__', cv2.__version__)
    

    myCamera = Camera()
    cv2.namedWindow("test")

    while True:
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            myCamera.capture_image(0)
