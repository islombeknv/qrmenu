from datetime import datetime
from io import BytesIO

import pytz
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
import qrcode
from django.core.files import File
from django.db import models

UserModel = get_user_model()


class Restaurant(models.Model):
    name = models.CharField(max_length=70)
    address1 = models.CharField(max_length=100)
    link = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserModel,
                             on_delete=models.CASCADE, related_name='restaurant')

    def save(self, *args, **kwargs):
        self.link = (get_random_string(length=32))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'restaurant'
        verbose_name_plural = 'restaurants'


class CategoryModel(models.Model):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserModel,
                             on_delete=models.CASCADE, related_name='category')

    def get_menu(self):
        return self.menu.count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class MenuModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='menu')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu")
    category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, related_name="menu", null=True)
    image = models.ImageField(upload_to='menu')
    name = models.CharField(max_length=70)
    price = models.IntegerField(default=0)
    real_price = models.FloatField(default=0)
    discount = models.IntegerField(default=0)
    description = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_discount(self):
        return self.discount != 0

    def get_price(self):
        if self.is_discount():
            return self.price - self.price * self.discount / 100
        else:
            return self.price

    def is_new(self):
        diff = datetime.now(pytz.timezone('Asia/Tashkent')) - self.created_at
        return diff.days <= 3

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'menu'
        verbose_name_plural = 'menu'


class TableModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='table')
    number = models.CharField(max_length=50)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        self.link = (get_random_string(length=32))
        qr = qrcode.QRCode(
            version=4,
            box_size=10,
            border=5,
        )
        qr.add_data(f'http://127.0.0.1:8000/menu/{self.restaurant.link}/?table={self.number}')
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        fname = f'{self.number}qrcode.png'
        buffer = BytesIO()
        img.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'table'
        verbose_name_plural = 'tables'
