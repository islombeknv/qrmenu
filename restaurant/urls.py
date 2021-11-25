from django.urls import path, re_path

from restaurant.views import *

app_name = 'menu'

urlpatterns = [
    path('', MTemplateView.as_view()),

    path('category/', CategoryListView.as_view(), name='category'),

    re_path(r'^category/delete/?option=\.', CategoryDelete, name='category-delete'),

    path('category/create/', CategoryCreateView.as_view(), name='category-create'),

    path('create/menu/', MenuCreateView.as_view(), name='create'),
]
