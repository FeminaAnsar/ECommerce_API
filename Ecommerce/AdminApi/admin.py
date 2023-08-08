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
    fields = ['category','product_name','description','price','stock','available','image','offer']
    list_display = ['id','category_id','product_name','description','price','stock','available','image','offer']


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    fields = ['user','address','mobile']
    list_display = ['user','address','mobile']


# Register your models here.
