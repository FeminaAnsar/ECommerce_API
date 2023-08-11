from django.urls import path
from .views import (
    RegisterView, ResetRequestView, ResetConfirmView,
    CategoryListView,ProductListView,ProductDetailView
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    path('reset-password/request/', ResetRequestView.as_view(), name='password_reset_request'),
    path('reset-password/confirm/<str:reset_token>/', ResetConfirmView.as_view(), name='password_reset_confirm'),

    path('category/list/',CategoryListView.as_view(),name='category_list'),
    path('product/list/',ProductListView.as_view(),name='category_list'),
    path('product/detail/<int:pk>',ProductDetailView.as_view(),name='category_list')

]
