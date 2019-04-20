import os
import cv2 as cv


def show_image(img):
    cv.imshow('image', img)
    # cv.waitKey(10)
    cv.waitKey(0)
    # cv.destroyAllWindows()


def image_test():
    static_path = os.path.join(os.getcwd(), '2019-03-25')
    return cv.imread(os.path.join(static_path, 'pista-camera9.jpg'))


if __name__ == "__main__":
    img = image_test()
    show_image(img)