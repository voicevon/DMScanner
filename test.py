import cv2

print(cv2.__version__)


class Camera:
    def __init__(self):
        self.__index = 0
        self.cam = type(cv2.VideoCapture(0))

    def set_index(self,my_index):
        self.__index = my_index

    def get_resolution(self):
        WIDTH = HIGH_VALUE
        HEIGHT = HIGH_VALUE

        self.__capture = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.__capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        self.__capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

        width = int(self.__capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.__capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        return width,height

    def start(self):
        # Set image resolution
        self.cam = cv2.VideoCapture(self.__index)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944)
        cv2.namedWindow("CameraId=" + str(self.__index))

    def capture_image(self):
        # cam = cv2.VideoCapture(camera_index)
        # # Set image resolution
        # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)
        # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944)
        # cv2.namedWindow("CameraId=" + str(camera_index))

        ret, frame = self.cam.read()
        img_name = "opencv_frame_{}.png".format(self.__index)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        # cam.release()


class CameraHub():

    def __init__(self):
        self.all_cameras = []

    def get_all_cameras(self):
        # checks the first 10 indexes.
        index = 0
        i = 10
        while i > 0:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                new_camera = Camera()
                self.all_cameras.append(new_camera)
                new_camera.set_index(index)
                cap.release()
            index += 1
            i -= 1
        # return allCameras
    
    def start_all_cameras(self):
        for cam in self.all_cameras:
            # print(cam)
            cam.start()

    def capture_all_images(self):
        for cam in self.all_cameras:
            cam.capture_image()

# arr = get_all_cameras()

if __name__ == '__main__':
    myHub = CameraHub()
    myCamera = Camera()
    cv2.namedWindow('aa')
    myHub.get_all_cameras()
    myHub.start_all_cameras()
    
    # print ('Count of cameras = ' , len(arr) , '  index id list=', arr)

    while True:
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            print ('start capturing')
            myHub.capture_all_images()

    cv2.destroyAllWindows()


