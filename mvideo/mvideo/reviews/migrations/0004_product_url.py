# Generated by Django 3.2.12 on 2022-02-16 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_review_review_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='url',
            field=models.CharField(default=1, max_length=255, verbose_name='Название товара'),
            preserve_default=False,
        ),
    ]
