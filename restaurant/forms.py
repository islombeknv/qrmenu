from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from restaurant.models import MenuModel, CategoryModel


class MenuForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = MenuModel
        exclude = ['created_at', 'user']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        exclude = ['updated_at', 'created_at', 'user']
