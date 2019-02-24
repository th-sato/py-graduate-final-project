import matplotlib.pyplot as plt
import cv2 as cv
import os

img_path = os.path.join(os.getcwd(), 'static/images')
img = cv.imread(os.path.join(img_path, 'pista-camera.jpg'))

for i in range(100):
    if i % 2 == 0:
        img2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    else:
        img2 = img
    cv.imshow('Image', img2)
    tecla = cv.waitKey(10) & 0xFF
    if tecla == 27:
        break


# Controlar o estercamento das rodas
# fw.turning_max = valor
# Criar uma funcao para realizar a curva

# sudo make install
# sudo ldconfig