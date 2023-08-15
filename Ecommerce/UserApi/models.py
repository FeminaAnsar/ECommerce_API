from django.db import models
from AdminApi.models import User,Product


class CartList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    ORDER_STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    )
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='processing')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.user.email


class CartItems(models.Model):
    cart = models.ForeignKey(CartList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '{}'.format(self.product)


class Checkout(models.Model):
    CHOICES = (
                (1, 'COD (Cash On Delivery)'),
                (2, 'UPI ID(GPay,Paytm, etc'),
                (3, 'Credit / Debit Card'),
                (4, 'Net Banking')
            )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.TextField(max_length=15)
    address = models.TextField()
    landmark = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    country = models.TextField(max_length=255)
    pincode = models.CharField(max_length=100)
    payment_amount = models.FloatField(default=0)
    payment_method = models.IntegerField(choices=CHOICES)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['id', ]

    def __str__(self):
        return self.user.email


class OrderedItem(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.FloatField()

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} - {self.subtotal}"

# Create your models here.
