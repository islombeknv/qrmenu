from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from restaurant.models import MenuModel, CategoryModel, TableModel


class MenuForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = MenuModel
        exclude = ['created_at', 'user', 'real_price']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        exclude = ['updated_at', 'created_at', 'user']


class TableForm(forms.ModelForm):
    class Meta:
        model = TableModel
        exclude = ['updated_at', 'created_at', 'user', 'restaurant', 'qr_code']