from selenium import webdriver
import time
from pathlib import Path
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-automation']) 

driver = webdriver.Chrome(options=options)
path = str(Path("C:/Users/Muaaz/Desktop/file.jpg"))

driver.implicitly_wait(10)
driver.get('https://s.taobao.com/search?&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20191111&ie=utf8&tfsid=O1CN016kkT2W1fgzUKx5chh_!!2-imgsearch.png&app=imgsearch')
url2 = 'https://s.taobao.com/search?'

#while url2 != driver.current_url:
#        time.sleep(1)
time.sleep(60)

#input = driver.find_element_by_id("TPL_username_1")
#input.send_keys("viatorjoey")
#input2 = driver.find_element_by_id("TPL_password_1")
#input2.send_keys("zipman7joey")
#input3 = driver.find_element_by_id("J_SubmitStatic")
#input3.click()

try:
    input = driver.find_element_by_xpath("//input[@type='file']")
    driver.execute_script("arguments[0].style.display = 'block';", input)
    input.send_keys(path)
except:
    pass       

while url2 == driver.current_url:
        time.sleep(1)

print(driver.current_url)
price = driver.find_elements_by_css_selector('div[class="price g_price g_price-highlight"]')
for price in price:
    print(price.text)


images = driver.find_elements_by_css_selector('div[class="row row-2 title"]')
for i in images:
    print(i.text)