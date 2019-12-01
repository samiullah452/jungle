def alibaba(urls):
	import requests
	url = 'https://api.exchangerate-api.com/v4/latest/CNY'
	response = requests.get(url)	
	data = response.json()
	rate=data["rates"]["USD"]
	ratekrw=data["rates"]["KRW"]

	from bs4 import BeautifulSoup
	content={}
	i=0
	for url in urls:
		try:
			content[i]={}
			content[i]['group']='Uncategorized'			    
			content[i]['image']=[]
			content[i]['region']=urls[url]['region']
			response=requests.get(urls[url]['url'])
			soup = BeautifulSoup(response.content, 'html5lib')
			name = soup.findAll("div",{"class":'company-name-container'})
			for name in name:
				content[i]['shop-name']=' '.join((name.text).split())


			images=soup.findAll("div",{"class":"thumb"})
			j=0
			for image in images:
					if j==3:
						break
					imgs = image.find("img")['src']
					imgs.find(".jpg")
					if imgs.find(".jpg")!=-1:
						content[i]['image'].append(imgs[:imgs.find(".jpg")]+".jpg")
						j+=1
					elif imgs.find(".png")!=-1:
						content[i]['image'].append(imgs[:imgs.find(".png")]+".png")
						j+=1


			title = soup.findAll("h1",{"class":'ma-title'})
			for title in title:
			    content[i]['title']=title.text

			price = soup.findAll("div",{"class":'ma-price-wrap'})
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
				price = driver.findAll("div",{"class":'ma-reference-price-highlight'})
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
				price = soup.findAll("div",{"class":'pre-inquiry-price'})
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