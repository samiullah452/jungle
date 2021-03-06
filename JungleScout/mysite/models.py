from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class profilePicture(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    profileImage = models.ImageField(upload_to = 'Image/Profiles/',blank=True , default="Image/Profiles/default.jpg")
    my_store_url=models.URLField()
    def __str__(self):
        return self.user.username


class profileModel(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    my_store_url=models.URLField()
    def __str__(self):
        return self.user.username


class content_downloader_groups(models.Model):
	name=models.CharField(max_length=255)
	user = models.ForeignKey(
      			get_user_model(),
     			 on_delete=models.CASCADE
    )

class user_content_downloader(models.Model):
	url=models.TextField()
	store_name=models.TextField()
	product_name=models.TextField()
	price=models.FloatField()
	price_krw=models.FloatField()
	image=models.TextField()
	name=models.ForeignKey(content_downloader_groups,on_delete=models.CASCADE)
	details=models.TextField()

class supplier_finder_groups(models.Model):
	name=models.CharField(max_length=255)
	user = models.ForeignKey(
      			get_user_model(),
     			 on_delete=models.CASCADE
    )

class user_supplier_finder(models.Model):
	url=models.TextField()
	store_name=models.TextField()
	product_name=models.TextField()
	price=models.FloatField()
	price_krw=models.FloatField()
	name=models.ForeignKey(supplier_finder_groups,on_delete=models.CASCADE)
	region=models.TextField()

class supplier_finder_image(models.Model):
	src=models.TextField()
	supplier=models.ForeignKey(user_supplier_finder,on_delete=models.CASCADE)


class keyword_groups(models.Model):
	name=models.CharField(max_length=255)
	user = models.ForeignKey(
      			get_user_model(),
     			 on_delete=models.CASCADE
    )

class user_keywords(models.Model):
	url=models.TextField()
	category_name=models.TextField()
	product_name=models.TextField()
	category_id=models.TextField()
	keywords=models.TextField()
	name=models.ForeignKey(keyword_groups,on_delete=models.CASCADE)
	details=models.TextField()

class profit_groups(models.Model):
	name=models.CharField(max_length=255)
	user = models.ForeignKey(
      			get_user_model(),
     			 on_delete=models.CASCADE
    )

class user_profit(models.Model):
	product_name=models.TextField()
	buying_price_min=models.FloatField(default=0)
	buying_price_max=models.FloatField(default=0)
	buying_price_avg=models.FloatField(default=0)
	exchange_rate=models.FloatField(default=167.43)
	oversea_shipping=models.FloatField(default=0)
	roi=models.FloatField(default=100)
	sales_goal=models.IntegerField(default=1)
	commision=models.FloatField(default=0)
	tax_rate=models.FloatField(default=0)
	vat=models.FloatField(default=0)
	local_delievery_cost=models.FloatField(default=0)
	extra_cost=models.FloatField(default=0)
	name=models.ForeignKey(profit_groups,on_delete=models.CASCADE)
	
