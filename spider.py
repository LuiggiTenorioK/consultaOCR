import pandas as pd
from time import sleep, time
from selenium import webdriver
from PIL import Image
import pytesseract
import cv2
import random
import platform
import pickle
import copy

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


def subCollectRepresentanteLegal(driver,result):
    # Representantes Legales
    driver.find_element_by_xpath('//*[@id="div_estrep"]/table/tbody/tr[3]/td/form/input[1]').click()
    sleep(2)
    result['RepresentantesLegales'] = list()
    i = 2
    while 1:
        try:
            rep = {}
            rep['Documento'] = driver.find_element_by_xpath(
                '//*[@id="print"]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[' + str(i) + ']/td[1]').text
            rep['NroDocumento'] = driver.find_element_by_xpath(
                '//*[@id="print"]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[' + str(i) + ']/td[2]').text
            rep['Nombre'] = driver.find_element_by_xpath(
                '//*[@id="print"]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[' + str(i) + ']/td[3]').text
            rep['Cargo'] = driver.find_element_by_xpath(
                '//*[@id="print"]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[' + str(i) + ']/td[4]').text
            rep['FechaDesde'] = driver.find_element_by_xpath(
                '//*[@id="print"]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[' + str(i) + ']/td[5]').text
            result['RepresentantesLegales'].append(rep)
        except Exception as e:
            break
        i += 1

    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.find_element_by_xpath('//*[@id="div_estrep"]/table/tbody/tr[1]/td/div/input').click()

    return result

def subCollectPeriodo(driver,result):
    # Trabajadores y Prestatarios
    driver.find_element_by_xpath('//*[@id="div_estrep"]/table/tbody/tr[1]/td[4]/form/input[1]').click()
    sleep(2)
    result['Periodico'] = []
    i = 3
    while 1:
        try:
            reg = {}
            reg['Periodo'] = driver.find_element_by_xpath(
                '//*[@id="print"]/table[3]/tbody/tr/td/table/tbody/tr[' + str(i) + ']/td[1]').text
            reg['NroTrabajadores'] = driver.find_element_by_xpath(
                '//*[@id="print"]/table[3]/tbody/tr/td/table/tbody/tr[' + str(i) + ']/td[2]').text
            reg['NroPensionistas'] = driver.find_element_by_xpath(
                '//*[@id="print"]/table[3]/tbody/tr/td/table/tbody/tr[' + str(i) + ']/td[3]').text
            reg['NroPrestadores'] = driver.find_element_by_xpath(
                '//*[@id="print"]/table[3]/tbody/tr/td/table/tbody/tr[' + str(i) + ']/td[4]').text
            result['Periodico'].append(reg)
        except Exception as e:
            break
        i += 1

    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.find_element_by_xpath('/html/body/table[1]/tbody/tr[1]/td/div/input').click()

    return result


def collectData(driver):
    result={}
    result['Razon_Social']=driver.find_element_by_xpath('/html/body/table[1]/tbody/tr[1]/td[2]').text
    result['Tipo']=driver.find_element_by_xpath('/html/body/table[1]/tbody/tr[2]/td[2]').text
    result['Nombre_Comercial']=driver.find_element_by_xpath('/html/body/table[1]/tbody/tr[3]/td[2]').text
    result['Estado']=driver.find_element_by_xpath('/html/body/table[1]/tbody/tr[5]/td[2]').text
    result['Condicion']=driver.find_element_by_xpath('/html/body/table[1]/tbody/tr[6]/td[2]').text
    result['Direccion'] = driver.find_element_by_xpath('/html/body/table[1]/tbody/tr[7]/td[2]').text
    result['ActividadesEconomicas'] = driver.find_element_by_xpath('/html/body/table[1]/tbody/tr[10]/td[2]/select').get_attribute("innerHTML")
    print('previo')
    print(result)

    print(driver.current_url)

    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    result=subCollectRepresentanteLegal(copy.copy(driver),result)

    print('previo')
    print(result)
    driver.save_screenshot("info.png")

    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    result=subCollectPeriodo(driver,result)

    print('previo')
    print(result)
    driver.save_screenshot("info.png")

    '''
    driver.find_element_by_xpath('//*[@id="div_estrep"]/table/tbody/tr[1]/td/div/input').click()
    driver.find_element_by_xpath('/html/body/table[1]/tbody/tr[1]/td/div/input').click()
    '''
    return result



def procesaCaptcha(driver):
    driver.save_screenshot("screencaptcha.png")
    img = Image.open("screencaptcha.png")
    img_aux = img.crop((804, 35, 910, 90))
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
    text_ocr=text_ocr.replace(" ", "")
    # imprimimos la informacion siempre y cuando tenga el tamanho de caracteres correctos
    if len(text_ocr) == 4:  # SUNEDU, tiene 3 caracteres su captcha
        return text_ocr
    else:
        return ""


def getData(driver,url,ruc):
    result={}
    n_err=0

    while n_err<5:
        flag=0

        #Inserta RUC
        driver.get(url)
        sleep(2)

        driver.find_element_by_xpath('//*[@id="s1"]/input').clear()
        driver.find_element_by_xpath('//*[@id="s1"]/input').send_keys(ruc)

        #CAPTCHA
        capt = ''
        while len(capt)!=4:
            driver.set_window_size(1124, 850)
            driver.save_screenshot("screencaptcha.png")
            img = Image.open("screencaptcha.png")
            img1 = img.crop((804, 35, 910, 90))
            driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[2]/td[4]/a').click()
            driver.save_screenshot("screencaptcha.png")
            img = Image.open("screencaptcha.png")
            img2 = img.crop((804, 35, 910, 90))

            while img1==img2:
                driver.save_screenshot("screencaptcha.png")
                img = Image.open("screencaptcha.png")
                img2 = img.crop((804, 35, 910, 90))
                sleep(1)
                print('Cargando captcha')



            capt = procesaCaptcha(driver)
            print(capt)


        driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[1]/td[6]/input').clear()
        driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[1]/td[6]/input').send_keys(capt)
        driver.save_screenshot("insertcaptcha.png")
        driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[1]/td[7]/input').click()

        #ALERTA

        try:
            driver.switch_to_alert().accept()
            print('ALERTA: fallo')
            flag += 1
        except Exception as e:
            #print('pass')
            pass

        #print(driver.window_handles)

        if len(driver.window_handles)==2:
            aux = driver.window_handles
            driver.close()
            driver.switch_to_window(aux[1])

        sleep(2)
        #Verificacion de pagina de datos
        try:
            verif=driver.find_element_by_xpath('/html/body/table[1]/tbody/tr[1]/td[1]').text
            if "RUC" in verif:
                print('data ready for: ' + str(ruc))
                result=collectData(driver)

                return result
            else:
                n_err+=1
        except Exception as e:
            driver.save_screenshot("errorcaptcha.png")
            n_err+=1

        print(str(ruc)+' va ' +str(n_err)+' errores')




def main(rucs):
    url='http://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/frameCriterioBusqueda.jsp'
    #url='http://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias'
    #driver =  webdriver.Chrome('chromedriver.exe')
    driver=get_driver()
    driver.set_window_size(1124, 850)
    #driver.get(url)
    rucs=rucs[:5] #test
    dataset=[]
    for ruc in rucs:
        data=getData(driver,url,str(ruc))
        dataset.append(data)
        print(data)

    print(dataset)




if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
    start_time = time()
    df=pd.read_csv('ruc.txt')
    rucs=list(df['RUC'].values)
    main(rucs)

    a = 0
    input(a)
