def profitcal(files,website,keys):
	content={}
	i=0
	if website=='1688':
		from selenium import webdriver
		from selenium.webdriver.firefox.options import Options
		import subprocess
		import time
		from pathlib import Path
		import re
		from googletrans import Translator
		translator = Translator() 
		url =  'https://www.1688.com/'

		firefox_options = Options()
		firefox_options.add_argument('-headless')

		profile = webdriver.FirefoxProfile()
		profile.set_preference("dom.file.createInChild",True)
		firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
		firefox_capabilities['marionette'] = True


		browser = webdriver.Firefox(executable_path='profitcalculator/geckodriver',firefox_options=firefox_options,firefox_profile = profile,capabilities=firefox_capabilities)
		browser.implicitly_wait(10) # seconds

		for files in file:
			content[i]={}
			content[i]['key']=file
			browser.get(url)
			path = str(Path(key))
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

			time.sleep(3)
			title = browser.find_elements_by_css_selector('div>a[title]')
			title.pop()

			for title in title:
			         
			       Title = translator.translate(title.text,src='zh-CN',dest='en')  
			       content[i]['title']=Title
			       break

			price = browser.find_elements_by_css_selector('div>span[class]')
			p = []

			for price in price: 
			    P = re.findall("\d{1,10}\.\d{2}",price.text)
			    for pr in P:
			        p.append(float(pr))
			if len(p):
				minimum = min(p) 
				maximum = max(p)
				average = sum(p)/len(p)        
			else:
				minimum=0
				maximum=0
				average=0

			content[i]['min']=minimum
			content[i]['max']=maximum
			content[i]['avg']=average
			content[i]['key']=file	
			i+=1
		browser.quit()
		return content

	if website=='TAOBAO':
		from selenium import webdriver
		import time
		from pathlib import Path
		from selenium.webdriver.chrome.options import Options

		options = Options()
		options.add_experimental_option('excludeSwitches', ['enable-automation']) 
		options.add_argument('--headless')
		driver = webdriver.Chrome('contentdownloader/chromedriver',options=options)
		driver.implicitly_wait(10)

		for files in file:
			content[i]={}
			content[i]['key']=file
			driver.get('https://s.taobao.com/search?&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20191111&ie=utf8&tfsid=O1CN016kkT2W1fgzUKx5chh_!!2-imgsearch.png&app=imgsearch')
			url2 = 'https://s.taobao.com/search?'
			path = str(Path(key))
			try:
			    input = driver.find_element_by_xpath("//input[@type='file']")
			    driver.execute_script("arguments[0].style.display = 'block';", input)
			    input.send_keys(path)
			except:
			    pass       

			while url2 == driver.current_url:
			        time.sleep(1)
			images = driver.find_elements_by_css_selector('div[class="row row-2 title"]')
			for i in images:
			    content[i]['title']=(i.text)
			    break

			p = []
			price = driver.find_elements_by_css_selector('div[class="price g_price g_price-highlight"]')
			for price in price:
			    p.append(price.text)
			if len(p):
				minimum = min(p) 
				maximum = max(p)
				average = sum(p)/len(p)        
			else:
				minimum=0
				maximum=0
				average=0

			content[i]['min']=minimum
			content[i]['max']=maximum
			content[i]['avg']=average
			content[i]['key']=file	

			i+=1
		return content

	if website=="Alibaba":
		from selenium import webdriver
		from selenium.webdriver.firefox.options import Options
		import subprocess
		import time
		from pathlib import Path
		import re

		url =  'https://www.alibaba.com/'
		firefox_options = Options()
		firefox_options.add_argument('-headless')
		profile = webdriver.FirefoxProfile()
		profile.set_preference("dom.file.createInChild",True)
		firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
		firefox_capabilities['marionette'] = True
		browser = webdriver.Firefox(executable_path='profitcalculator/geckodriver',firefox_options=firefox_options,firefox_profile = profile,capabilities=firefox_capabilities)
		browser.implicitly_wait(20)
		for file in files:
			content[i]={}
			content[i]['key']=file
			browser.get(url)
			element = browser.find_element_by_class_name("ui-searchbar-imgsearch-icon")
			browser.execute_script("arguments[0].click();", element)
			input = browser.find_element_by_xpath("//input[@type='file']")
			browser.execute_script("arguments[0].style.display = 'block';", input)
			path = str(Path(file))

			input.send_keys(path)
			        
			while url == browser.current_url:
			        time.sleep(1)
			time.sleep(3)

			title = browser.find_elements_by_css_selector('div>a[title]')
			for title in title:
			    Title = title.text
			    if Title!='':
				    content[i]['title']=Title 
				    break
			if 'title' not in content[i]:
		 	    content[i]['title']="Product"
			prices = browser.find_elements_by_class_name('bc-ife-gallery-price')
			p = []
			for prices in prices:
			    P = re.findall("\d{1,10}\.\d{2}",prices.text)
			    for pr in P:
			        p.append(float(pr))
			if len(p):
				minimum = min(p) 
				maximum = max(p)
				average = sum(p)/len(p)        
			else:
				minimum=0
				maximum=0
				average=0

			content[i]['min']=minimum
			content[i]['max']=maximum
			content[i]['avg']=average
			i+=1
		print(content)
		return content
