
"""
Settings for pixel_glasses.png
"""
import cv2

SETTINGS = {
    "pixel_glass":
    {
        "image": cv2.imread("Sprites/pixel_glasses.png", -1),
        "x_direction": -150,
        "y_direction": 0,
        "scale": 3
    },
    "letov_glass":
    {
        "image": cv2.imread("Sprites/letov_glass.png", -1),
        "x_direction": 0,
        "y_direction": 0,
        "scale": 2.15
    },

    "adidas_hat":
    {
        "image": cv2.imread("Sprites/adidas_hat.png", -1),
        "x_direction": -150,
        "y_direction": 0,
        "scale": 1.15
    },
    "letov_hat":
    {
        "image": cv2.imread("Sprites/letov_hat.png", -1),
        "x_direction": -0,
        "y_direction": 0,
        "scale": 1.15
    },
    "spider_face":
    {
        "image": cv2.imread("Sprites/spider_face.png", -1),
        "x_direction": -0,
        "y_direction": 0,
        "scale": 1.75,
        "line_between_eyes" : 700
    }
}
