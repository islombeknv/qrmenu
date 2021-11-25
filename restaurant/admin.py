from django.contrib import admin

from restaurant.models import MenuModel, Restaurant, TableModel, CategoryModel

admin.site.register(TableModel)
admin.site.register(CategoryModel)
admin.site.register(MenuModel)
admin.site.register(Restaurant)
