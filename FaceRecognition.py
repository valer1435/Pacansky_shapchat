import math

import imutils
import numpy as np
import cv2

from OpenCV.Settings.sptites_settings import SETTINGS
from OpenCV.help_functions import overlay_image_alpha


class MainThread:
    eyeCascade = cv2.CascadeClassifier('Cascades/haarcascade_eye.xml')
    faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

    def __init__(self):
        self.hat = None
        self.glass = None
        self.face = None
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)  # set Width
        self.cap.set(4, 480)  # set Height
        self.final = None

    def main(self):
        ret, image = self.cap.read()
        self.final = image
        img = image.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = MainThread.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(20, 20)
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            eyes = MainThread.eyeCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=20,
                minSize=(10, 10)

            )
            eyes_center = []
            if len(eyes) == 2:
                for (x1, y1, w1, h1) in sorted(eyes, key=lambda points: points[0]):
                    cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
                    eyes_center.append((x1 + w1 // 2, y1 + h1 // 2))

                # there we find important constants like length behind eyes, rotate angle, etc
                length_of_eyes_line = math.sqrt(
                    math.pow(eyes_center[0][0] - eyes_center[1][0], 2)
                    +
                    math.pow(eyes_center[0][1] - eyes_center[1][1], 2))
                cv2.line(img, eyes_center[0], eyes_center[1], (0, 0, 255))

                tan_alpha = (eyes_center[1][1] - eyes_center[0][1]) / (eyes_center[1][0] - eyes_center[0][0])
                rotate_angle = math.atan(tan_alpha)

                absolute_center = (
                    (eyes_center[0][0] + eyes_center[1][0]) // 2,
                    (eyes_center[0][1] + eyes_center[1][1]) // 2
                )

                if self.face:
                    self.final = MainThread.draw_face(self.face,
                                                      self.final,
                                                      absolute_center,
                                                      length_of_eyes_line,
                                                      h,
                                                      rotate_angle)

                if self.glass:
                    self.final = MainThread.draw_glass(self.glass,
                                                       self.final,
                                                       absolute_center,
                                                       length_of_eyes_line,
                                                       rotate_angle)

                if self.hat:
                    self.final = MainThread.draw_hat(self.hat,
                                                     self.final, 
                                                     absolute_center,
                                                     y,
                                                     w,
                                                     rotate_angle)

                cv2.imshow('video1', self.final)
        cv2.imshow('video', img)

        k = cv2.waitKey(30) & 0xff
        if k == 27:  # press 'ESC' to quit
            return False
        if k == 49:  # press 1
            self.set_face("spider_face")
        if k == 61:  # press =
            self.set_face(None)

        if k == 113:  # press q
            self.set_glass("pixel_glass")
        if k == 119:  # press w
            self.set_glass("letov_glass")
        if k == 92:  # press \
            self.set_glass(None)

        if k == 97:  # press a
            self.set_hat("adidas_hat")
        if k == 39:  # press '
            self.set_hat(None)

        return True

    @staticmethod
    def draw_face(name, surface, center,  lenth_eyes_line, h_face, rotate_angle):
        face_scale_x = SETTINGS[name]["scale"] * lenth_eyes_line / (SETTINGS[name]["line_between_eyes"])
        face_scale_y = (h_face + h_face // 2.5) / SETTINGS[name]["image"].shape[0]
        overlay_face = cv2.resize(SETTINGS[name]["image"], None, fx=face_scale_x, fy=face_scale_y,
                                  interpolation=cv2.INTER_AREA)
        overlay_face = imutils.rotate_bound(overlay_face, math.degrees(rotate_angle))

        final = overlay_image_alpha(surface,
                                    overlay_face[:, :, 0:3],
                                    center,
                                    overlay_face[:, :, 3] / 255.0)
        return final

    @staticmethod
    def draw_glass(name, surface, center,  lenth_eyes_line, rotate_angle):
        glasses_width = SETTINGS[name]["scale"] * lenth_eyes_line
        h_g, w_g = SETTINGS[name]["image"].shape[:2]
        scaling_factor = glasses_width / w_g

        print(center[0], SETTINGS[name]["x_direction"] * scaling_factor)
        center_glass = (
            center[0] + int(SETTINGS[name]["x_direction"] * scaling_factor),
            center[1] + int(SETTINGS[name]["y_direction"] * scaling_factor)
        )
        overlay_glasses = cv2.resize(SETTINGS[name]["image"], None, fx=scaling_factor,
                                     fy=scaling_factor,
                                     interpolation=cv2.INTER_AREA)
        overlay_glasses = imutils.rotate_bound(overlay_glasses, math.degrees(rotate_angle))
        final = overlay_image_alpha(surface,
                                    overlay_glasses[:, :, 0:3],
                                    center_glass,
                                    overlay_glasses[:, :, 3] / 255.0)

        return final

    @staticmethod
    def draw_hat(name, surface, center, y_face, w_face, rotate_angle):

        # so there we find X coordinate of intersecting line normal to main axis (line between eyes)
        tan_alpha = math.tan(rotate_angle)
        if tan_alpha != 0:
            a = (y_face - center[1]) / math.sin(math.atan(-1 / tan_alpha))
        else:
            a = (y_face - center[1])

        y_powed = math.pow(y_face - center[1], 2)
        c_part = y_powed - math.pow(a, 2) + math.pow(center[0], 2)
        b_part = -center[0]
        discr = math.sqrt(b_part ** 2 - c_part)

        if tan_alpha > 0:
            res = -b_part + discr
        else:
            res = -b_part - discr

        hat_scale = SETTINGS[name]["scale"] * w_face / (SETTINGS[name]["image"].shape[1])
        overlay_hat = cv2.resize(SETTINGS[name]["image"], None, fx=hat_scale, fy=hat_scale,
                                 interpolation=cv2.INTER_AREA)
        overlay_hat = imutils.rotate_bound(overlay_hat, math.degrees(rotate_angle))

        final = overlay_image_alpha(surface,
                                    overlay_hat[:, :, 0:3],
                                    (int(res), int(y_face - overlay_hat.shape[0] / 6)),
                                    overlay_hat[:, :, 3] / 255.0)
        return final

    def set_glass(self, glass):
        self.glass = glass

    def set_hat(self, hat):
        self.hat = hat

    def set_face(self, face):
        self.face = face


if __name__ == "__main__":
    newThread = MainThread()
    while 1:
        if not newThread.main():
            break
