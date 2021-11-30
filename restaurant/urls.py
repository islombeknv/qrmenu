from django.urls import path, re_path

from restaurant.views import *

app_name = 'menu'

urlpatterns = [
    path('', MTemplateView.as_view(), name='dashboard'),

    path('category/', CategoryListView.as_view(), name='category'),
    re_path(r'^category/delete/?option=\.', CategoryDelete, name='category-delete'),
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),

    path('product/create', MenuCreateView.as_view(), name='create'),
    path('product/list/', AdminMenuListView.as_view(), name='list'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    re_path(r'^product/delete/?option=\.', ProductDelete, name='product-delete'),

    path('table/list/', TableListView.as_view(), name='table-list'),
    path('table/create/', TableCreateView.as_view(), name='table-create'),
    re_path(r'^table/delete/?option=\.', TableDelete, name='table-delete'),
]
