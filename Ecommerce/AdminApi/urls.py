from django.urls import path
from .views import (
    UserListView,UserDeleteView,
    AddCategoryView,EditCategoryView,
    AddProductView,EditProductView,DeleteProductView,
    OrderListView,OrderDetailView,OrderStatusUpdateView,
    PromotionalMail
)

urlpatterns = [
    path('user/list/', UserListView.as_view(),name='user-list'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(),name='user-delete'),

    path('category/add/', AddCategoryView.as_view(),name='add-category'),
    path('category/edit/<int:pk>', EditCategoryView.as_view(),name='edit-category'),

    path('product/add/', AddProductView.as_view(),name='add-product'),
    path('product/edit/<int:pk>/', EditProductView.as_view(),name='edit-product'),
    path('product/delete/<int:pk>/', DeleteProductView.as_view(),name='delete-product'),

    path('order/list/',OrderListView.as_view(),name='order-list'),
    path('order/detail/',OrderDetailView.as_view(),name='order-detail'),
    path('order/status-update/',OrderStatusUpdateView.as_view,name='order-status-update'),

    path('send-promotional-mail/',PromotionalMail.as_view(),name='promotional-mail')
    ]