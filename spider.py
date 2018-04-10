import pandas as pd
from time import sleep, time
from selenium import webdriver
from PIL import Image
import cv2
import pytesseract

def collectData():




def procesaCaptcha(driver):
    driver.save_screenshot("screencaptcha.png")
    img = Image.open("screencaptcha.png")
    img_aux = img.crop((790, 30, 890, 80))
    img_aux.save("captcha.png")

    # convert color img to black and white, using OpenCV
    #im_gray = cv2.imread("captcha.png", cv2.CV_LOAD_IMAGE_GRAYSCALE)
    im_gray = cv2.imread("captcha.png", cv2.IMREAD_GRAYSCALE)

    #im_gray = cv2.GaussianBlur(im_gray, (3, 3), 0)
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    im_bw = cv2.threshold(im_bw, thresh, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite("captcha_gray.png", im_bw)
    # convertimos la imagen a texto utilizando texto
    text_ocr = pytesseract.image_to_string(Image.open("captcha_gray.png"))
    text_ocr = text_ocr.strip()
    # imprimimos la informacion siempre y cuando tenga el tamanho de caracteres correctos
    if len(text_ocr) == 4:  # SUNEDU, tiene 3 caracteres su captcha
        return text_ocr
    else:
        return ""


def getData(driver,ruc):
    sleep(1)
    driver.find_element_by_xpath('//*[@id="s1"]/input').clear()
    driver.find_element_by_xpath('//*[@id="s1"]/input').send_keys(ruc)

    main_page_hadler=driver.window_handles[0]

    n_err=0

    while n_err<5:
        flag=0
        capt='AAAA'
        # capt=procesaCaptcha(driver)
        driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[1]/td[6]/input').clear()
        driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[1]/td[6]/input').send_keys(capt)
        sleep(5)
        driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[1]/td[7]/input').click()

        try:
            driver.switch_to_alert().accept()
            print('fallo')
            flag += 1
        except Exception as e:
            print('wtf')


        if len(driver.window_handles)>1:
            aux=driver.window_handles
            flag+=1
            for i in aux:
                if i != main_page_hadler:
                    driver.switch_to_window(i)
                    driver.close()
            driver.switch_to_window(main_page_hadler)

        if flag==0:
            collectData(driver)
        else:
            n_err+=1



def main(rucs):
    url='http://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/frameCriterioBusqueda.jsp'

    driver =  webdriver.Chrome('chromedriver.exe')
    driver.set_window_size(1124, 850)
    driver.get(url)

    for ruc in rucs:
        getData(driver,str(ruc))


if __name__ == '__main__':
    start_time = time()
    df=pd.read_csv('ruc.txt')
    rucs=list(df['RUC'].values)
    main(rucs)

    a = 0
    input(a)
