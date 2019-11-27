def alibaba(urls):
	import requests
	url = 'https://api.exchangerate-api.com/v4/latest/CNY'
	response = requests.get(url)	
	data = response.json()
	rate=data["rates"]["USD"]
	ratekrw=data["rates"]["KRW"]

	from selenium import webdriver
	import time
	import string
	import os
	import urllib.request
	from selenium.webdriver.chrome.options import Options
	options = Options()
	options.add_argument('--headless')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	content={}
	i=0
	driver = webdriver.Chrome('contentdownloader/chromedriver',options=options)
	for url in urls:
		try:
			content[i]={}
			content[i]['group']='Uncategorized'			    
			content[i]['image']=[]
			content[i]['region']=urls[url]['region']
			driver.get(urls[url]['url'])
			name = driver.find_elements_by_class_name('company-name-container')

			for name in name:
				content[i]['company_href']=name.find_element_by_xpath(".//a").get_attribute('href')
				content[i]['shop-name']=name.text

			images=driver.find_elements_by_xpath('//div[@class="thumb"]/a/img')
			j=0
			for image in images:
				try:
					if j==3:
						break
					image.click()
					imgs = driver.find_elements_by_xpath('//div[@class="iwrap nopic"]/a/img')
					for img in imgs:
						content[i]['image'].append(img.get_attribute('src'))
						j+=1
				except Exception as e:
					pass

			title = driver.find_elements_by_class_name('ma-title')
			for title in title:
			    content[i]['title']=title.text

			price = driver.find_elements_by_class_name('ma-price-wrap')
			for price in price:
				index=(price.text).find("$")
				if index==-1:
					index=0
				content_price=''

				for d in (price.text)[index+1:-1]:
					if d.isdigit() or d=='.':
						content_price+=d
					if d=="/" or d==" " or d=="$" or d.isalpha():
						break

				content[i]['price']=round((1/rate)*float(content_price), 2)

			if 'price' not in content[i]:
				price = driver.find_elements_by_class_name('ma-reference-price-highlight')
				for price in price:
					index=(price.text).find("$")
					if index==-1:
						index=0
					content_price=''
					for d in (price.text)[index+1:-1]:
						if d.isdigit() or d=='.':
							content_price+=d
						if d=="/" or d==" " or d=="$" or d.isalpha():
							break
				content[i]['price']=round((1/rate)*float(content_price), 2)


			if 'price' not in content[i]:
				price = driver.find_elements_by_class_name('pre-inquiry-price')
				for price in price:
					index=(price.text).find("$")
					if index==-1:
						index=0
					content_price=''
					for d in (price.text)[index+1:-1]:
						if d.isdigit() or d=='.':
							content_price+=d
						if d=="/" or d==" " or d=="$" or d.isalpha():
							break
				content[i]['price']=round((1/rate)*float(content_price), 2)


			content[i]['price_krw']=round((ratekrw)*float(content[i]['price']), 2)
			content[i]['url']=urls[url]['url']
			i+=1
		except Exception as e:
			print(urls[url]['url'])
			print(e)
	return content