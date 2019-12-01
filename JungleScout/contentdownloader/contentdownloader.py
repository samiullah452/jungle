def content(urls,website):
	content={}
	if website=='1688':
		import requests
		import urllib.request
		from bs4 import BeautifulSoup
		from dicttoxml import dicttoxml
		url = 'https://api.exchangerate-api.com/v4/latest/CNY'
		response = requests.get(url)	
		data = response.json()
		ratekrw=data["rates"]["KRW"]
		i=0
		for url in urls:
			index=url.find('?')
			xml={}
			xml['SearchItemsParameters']={}
			xml['SearchItemsParameters']["Provider"]="Alibaba1688"
			xml['SearchItemsParameters']["LanguageOfQuery"]="en"
			xml['SearchItemsParameters']['ItemTitle']=url[0:index]
			xml_str = dicttoxml(xml,attr_type=False)
			xml_str=str(xml_str)
			xml_str=xml_str[xml_str.find('<SearchItemsParameters>'):xml_str.find('</root>')]
			req = requests.get('http://otapi.net/OtapiWebService2.asmx/SearchItemsFrame?instanceKey=36bafd6e-baea-41e4-9e8d-4eb2436b0166&language=en&xmlParameters='+str(xml_str)+'&framePosition=0&frameSize=1')
			soup = BeautifulSoup(req.content,'xml')
			Items=soup.find("Items")
			itms=Items.findAll('Item')
			for item in itms:
				try:
					content[i]={}
					Itemid=item.find('Id')
					req = requests.get('http://otapi.net/OtapiWebService2.asmx/GetItemFullInfo?instanceKey=36bafd6e-baea-41e4-9e8d-4eb2436b0166&language=en&itemId='+Itemid.text)
					soup = BeautifulSoup(req.content,'xml')
					title=soup.find('OriginalTitle')
					content[i]['group']='Uncategorized'			    
					content[i]['title']=title.text
					pic=soup.find('MainPictureUrl')
					content[i]['image']=pic.text
					price=soup.find('OriginalPrice')
					content[i]['price']=round(float(price.text), 2)
					content[i]['price_krw']=round((ratekrw)*float(content[i]['price']), 2)					
					location=soup.find('Location')
					content[i]['region']=''
					if location.City is not None:
						content[i]['region']+=location.City.text+" "
					if location.State is not None:
							content[i]['region']+=location.State.text	
					if content[i]['region']=='':
						content[i]['region']="China"
					content[i]['details']=''
					weight=soup.find('ActualWeightInfo')
					if weight:
						content[i]['details']+="Weight:"+weight.Weight.text+'kg '
					promotions=soup.find('Promotions')
					if promotions:
						try:
							content[i]['details']+=promotions.Desciption.text+'\n'
						except:
							pass
					weight=soup.find('MasterQuantity')
					if weight:
						content[i]['details']+="Master Quantity:"+weight.text+' '
					weight=soup.find('FirstLotQuantity')
					if weight:
						content[i]['details']+="First Lot Quantity:"+weight.text+' '
					weight=soup.find('NextLotQuantity')
					if weight:
						content[i]['details']+="Next Lot Quantity:"+weight.text+' '
					weight=soup.find('DeliveryPrice')
					if weight:
						content[i]['details']+="Delivery Price:"+soup.find('DeliveryPrice').OriginalPrice.text+'¥'

					vendorid=soup.find('VendorId').text
					req = requests.get('http://otapi.net/OtapiWebService2.asmx/GetVendorInfo?instanceKey=36bafd6e-baea-41e4-9e8d-4eb2436b0166&language=en&vendorId='+vendorid)
					soup1 = BeautifulSoup(req.content,'xml')
					vendor=soup1.find('ShopName')
					if vendor is not None:
						content[i]['shop-name']=vendor.text
					else:
						vendor=soup1.find('DisplayName')						
						content[i]['shop-name']=vendor.text

					path="/jungle/media/products/"+content[i]['shop-name'].translate(str.maketrans('', '', string.punctuation))

					if not os.path.isdir(path):
						os.mkdir(path)

					path="/jungle/media/products/"+content[i]['shop-name'].translate(str.maketrans('', '', string.punctuation))+"/"+content[i]['title'].translate(str.maketrans('', '', string.punctuation))
					if not os.path.isdir(path):
						os.mkdir(path)

					pics=soup.findAll('ItemPicture')
					for j,pic in enumerate(pics):
						urllib.request.urlretrieve(pic.Url.text, "image"+str(j)+".jpg")

					vids=soup.findAll('Video')
					for j,vid in enumerate(vids):
						urllib.request.urlretrieve(vid["Url"], "video"+str(j)+".mp4")

					content[i]['url']=url
					i+=1
					break
				except Exception as e:
						print(e)		
						pass
	elif website=='Alibaba':
		import requests
		url = 'https://api.exchangerate-api.com/v4/latest/CNY'
		response = requests.get(url)	
		data = response.json()
		rate=data["rates"]["USD"]
		ratekrw=data["rates"]["KRW"]

		from selenium import webdriver
		import string
		import os
		import urllib.request
		from selenium.webdriver.chrome.options import Options
		import json
		options = Options()
		options.add_argument('--headless')
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')
		i=0
		driver = webdriver.Chrome('contentdownloader/chromedriver',options=options)
		for url in urls:
			try:
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
					images=driver.find_elements_by_xpath('//div[@class="iwrap nopic"]/a/img')
					for images in images:
					    content[i]['image']=images.get_attribute('src')



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
						if d=="/" or d=="$" or d.isalpha() or d==" ":
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
				content[i]['details']=''
				table = driver.find_elements_by_xpath('//div[@data-role="detail-tab-body"]')
				for table in table:
				    content[i]['details']+=table.text
				content[i]['url']=url

				path="/jungle/media/products/"+content[i]['shop-name'].translate(str.maketrans('', '', string.punctuation))

				if not os.path.isdir(path):
					os.mkdir(path)

				path="/jungle/media/products/"+content[i]['shop-name'].translate(str.maketrans('', '', string.punctuation))+"/"+content[i]['title'].translate(str.maketrans('', '', string.punctuation))
				if not os.path.isdir(path):
					os.mkdir(path)

				videos=driver.find_elements_by_xpath('//video')
				for j,video in enumerate(videos):
					urllib.request.urlretrieve(video.get_attribute('src'), path+"/video"+str(j)+".mp4")

				images=driver.find_elements_by_xpath('//div[@class="thumb"]/a/img')
				for j,image in enumerate(images):
					try:
						image.click()
						imgs = driver.find_elements_by_xpath('//div[@class="iwrap nopic"]/a/img')
						for img in imgs:
							urllib.request.urlretrieve(img.get_attribute('src'), path+"/image"+str(j)+'.jpg')
					except Exception as e:
						pass
				with open(path+'/text.txt', 'w') as f:
					f.write(json.dumps(content[i]))
				i+=1
			except Exception as e:
				print(e)

	elif website=="TAOBAO":
		import requests
		import urllib.request
		from urllib import parse
		from bs4 import BeautifulSoup
		from dicttoxml import dicttoxml
		url = 'https://api.exchangerate-api.com/v4/latest/CNY'
		response = requests.get(url)	
		data = response.json()
		ratekrw=data["rates"]["KRW"]
		i=0
		for url in urls:
			t = parse.parse_qs(parse.urlsplit(url).query)
			req = requests.get('http://otapi.net/OtapiWebService2.asmx/GetItemFullInfo?instanceKey=36bafd6e-baea-41e4-9e8d-4eb2436b0166&language=en&itemId='+t['id'][0])
			soup = BeautifulSoup(req.content,'xml')
			try:
				content[i]={}
				title=soup.find('OriginalTitle')
				content[i]['group']='Uncategorized'			    
				content[i]['title']=title.text
				pic=soup.find('MainPictureUrl')
				content[i]['image']=pic.text
				price=soup.find('OriginalPrice')
				content[i]['price']=round(float(price.text), 2)
				content[i]['price_krw']=round((ratekrw)*float(content[i]['price']), 2)					
				location=soup.find('Location')
				content[i]['region']=''
				if location.City is not None:
					content[i]['region']+=location.City.text+" "
				if location.State is not None:
						content[i]['region']+=location.State.text	
				if content[i]['region']=='':
					content[i]['region']="China"
				content[i]['details']=''
				weight=soup.find('ActualWeightInfo')
				if weight:
					content[i]['details']+="Weight:"+weight.Weight.text+'kg '
				promotions=soup.find('Promotions')
				if promotions:
					try:
						content[i]['details']+=promotions.Desciption.text+'\n'
					except:
						pass
				weight=soup.find('MasterQuantity')
				if weight:
					content[i]['details']+="Master Quantity:"+weight.text+' '
				weight=soup.find('FirstLotQuantity')
				if weight:
					content[i]['details']+="First Lot Quantity:"+weight.text+' '
				weight=soup.find('NextLotQuantity')
				if weight:
					content[i]['details']+="Next Lot Quantity:"+weight.text+' '
				weight=soup.find('DeliveryPrice')
				if weight:
					content[i]['details']+="Delivery Price:"+soup.find('DeliveryPrice').OriginalPrice.text+'¥'
					vendorid=soup.find('VendorId').text
				req = requests.get('http://otapi.net/OtapiWebService2.asmx/GetVendorInfo?instanceKey=36bafd6e-baea-41e4-9e8d-4eb2436b0166&language=en&vendorId='+vendorid)
				soup1 = BeautifulSoup(req.content,'xml')
				vendor=soup1.find('ShopName')
				if vendor is not None:
					content[i]['shop-name']=vendor.text
				else:
					vendor=soup1.find('DisplayName')						
					content[i]['shop-name']=vendor.text

				path="/jungle/media/products/"+content[i]['shop-name'].translate(str.maketrans('', '', string.punctuation))

				if not os.path.isdir(path):
					os.mkdir(path)

				path="/jungle/media/products/"+content[i]['shop-name'].translate(str.maketrans('', '', string.punctuation))+"/"+content[i]['title'].translate(str.maketrans('', '', string.punctuation))
				if not os.path.isdir(path):
					os.mkdir(path)

				pics=soup.findAll('ItemPicture')
				for j,pic in enumerate(pics):
					urllib.request.urlretrieve(pic.Url.text, "image"+str(j)+".jpg")

				vids=soup.findAll('Video')
				for j,vid in enumerate(vids):
					urllib.request.urlretrieve(vid["Url"], "video"+str(j)+".mp4")
				content[i]['url']=url
				i+=1
				break
			except Exception as e:
					print(e)		
					pass

	return content 
