from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import subprocess
import time
from pathlib import Path
import re

path = str(Path("C:/Users/Muaaz/Desktop/file2.jpg"))


url =  'https://www.alibaba.com/'


firefox_options = Options()
firefox_options.add_argument('-headless')
profile = webdriver.FirefoxProfile()
profile.set_preference("dom.file.createInChild",True)
firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
browser = webdriver.Firefox(firefox_options=firefox_options,firefox_profile = profile,capabilities=firefox_capabilities)
browser.implicitly_wait(20) # seconds
browser.get(url)
element = browser.find_element_by_class_name("ui-searchbar-imgsearch-icon")
#element.click()
browser.execute_script("arguments[0].click();", element)
input = browser.find_element_by_xpath("//input[@type='file']")
browser.execute_script("arguments[0].style.display = 'block';", input)

input.send_keys(path)
        
while url == browser.current_url:
        time.sleep(1)
alibaba_url= browser.current_url
#browser.quit()


print(alibaba_url)

#images = browser.find_elements_by_class_name('inner-img')
#for images in images:
#    print(images.get_attribute('src'))

time.sleep(3)

title = browser.find_elements_by_css_selector('div>a[title]')
for title in title:
    Title = title.text
    print(Title) 
    break
 



minorder = browser.find_elements_by_class_name('bc-ife-gallery-minorder')
for minorder in minorder:
    #print(minorder.text)
    pass    
prices = browser.find_elements_by_class_name('bc-ife-gallery-price')
p = []
for prices in prices:
    P = re.findall("\d{1,10}\.\d{2}",prices.text)
    for pr in P:
        p.append(float(pr))

minimum = min(p) 
maximum = max(p)
average = sum(p)/len(p)        
print(minimum,maximum,average)
# For conversion to Korean currency scrap https://www.x-rates.com/calculator/?from=USD&to=KRW&amount=1
 
minimum = browser.find_elements_by_class_name('bc-ife-gallery-company-title')
for minimum in minimum:
    #print(minimum.text)
    pass
minimum = browser.find_elements_by_class_name('bc-ife-gallery-icon-list-item')
for minimum in minimum:
    #print(minimum.text)
    pass    
