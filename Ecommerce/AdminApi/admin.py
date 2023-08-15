from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    fields = ['id', 'email', 'username', 'first_name', 'last_name']
    list_display = ['id', 'email', 'username', 'first_name', 'last_name']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['category_name']
    list_display = ['id','category_name']


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['product_name','description','price','stocky','available','image','offer']
    list_display = ['id','product_name','description','price','stock','available','image','offer']

    def categories_display(self, obj):
        return ", ".join([category.category_name for category in obj.categories.all()])

    categories_display.short_description = 'Categories'




# Register your models here.
