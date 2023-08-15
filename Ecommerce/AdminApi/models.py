from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name= models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255,unique=True)
    reset_password_token = models.CharField(max_length=100, null=True, blank=True)
    registration_date = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    def __str__(self):
        return self.email


class Category(models.Model):
    category_name = models.CharField(max_length=250, unique=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return '{}'.format(self.category_name)


class Product(models.Model):
    product_name = models.CharField(max_length=250, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    stock = models.PositiveIntegerField()
    available = models.BooleanField()
    image = models.ImageField(upload_to='product')
    offer = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    categories = models.ManyToManyField(Category)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.product_name

# Create your models here.
