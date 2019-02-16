import cv2
import os
img_path = os.path.join(os.getcwd(), 'static/images')
img = cv2.imread(os.path.join(img_path, 'straight_lines1.jpg'))
cv2.rectangle(img, (0,0), (100, 100), (255, 255, 255), 2)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Controlar o esterçamento das rodas
# fw.turning_max = valor
# Criar uma função para realizar a curva

# sudo make install
# sudo ldconfig