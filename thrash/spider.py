import pandas as pd
from time import sleep, time
from selenium import webdriver
from PIL import Image
#import pytesseract
import random
import platform

def get_proxy_server():
    aleatorio = random.randint(0, 1)
    arr_proxy = ["190.117.188.223:3128","200.60.130.162:3128"]
    return arr_proxy[aleatorio]

def get_driver():
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    proxy_server = get_proxy_server()
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap['platform'] = "WINDOWS"
    dcap['version'] = "10"

    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
       ]

    dcap["phantomjs.page.settings.userAgent"] = user_agent_list[random.randrange(1, len(user_agent_list)-1, 1)]

    if platform.system() == 'Linux':
        #driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs", desired_capabilities=dcap,
        #                                  service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1',
        #                                                '--proxy=127.0.0.1:9050', '--proxy-type=socks5'])
        driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs", desired_capabilities=dcap,
                                     service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1',
                                                   '--proxy=' + proxy_server, '--proxy-type=http'])
    else:
        driver = webdriver.PhantomJS(
            executable_path="phantomjs/phantomjs.exe",
            desired_capabilities=dcap)

    return driver



def collectData():
    pass



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
    driver.save_screenshot("screencaptcha.png")
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
                    driver.save_screenshot("screencaptcha.png")
                    driver.close()
            driver.switch_to_window(main_page_hadler)

        if flag==0:
            collectData(driver)
        else:
            n_err+=1







def main(rucs):
    #url='http://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/frameCriterioBusqueda.jsp'
    url='http://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias'
    #driver =  webdriver.Chrome('chromedriver.exe')
    driver=get_driver()
    driver.set_window_size(1124, 850)
    driver.get(url)
    rucs=rucs[:5] #test
    for ruc in rucs:
        getData(driver,str(ruc))


if __name__ == '__main__':
    start_time = time()
    df=pd.read_csv('ruc.txt')
    rucs=list(df['RUC'].values)
    main(rucs)

    a = 0
    input(a)
