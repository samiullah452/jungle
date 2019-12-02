from SupplierFinders.alibaba import alibaba

def test(keys,website):
	content={}
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
			xml['ImageUrl']=key
			print(key)
			xml_str = dicttoxml(xml,attr_type=False)
			xml_str=str(xml_str)
			print(xml_str)
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
		from pathlib import Path
		import re
		
		from selenium.webdriver.chrome.options import Options
		options = Options()
		options.add_argument('--headless')		
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')
		browser = webdriver.Chrome('contentdownloader/chromedriver',options=options)
		i=0
		urls={}
		url =  'https://www.alibaba.com/'
		browser.implicitly_wait(20)
		for key in keys:
			content[i]={}
			content[i]['key']=key
			browser.get(url)
			element = browser.find_element_by_class_name("ui-searchbar-imgsearch-icon")
			browser.execute_script("arguments[0].click();", element)
			input = browser.find_element_by_xpath("//input[@type='file']")
			browser.execute_script("arguments[0].style.display = 'block';", input)
			path = str(Path(key))

			input.send_keys(path)
			        
			while url == browser.current_url:
			        time.sleep(1)
			time.sleep(3)

			for company_detali in browser.find_elements_by_xpath('//div[@class="bc-ife-gallery-item-title bc-ife-gallery-item-title-line2"]/a'):
				region='China'
				try:
					urls[i]={}
					urls[i]['region']=region
					urls[i]['url']=company_detali.get_attribute('href')
					i+=1
				except Exception as e:
					print(e)
					pass
		supplier=alibaba(urls)
		return supplier
 