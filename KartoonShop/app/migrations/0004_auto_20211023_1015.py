# Generated by Django 3.2.8 on 2021-10-23 04:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_category_subcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='Category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='SubCategory',
        ),
    ]
