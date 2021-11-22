from io import BytesIO
from django.utils.crypto import get_random_string

import qrcode
from django.core.files import File
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=70)
    address1 = models.CharField(max_length=100)
    link = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.link = (get_random_string(length=32))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'restaurant'
        verbose_name_plural = 'restaurants'


class MenuModel(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name="menu")
    image = models.ImageField(upload_to='menu')
    name = models.CharField(max_length=70)
    price = models.IntegerField(default=0)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'menu'
        verbose_name_plural = 'menu'


class TableModel(models.Model):
    number = models.CharField(max_length=50)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        self.link = (get_random_string(length=32))
        qr = qrcode.QRCode(
            version=4,
            box_size=10,
            border=5,
        )
        qr.add_data(f'http://127.0.0.1:8000/menu/{self.restaurant.link}/')
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
