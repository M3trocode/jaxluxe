# Generated by Django 4.2.7 on 2023-12-23 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_category_options_product_in_stock_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
        migrations.RemoveField(
            model_name='category',
            name='image',
        ),
    ]