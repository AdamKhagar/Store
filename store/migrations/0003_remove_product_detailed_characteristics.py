# Generated by Django 3.1.7 on 2021-02-24 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20210224_1157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='detailed_characteristics',
        ),
    ]
