from django.urls import path
from .views import (
    AddCategoryView,
    AddProductView,EditProductView,DeleteProductView
)

urlpatterns = [
    path('category/add/', AddCategoryView.as_view(),name='add-category'),

    path('product/add/', AddProductView.as_view(),name='add-product'),
    path('product/edit/<int:pk>/', EditProductView.as_view(),name='edit-product'),
    path('product/delete/<int:pk>/', DeleteProductView.as_view(),name='delete-product'),
    ]