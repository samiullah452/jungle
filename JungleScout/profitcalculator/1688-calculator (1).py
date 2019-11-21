from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import subprocess
import time
from pathlib import Path
import re
from googletrans import Translator

translator = Translator() 
path = str(Path("C:/Users/Muaaz/Desktop/file.jpg"))
url =  'https://www.1688.com/'

firefox_options = Options()
firefox_options.add_argument('-headless')

profile = webdriver.FirefoxProfile()
profile.set_preference("dom.file.createInChild",True)
firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True


browser = webdriver.Firefox(firefox_options=firefox_options,firefox_profile = profile,capabilities=firefox_capabilities)
browser.implicitly_wait(10) # seconds
browser.get(url)


try:
        browser.execute_script("document.getElementById('img-search-btn').click()")
        input = browser.find_element_by_xpath('//input[@type="file"]')
        browser.execute_script("var input = arguments[0];input.style.display = 'block'", input)
        input.send_keys(path)
        browser.execute_script("document.getElementById('img-search-btn').click()")
        browser.execute_script("var input = arguments[0];input.style.display = 'block'", input)
        input.send_keys(path)
except:
        pass
       
while url == browser.current_url :
        time.sleep(1)

url_1688 = browser.current_url
f = open("url.txt","w")
f.write(url_1688) 
f.close()

print(url_1688)
time.sleep(3)
price = browser.find_elements_by_css_selector('div>span[class]')
p = []

for price in price: 
    P = re.findall("\d{1,10}\.\d{2}",price.text)
    for pr in P:
        p.append(float(pr))
minimum = min(p) 
maximum = max(p)
average = sum(p)/len(p)        
print(minimum,maximum,average)

title = browser.find_elements_by_css_selector('div>a[title]')
title.pop()

for title in title:
         
       Title = translator.translate(title.text,src='zh-CN',dest='en')  
       break
print(Title)
browser.quit()