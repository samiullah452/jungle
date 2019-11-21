def supplier(keys,website):
	supplier={}
	if website=='1688':
		from selenium import webdriver
		import time
		from selenium.webdriver.chrome.options import Options
		options = Options()
		options.add_argument('--headless')
		driver= webdriver.Chrome('contentdownloader/chromedriver.exe',options=options)

		from selenium.webdriver.common.keys import Keys
		i=0	
		for key in keys:
			supplier[i]={}
			driver.get('https://s.1688.com/company/company_search.htm?keywords=watch&n=y&netType=1%2C11&encode=utf-8&spm=a260k.dacugeneral.search.0')
			supplier[i]['image']=[]
			time.sleep(5)
			Send = driver.find_element_by_css_selector('div>input[type="text"]')
			Send.clear()
			Send.send_keys(key)
			button = driver.find_element_by_xpath('//*[@id="s_search_form"]/fieldset/div[2]/div[1]/div/div[2]/button').click()

			company_detalis = driver.find_elements_by_class_name('list-item-left')
			for company_detalis in company_detalis:
			    supplier[i]['company_detalis']=company_detalis.text

			title = driver.find_elements_by_class_name('list-item-right')
			for title in title:
				supplier[i]['title']=title.text

			title = driver.find_elements_by_css_selector('div[class="img-thumb"]>a>img')
			for title in title:
				supplier[i]['image'].append(title.get_attribute('src'))

			images = driver.find_elements_by_xpath('//*[@id="mod-detail-bd"]/div[1]/div/div/div/div/div[1]/div/a/img')
			for images in images:
				supplier[i]['image'].append(title.get_attribute('src'))
		print(supplier)
	elif website=="Alibaba":
		from selenium import webdriver
		import time
		from selenium.webdriver.chrome.options import Options
		options = Options()
		options.add_argument("--headless")
		options.add_argument("start-maximized")
		options.add_argument("disable-infobars")
		options.add_argument("--disable-extensions")
		options.add_argument("--no-sandbox")
		options.add_argument("window-size=1920,1080")
		options.add_argument("--disable-dev-shm-usage")		
		from selenium.webdriver.common.keys import Keys

		driver= webdriver.Chrome('contentdownloader/chromedriver.exe',options=options)

		i=0
		for key in keys:
			driver.get('https://www.alibaba.com/corporations/watch.html')
			time.sleep(5)
			Send = driver.find_element_by_name('SearchText')
			Send.clear()
			Send.send_keys(key)
			button = driver.find_element_by_xpath('//*[@id="J_SC_header"]/header/div[2]/div[2]/div/div[1]/form/input[4]').click()
			for j in range(1,11):
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight*"+str(j/10)+");")
				time.sleep(2)
		
			for company_detali in driver.find_elements_by_xpath('//div[@class="item-main"]'):
				try:
					supplier[i]={}
					supplier[i]['group']='Uncategorized'
					supplier[i]['shop-name']=''
					supplier[i]['image']=[]
					supplier[i]['title']=''
					supplier[i]['price']=''
					supplier[i]['region']=''
					supplier[i]['url']=''
					title = company_detali.find_elements_by_class_name('item-title')
					urls=title[0].find_element_by_xpath('.//h2[@class="title ellipsis"]/a')
					supplier[i]['url']=urls.get_attribute('href')
					supplier[i]['shop-name']=urls.text
					name=company_detali.find_element_by_xpath('.//*[@class="value ellipsis ph"]')
					supplier[i]['title']=name.text

					name=company_detali.find_elements_by_xpath('.//*[@class="ellipsis search"]')
					supplier[i]['region']=name[0].text
					supplier[i]['price']=name[1].text

					images = company_detali.find_elements_by_xpath('.//*[@class="img-thumb"]/a/img')
					j=0
					for image in images:
						if image.get_attribute('src') is None:
							continue
						if j==3:
							break
						supplier[i]['image'].append(image.get_attribute('src'))			    
						j+=1
					if len(supplier[i]['image'])>0:
						i+=1 
				except:
					pass
		return supplier		   