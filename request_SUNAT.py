from lxml import html
import requests

base_url='http://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc'
captcha_url=base_url+'/captcha'
cons_url = base_url+'/jcrS00Alias'

ruc='20138469442'

s = requests.Session()

page = s.get(captcha_url+'?accion=random')
tree = html.fromstring(page.content)

captcha=tree.xpath('/html/body')[0].text_content()

page = s.get(cons_url+'?nroRuc='+ruc+'&accion=consPorRuc&numRnd='+captcha)
tree = html.fromstring(page.content)

table=tree.xpath('/html/body/table')[0]
for i in table:
    try:
        print(i[1].text_content())
    except:
        pass