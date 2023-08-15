from django.contrib import admin
from UserApi import models


@admin.register(models.CartList)
class CartAdmin(admin.ModelAdmin):
    fields = ['user',]
    list_display = ['id','user_id']


@admin.register(models.CartItems)
class ItemsAdmin(admin.ModelAdmin):
    fields = ['cart','product','quantity',]
    list_display = ['id','cart_id','product_id','quantity',]


@admin.register(models.Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    fields = ['user','mobile', 'address','landmark','state','country', 'pincode', 'payment_amount','payment_method']
    list_display = ['id','user_id','mobile', 'address','landmark','state','country', 'pincode','payment_amount', 'payment_method','created_at']


@admin.register(models.OrderedItem)
class OrderAdmin(admin.ModelAdmin):
    fields = ['checkout','product','quantity','subtotal']
    list_display = ['id','checkout_id','product_id','quantity','subtotal']
# Register your models here.
