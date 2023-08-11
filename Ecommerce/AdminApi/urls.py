from django.urls import path
from .views import (
    UserListView,UserDeleteView,
    AddCategoryView,
    AddProductView,EditProductView,DeleteProductView
)

urlpatterns = [
    path('user/list/', UserListView.as_view(),name='user-list'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(),name='user-delete'),

    path('category/add/', AddCategoryView.as_view(),name='add-category'),

    path('product/add/', AddProductView.as_view(),name='add-product'),
    path('product/edit/<int:pk>/', EditProductView.as_view(),name='edit-product'),
    path('product/delete/<int:pk>/', DeleteProductView.as_view(),name='delete-product'),
    ]