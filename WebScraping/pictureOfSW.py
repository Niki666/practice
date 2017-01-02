#coding=utf-8
import urllib
import urllib2
import re
import urllib

def download_page(url):
    request = urllib2.Request(url)
    response = urllib.urlopen(request)
    data = response.read()
    return data

def get_image(html):
    regx = r'\/teacherspic\/*\.jpg'
    pattern = re.compile(regx)
    get_imag = re.findall(pattern,repr(html))
    num = 1
    for img in  get_imag:
        image = download_page(img)
        with open('%s.jpg'%num,'wb') as fb:
            fb.write(image)
            num += 1
            print ('working'%num)
    return

url = 'http://www.cse.cqu.edu.cn/FrontPage/TeacherPage'
html = download_page(url)
get_image(html)