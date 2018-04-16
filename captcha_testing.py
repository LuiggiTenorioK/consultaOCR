import urllib2
import os
import cv2
import numpy as np
import pytesseract
from PIL import Image

def getCaptcha(cant,target):
    directory='tmp'
    if not os.path.exists(directory):
        os.makedirs(directory)
    for i in range(cant):
        url = urllib2.urlopen(target)
        tImg= "./tmp/" + str(i) + ".png"
        with open(tImg, 'wb') as f:
            f.write(url.read())

def deleteCaptcha():
    dir_file = "./tmp/"
    onlyfiles = [f for f in os.listdir(dir_file) if os.path.isfile(os.path.join(dir_file, f))]
    for i in onlyfiles:
        tImg= "./tmp/" + i
        os.remove(tImg)
    os.rmdir('tmp')

def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)


def breakCaptcha():
    dir_file = "tmp/"
    # obtenemos los nombre de los archivos
    onlyfiles = [f for f in os.listdir(dir_file) if os.path.isfile(os.path.join(dir_file, f))]
    for imgFile in onlyfiles:
        im_gray = cv2.imread(dir_file + imgFile, cv2.IMREAD_GRAYSCALE)

        cv2.imwrite("tmp/01_test_gray.png", im_gray)

        (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        cv2.imwrite("tmp/test_th1.png", im_bw)
        im_bw = cv2.threshold(im_bw, thresh, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite("tmp/test_th2.png", im_bw)


        cv2.imwrite(dir_file+"c_"+imgFile, im_bw)
        # convertimos la imagen a texto utilizando texto
        img_diree=dir_file + "c_" + imgFile
        p_img=Image.open(img_diree)
        text_ocr = pytesseract.image_to_string(p_img)
        text_ocr = text_ocr.strip()

        if len(text_ocr) == 4:
            print(dir_file+"c_"+imgFile)
            print(text_ocr)


def run_tests(n,target):
    getCaptcha(n,target)
    breakCaptcha()
    deleteCaptcha()

if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
    target = 'http://www.sunat.gob.pe/cl-ti-itmrconsruc/captcha?accion=image'
    n=5
    run_tests(n,target)