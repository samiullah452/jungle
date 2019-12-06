def profitcal(files,website):
	content={}
	i=0
	if website=='1688':
		import requests
		from bs4 import BeautifulSoup
		from dicttoxml import dicttoxml
		content={}
		i=0
		for file in files:
			xml={}
			xml['SearchItemsParameters']={}
			xml['SearchItemsParameters']["Provider"]="Alibaba1688"
			xml['SearchItemsParameters']["LanguageOfQuery"]="en"
			xml['SearchItemsParameters']['ImageUrl']=file
			xml_str = dicttoxml(xml,attr_type=False)
			xml_str=str(xml_str)
			xml_str=xml_str[xml_str.find('<SearchItemsParameters>'):xml_str.find('</root>')]
			req = requests.get('http://otapi.net/OtapiWebService2.asmx/SearchItemsFrame?instanceKey=36bafd6e-baea-41e4-9e8d-4eb2436b0166&language=en&xmlParameters='+str(xml_str)+'&framePosition=0&frameSize=40')
			soup = BeautifulSoup(req.content,'xml')
			Items=soup.find("Items")
			itms=Items.findAll('Item')
			content[i]={}
			content[i]['group']='Uncategorized'			    
			price_list=[]
			for item in itms:
					if 'title' not in content[i]:
						title=item.find('OriginalTitle')
						content[i]['title']=title.text
					price=item.find('OriginalPrice')
					price_list.append(round(float(price.text), 2))
			if len(price_list):
				minimum = min(price_list) 
				maximum = max(price_list)
				average = round(sum(price_list)/len(price_list) ,2)       

			else:
				minimum=0
				maximum=0
				average=0


			content[i]['min']=minimum
			content[i]['max']=maximum
			content[i]['avg']=average
			i+=1
		return content

	if website=='TAOBAO':
		import requests
		from bs4 import BeautifulSoup
		from dicttoxml import dicttoxml
		content={}
		i=0
		for file in files:
			xml={}
			xml['SearchItemsParameters']={}
			xml['SearchItemsParameters']["Provider"]="Taobao"
			xml['SearchItemsParameters']["LanguageOfQuery"]="en"
			xml['SearchItemsParameters']['ImageUrl']=file
			xml_str = dicttoxml(xml,attr_type=False)
			xml_str=str(xml_str)
			xml_str=xml_str[xml_str.find('<SearchItemsParameters>'):xml_str.find('</root>')]
			req = requests.get('http://otapi.net/OtapiWebService2.asmx/SearchItemsFrame?instanceKey=36bafd6e-baea-41e4-9e8d-4eb2436b0166&language=en&xmlParameters='+str(xml_str)+'&framePosition=0&frameSize=40')
			soup = BeautifulSoup(req.content,'xml')
			Items=soup.find("Items")
			itms=Items.findAll('Item')
			content[i]={}
			content[i]['group']='Uncategorized'			    
			price_list=[]
			for item in itms:
					if 'title' not in content[i]:
						title=item.find('OriginalTitle')
						content[i]['title']=title.text
					price=item.find('OriginalPrice')
					price_list.append(round(float(price.text), 2))

			if len(price_list):
				minimum = min(price_list) 
				maximum = max(price_list)
				average = round(sum(price_list)/len(price_list) ,2)       
			else:
				minimum=0
				maximum=0
				average=0


			content[i]['min']=minimum
			content[i]['max']=maximum
			content[i]['avg']=average
			i+=1

		return content

	if website=="Alibaba":
		import requests
		url = 'https://api.exchangerate-api.com/v4/latest/CNY'
		response = requests.get(url)	
		data = response.json()
		rate=data["rates"]["USD"]

		from selenium import webdriver
		#from selenium.webdriver.firefox.options import Options
		import subprocess
		import time
		from pathlib import Path
		import re
		
		from selenium.webdriver.chrome.options import Options
		options = Options()
		options.add_argument('--headless')		
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')
		browser = webdriver.Chrome('contentdownloader/chromedriver',options=options)
		
		url =  'https://www.alibaba.com/'
		#firefox_options = Options()
		#firefox_options.add_argument('-headless')
		#profile = webdriver.FirefoxProfile()
		#profile.set_preference("dom.file.createInChild",True)
		#firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
		#firefox_capabilities['marionette'] = True
#		browser = webdriver.Firefox(executable_path='profitcalculator/geckodriver',firefox_options=firefox_options,firefox_profile = profile,capabilities=firefox_capabilities)
		browser.implicitly_wait(20)
		for file in files:
			content[i]={}
			content[i]['group']='Uncategorized'			    
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


			title = browser.find_element_by_class_name('bc-ife-gallery-item-title')
			content[i]['title']=title.text

			prices = browser.find_elements_by_class_name('bc-ife-gallery-price')
			p = []
			for prices in prices:
			    P = re.findall("\d{1,10}\.\d{2}",prices.text)
			    for pr in P:
			        p.append(round( (1/rate)*float(pr),2 ) )
			if len(p):
				minimum = min(p) 
				maximum = max(p)
				average = round(sum(p)/len(p) ,2)       

			else:
				minimum=0
				maximum=0
				average=0

			content[i]['min']=minimum
			content[i]['max']=maximum
			content[i]['avg']=average
			i+=1
		return content
