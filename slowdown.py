import cv2
from time import sleep

class Camera_hub():
    def __init__(self):
        self.all_index = []

    def get_all_cameras(self):
        # checks the first 7 indexes.
        index = 0
        i = 7
        while i > 0:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                print("get a new camera.  index = ", index)
                self.all_index.append(index)
                cap.release()
            index += 1
            i -= 1

        print('=========================================')
        print('get_all_cameras result: ', self.all_index)


    def start_camera_and_grab_images(self,counter):
        WIDTH = 2592
        HEIGHT = 1944
        center = (WIDTH / 2, HEIGHT / 2)
        
        scale = 1.0

        for index in self.all_index:
            this_cam = cv2.VideoCapture(index)
            this_cam.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
            this_cam.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
            cv2.namedWindow(str(index))

            ret, frame = this_cam.read()
            if ret:
                if(index == 4 or index == 6):
                    # rotate 180 degree
                    M = cv2.getRotationMatrix2D(center, 180, scale)
                    frame = cv2.warpAffine(frame, M, (WIDTH, HEIGHT)) 
                
                cv2.imshow(str(index),frame)
                # write to file
                img_name = './images/f_' + str(counter) + '_'+ str(index) + '.png'
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))

            else:
                print("failed to grab frame")
            # prepare for next camera
            this_cam.release
            cv2.waitKey(5)   # zero means for ever !!!
        print ('--------------------------------------------------  All images have been writen' )

myhub = Camera_hub()
myhub.get_all_cameras()

cv2.namedWindow('splash')

counter = 0
while True:
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        myhub.start_camera_and_grab_images(counter)
        cv2.destroyWindow('splash')
        counter += 1

cv2.destroyAllWindows()