# Generated by Django 3.1.7 on 2021-03-04 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20210304_1509'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='cost',
            new_name='price',
        ),
    ]
