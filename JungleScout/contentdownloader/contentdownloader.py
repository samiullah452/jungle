def content(urls,website):
	content={}
	if website=='1688':
		from selenium import webdriver
		import time
		from selenium.webdriver.chrome.options import Options
		options = Options()
		options.add_argument('--headless')
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')
		driver= webdriver.Chrome('contentdownloader/chromedriver',options=options)
		i=0
		for url in urls:
			content[i]={}
			content[i]['group']='Uncategorized'			    
			driver.get(url)
			time.sleep(5)
			shop_name=driver.find_elements_by_xpath('//div[@class="mod-detail-hd"]')
			for shop in shop_name:
				content[i]['shop-name']=shop.text
			images = driver.find_elements_by_xpath('//*[@id="mod-detail-bd"]/div[1]/div/div/div/div/div[1]/div/a/img')

			for images in images:
			    content[i]['image']=images.get_attribute('src')

			title = driver.find_elements_by_xpath('//*[@id="mod-detail-price"]/div/table')
			for title in title:
			    content[i]['title']=title.text

			offer = driver.find_elements_by_xpath('//*[@id="mod-detail-bd"]/div[2]/div[6]/div/div')
			for offer in offer:
			    content[i]['price']=offer.text

			details = driver.find_elements_by_xpath('//*[@id="mod-detail-bd"]/div[2]/div[8]/div/div')
			for details in details:
			    content[i]['details']=details.text
			content[i]['url']=url
			i+=1
	elif website=='Alibaba':
		from selenium import webdriver
		import time

		from selenium.webdriver.chrome.options import Options
		options = Options()
		options.add_argument('--headless')
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')
		i=0
		driver = webdriver.Chrome('contentdownloader/chromedriver',options=options)
		for url in urls:
			content[i]={}
			content[i]['group']='Uncategorized'			    
			driver.get(url)
			name = driver.find_elements_by_class_name('company-name-container')
			for name in name:
 				content[i]['shop-name']=name.text


			images=driver.find_elements_by_xpath('//div[@class="iwrap nopic"]/a/img')
			for images in images:
			    content[i]['image']=images.get_attribute('src')
	
			if 'image' not in content[i]:
				images = driver.find_elements_by_class_name('pic')
				for images in images:
				    content[i]['image']=images.get_attribute('src')
		
			if 'image' not in content[i]:
				image=driver.find_element_by_xpath('//div[@class="thumb"]/a/img').click()
				images = driver.find_elements_by_class_name('pic')
				for images in images:
				    content[i]['image']=images.get_attribute('src')

			title = driver.find_elements_by_class_name('ma-title')
			for title in title:
			    content[i]['title']=title.text

			price = driver.find_elements_by_class_name('ma-price-wrap')
			for price in price:
			    content[i]['price']=price.text

			if 'price' not in content[i]:
				price = driver.find_elements_by_class_name('ma-reference-price-highlight')
				for price in price:
				    content[i]['price']=price.text

			if 'price' not in content[i]:
				price = driver.find_elements_by_class_name('pre-inquiry-price')
				for price in price:
				    content[i]['price']=price.text
			
			content[i]['details']=''
			table = driver.find_elements_by_tag_name('table')
			for table in table:
			    content[i]['details']+=table.text
			content[i]['url']=url
			i+=1
	elif website=="TAOBAO":
		from selenium import webdriver
		import time
		from selenium.webdriver.chrome.options import Options
		options = Options()
		options.add_argument('--headless')
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')
		driver= webdriver.Chrome('contentdownloader/chromedriver',options=options)
		i=0
		for url in urls:
			content[i]={}
			content[i]['group']='Uncategorized'			    
			driver.get(url)
			time.sleep(5)
			title = driver.find_elements_by_class_name('tb-shop-name')
			for title in title:
   			    content[i]['shop-name']=title.text			     

			if 'shop-name' not in content[i]:
				title = driver.find_elements_by_class_name('shop-name-link')
				for title in title:
				    print(title)
				    content[i]['shop-name']=title.text			     


			if 'shop-name' not in content[i]:
				    content[i]['shop-name']=''	
		     
			images = driver.find_elements_by_id('J_ImgBooth')
			for images in images:
			    content[i]['image']=images.get_attribute('src')

			title = driver.find_elements_by_class_name('tb-main-title')
			for title in title:
   			    content[i]['title']=title.text			     
			
			offer = driver.find_elements_by_id('J_StrPrice')
			for offer in offer:
				content[i]['price']=offer.text			     

			details = driver.find_elements_by_class_name('attributes')
			content[i]['details']=''			     
			for details in details:
				content[i]['details']+=details.text			     
			content[i]['url']=url			     
			i+=1
	return content 
