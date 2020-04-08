from SupplierFinders.alibaba import alibaba

def supplier(keys,website):
	if website=='1688':
		import requests
		from bs4 import BeautifulSoup
		from dicttoxml import dicttoxml
		url = 'https://api.exchangerate-api.com/v4/latest/CNY'
		response = requests.get(url)	
		data = response.json()
		ratekrw=data["rates"]["KRW"]
		content={}
		i=0
		for key in keys:
			xml={}
			xml['SearchItemsParameters']={}
			xml['SearchItemsParameters']["Provider"]="Alibaba1688"
			xml['SearchItemsParameters']["LanguageOfQuery"]="en"
			xml['SearchItemsParameters']['ItemTitle']=key
			xml_str = dicttoxml(xml,attr_type=False)
			xml_str=str(xml_str)
			xml_str=xml_str[xml_str.find('<SearchItemsParameters>'):xml_str.find('</root>')]
			req = requests.get('http://otapi.net/OtapiWebService2.asmx/SearchItemsFrame?instanceKey=36bafd6e-baea-41e4-9e8d-4eb2436b0166&language=en&xmlParameters='+str(xml_str)+'&framePosition=0&frameSize=40')
			soup = BeautifulSoup(req.content,'xml')
			Items=soup.find("Items")
			itms=Items.findAll('Item')
			for item in itms:
				try:
					content[i]={}
					title=item.find('OriginalTitle')
					content[i]['group']='Uncategorized'			    
					content[i]['title']=title.text
					content[i]['image']=[]	
					pics=item.findAll('ItemPicture')
					for j,pic in enumerate(pics):
						if j==3:
						    break
						content[i]['image'].append(pic.Url.text)
					price=item.find('OriginalPrice')
					content[i]['price']=round(float(price.text), 2)
					content[i]['price_krw']=round((ratekrw)*float(content[i]['price']), 2)					
					location=item.find('Location')
					content[i]['region']=''
					if location.City is not None:
						content[i]['region']+=location.City.text+" "
					if location.State is not None:
							content[i]['region']+=location.State.text	
					if content[i]['region']=='':
						content[i]['region']="China"
					vendorid=item.find('VendorId').text
					req = requests.get('http://otapi.net/OtapiWebService2.asmx/GetVendorInfo?instanceKey=36bafd6e-baea-41e4-9e8d-4eb2436b0166&language=en&vendorId='+vendorid)
					soup = BeautifulSoup(req.content,'xml')
					vendor=soup.find('ShopName')
					if vendor is not None:
						content[i]['shop-name']=vendor.text
					else:
						vendor=soup.find('DisplayName')						
						content[i]['shop-name']=vendor.text
					url=item.find('ExternalItemUrl')
					content[i]['url']=url.text
					i+=1
				except Exception as e:
						print(e)		
						pass
		return content
	
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
		urls={}
		driver= webdriver.Chrome('contentdownloader/chromedriver',options=options)
		driver.get('https://www.alibaba.com/corporations/watch.html')
		i=0
		for key in keys:
			time.sleep(5)
			Send = driver.find_element_by_name('SearchText')
			Send.clear()
			Send.send_keys(key)
			button = driver.find_element_by_xpath('//*[@id="J_SC_header"]/header/div[2]/div[2]/div/div[1]/form/input[4]').click()
			for company_detali in driver.find_elements_by_xpath('//div[@class="item-main"]'):
				name=company_detali.find_elements_by_xpath('.//*[@class="ellipsis search"]')
				region=name[0].text
				try:
					link = company_detali.find_element_by_xpath('.//*[@class="img-thumb"]/a')
					urls[i]={}
					urls[i]['region']=region
					urls[i]['url']=link.get_attribute('href')
					i+=1
				except Exception as e:
					pass
		supplier=alibaba(urls)
		return supplier		   