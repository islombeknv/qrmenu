# Generated by Django 3.2.9 on 2021-11-27 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_alter_menumodel_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='menumodel',
            name='discount',
            field=models.IntegerField(default=0),
        ),
    ]
