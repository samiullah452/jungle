from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(profilePicture)

admin.site.register(content_downloader_groups)
admin.site.register(user_content_downloader)

admin.site.register(supplier_finder_groups)
admin.site.register(user_supplier_finder)
admin.site.register(supplier_finder_image)

admin.site.register(profit_groups)
admin.site.register(user_profit)

admin.site.register(keyword_groups)
admin.site.register(user_keywords)
