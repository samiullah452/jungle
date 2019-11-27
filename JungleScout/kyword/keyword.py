def keyword_finder(URLS):
	from bs4 import BeautifulSoup
	import requests
	content={}
	i=0
	for url in URLS:
		try:
			req = requests.get(url)
			soup = BeautifulSoup(req.content, 'html.parser')

			content[i]={}
			content[i]['group']="Uncategorized"
			title=soup.find('title').text
			description=soup.find("meta" ,property='og:description').get('content')
			keyword=soup.find("meta" ,attrs={'name':'keywords'}).get('content')
			category=soup.find("script",attrs={'type':'application/ld+json'}).text
			start=category.find("category")+11
			end=category.find("offers")-3
			cat=category[start:end]
			ListCategory=cat.split('>')
			categorys=soup.find_all("script",attrs={'type':'text/javascript'})
			for category in categorys:
				a=category.text
				if len(category.attrs)==1 and a.find('lcatid')!=-1:
					c1=a.find('lcatid')
					c2=a.find('lcatnm')
					c3=a.find('mcatid')
					c4=a.find('mcatnm')
					c5=a.find('scatid')
					c6=a.find('scatnm')
					c7=a.find('if (typeof wcs !==')

					idstart2=c2+12
					idend2=c3-11
					name1=a[idstart2:idend2]

					idstart4=c4+12
					idend4=c5-11
					name2=a[idstart4:idend4]

					idstart6=c6+12
					idend6=idstart6+20
					name=a[idstart6:idend6]
					name3=name.split('"')
					content[i]['category_name']=name1+' '+name2+' '+name3[0]

					idstart1=c1+12
					idend1=c2-11
					id1=a[idstart1:idend1]

					idstart3=c3+12
					idend3=c4-11
					id2=a[idstart3:idend3]

					idstart5=c5+12
					idend5=c6-11
					id3=a[idstart5:idend5]
					content[i]['category_id']=id1+' '+id2+' '+id3
					content[i]['title']=title
					content[i]['description']=description
					content[i]['keywords']=keyword
					content[i]['url']=url
					i+=1
					break
		except:
			pass	
	return content