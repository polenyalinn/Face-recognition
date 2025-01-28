import cv2
from abc import ABC

import numpy as np


class Frame_Grab(ABC):
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    regions = [None, None, None]

    def grab_new_frame(self):
        if not self.cap:
            self.regions = [None, None, None]
            return

        # Capture the current frame
        ret, frame = self.cap.read()
        if not ret:
            self.regions = [None, None, None]
            return

        # Get the size of the frame.
        height, width = frame.shape[0], frame.shape[1]

        # BGR 2 HSV
        cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Divide the regions. (-+5 for the lines.)
        self.regions[0] = frame[0:height, 0:int(width / 3)]
        self.regions[1] = frame[0:height, int(width / 3):int(2 * width / 3)]
        self.regions[2] = frame[0:height, int(2 * width / 3):width]

        return frame

    def release_cap(self):
        self.cap.release()
        self.cap = None

        # Close all active windows
        cv2.destroyAllWindows()

    @staticmethod
    def combine_regions(region_one, region_two, region_three):
        # Padding for the regions.
        padding = np.zeros((region_one.shape[0], 3, 3), np.uint8)
        padding.fill(255)

        return np.concatenate((
            region_one,
            padding,
            region_two,
            padding,
            region_three
        ),
            axis=1
        )


class Slider_Data(ABC):
    __slider_data = {}

    def Set_Slider_Data(self, id, data):
        self.__slider_data[id] = data

    def Get_Slider_Data(self, data):
        return self.__slider_data


class Region1(Frame_Grab, Slider_Data):
    def __init__(self):
        super(Frame_Grab, self).__init__()

    def get_region_frame(self):
        self.grab_new_frame()
        return self.regions[0]

    def Pixel_Calculation(self):
        pass


class Region2(Frame_Grab, Slider_Data):
    def __init__(self):
        super(Frame_Grab, self).__init__()

    def get_region_frame(self):
        self.grab_new_frame()
        return self.regions[1]

    def Pixel_Calculation(self):
        pass


class Region3(Frame_Grab, Slider_Data):
    def __init__(self):
        super(Frame_Grab, self).__init__()

    def get_region_frame(self):
        self.grab_new_frame()
        return self.regions[2]

    def Pixel_Calculation(self):
        pass


if __name__ == '__main__':
    # Create regions.
    region_one = Region1()
    region_two = Region2()
    region_three = Region3()

    def trackbar_change(trackbar_id, value):
        region_one.Set_Slider_Data(trackbar_id, value)
        region_two.Set_Slider_Data(trackbar_id, value)
        region_three.Set_Slider_Data(trackbar_id, value)
        print(trackbar_id, value)

    cv2.namedWindow("Main Frame")

    cv2.createTrackbar("LH", "Main Frame", 0, 255, lambda x: trackbar_change("LH", x))
    cv2.createTrackbar("LS", "Main Frame", 0, 255, lambda x: trackbar_change("LS", x))
    cv2.createTrackbar("LV", "Main Frame", 0, 255, lambda x: trackbar_change("LV", x))

    cv2.createTrackbar("HH", "Main Frame", 255, 255, lambda x: trackbar_change("HH", x))
    cv2.createTrackbar("HS", "Main Frame", 255, 255, lambda x: trackbar_change("HS", x))
    cv2.createTrackbar("HV", "Main Frame", 255, 255, lambda x: trackbar_change("HV", x))

    cv2.createTrackbar("Threshold", "Main Frame", 255, 255, lambda x: trackbar_change("Threshold", x))

    while True:
        r1_frame = region_one.get_region_frame()
        r2_frame = region_two.get_region_frame()
        r3_frame = region_three.get_region_frame()

        cv2.imshow("Main Frame", Frame_Grab.combine_regions(r1_frame, r2_frame, r3_frame))

        c = cv2.waitKey(1)
        if c == 27:
            break
