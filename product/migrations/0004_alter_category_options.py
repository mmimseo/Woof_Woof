# Generated by Django 4.1.1 on 2022-11-08 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_category_company_product_category_product_company'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]