# Generated by Django 3.1.7 on 2021-03-14 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20210311_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productssubcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='store.productscategory'),
        ),
    ]