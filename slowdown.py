import cv2
from time import sleep

class Camera_hub():
    def __init__(self):
        self.all_index = []

    def get_all_cameras(self):
        # checks the first 10 indexes.
        index = 0
        i = 10
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


    def start_camera_and_grab_images(self):

        cam = cv2.VideoCapture(0)

        cv2.namedWindow("test")

        index = 0


        ret, frame = cam.read()
        if ret:
        # cv2.imshow("test", frame)

        # k = cv2.waitKey(1)
        # if k%256 == 27:
        #     # ESC pressed
        #     print("Escape hit, closing...")
        #     break
        # elif k%256 == 32:
        #     # SPACE pressed
            img_name = "opencv_frame_{}.png".format(index)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            # img_counter += 1
            # cv2.waitKey(1000)
        else:
            print("failed to grab frame")


myhub = Camera_hub()
myhub.get_all_cameras()

while True:
    cv2.namedWindow('aa')
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        myhub.start_camera_and_grab_images()


cv2.destroyAllWindows()