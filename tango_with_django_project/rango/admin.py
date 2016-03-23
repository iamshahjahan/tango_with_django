from django.contrib import admin

# Register your models here.

from rango.models import Category,Page


class PageAdmin(admin.ModelAdmin):
	"""customization of admin panel"""
# adding title, category and url to the admin panel
	list_display = ('title','category','url')
	
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page,PageAdmin)