# Generated by Django 3.2.12 on 2022-02-15 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220215_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_id',
            field=models.CharField(default=1, max_length=150, verbose_name='ID комментария'),
            preserve_default=False,
        ),
    ]
