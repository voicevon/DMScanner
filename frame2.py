import cv2

class Camera():
    def __init__(self,index,capturer):
        self.index = 0
        self.capturer = capturer



class CameraHub():

    def __init__(self):
        self.all_cameras = []

    def get_all_cameras(self):
        # checks the first 10 indexes.
        index = 0
        i = 10
        while i > 0:
            print("=========================== trying to find one.")
            cap = cv2.VideoCapture(index)
            cap.set(cv2.CAP_PROP_FPS, 1)

            if cap.read()[0]:
                print("get a new camera")

                new_camera = Camera(index=index, capturer=cap )
                self.all_cameras.append(new_camera)
                # cap.release()
                print("-----------------added index=",index)
            index += 1
            i -= 1
            print('')
            print('')

    def start(self):
        # create video windows
        for this_camera in self.all_cameras:
            cv2.namedWindow(str(this_camera.index))
            this_camera.capturer = cv2.VideoCapture(this_camera.index)

        # monitor and capture image to files when press space key.
        while True:
            for this_camera in self.all_cameras:
                ret, frame = this_camera.capturer.read()
                if not ret:
                    print("failed to grab frame")
                    break
                cv2.imshow(str(this_camera.index), frame)

                k = cv2.waitKey(1)
                if k%256 == 27:
                    # ESC pressed
                    print("Escape hit, closing...")
                    break
                elif k%256 == 32:
                    # SPACE pressed
                    img_name = "opencv_frame_{}.png".format(this_camera.index)
                    cv2.imwrite(img_name, frame)
                    print("{} written!".format(img_name))
                    img_counter += 1


if __name__ == '__main__':
    my_hub = CameraHub()
    my_hub.get_all_cameras()
    my_hub.start()

# cam.release()

# cv2.destroyAllWindows()