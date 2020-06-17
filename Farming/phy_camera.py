class phy_camera:

    def __init__(self):
        # self.need_to_flip = False
        # self.opencv_id = 0
        # self.quadrant_position = 1
        self.setup(1)
        self.setup(2)
        self.setup(3)
        self.setup(4)

    def setup(self, quadrant_position):
        self.quadrant_position = quadrant_position

        if quadrant_position == 1:
            self.opencv_id = 0
            self.need_to_flip = False

        if quadrant_position == 2:
            self.opencv_id = 2
            self.need_to_flip = False

        if quadrant_position == 3:
            self.opencv_id = 4
            self.need_to_flip = True

        if quadrant_position == 4:
            self.opencv_id = 6
            self.need_to_flip = True
