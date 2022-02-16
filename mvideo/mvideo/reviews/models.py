from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название товара')
    sku_id = models.CharField(max_length=50, verbose_name='id товара')
    rating = models.FloatField(verbose_name='Оценка')
    reviews_amount = models.IntegerField(verbose_name='Количество отзывов')
    url = models.CharField(max_length=255, verbose_name='Название товара')
    
    def __str__(self):
        return self.name

class Review(models.Model):
    review_id = models.CharField(max_length=150, verbose_name='ID комментария')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    name = models.CharField(max_length=150, verbose_name='Автор комментария')
    date = models.DateField(auto_now=True, verbose_name='Дата отзыва')
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)
    pros = models.TextField(verbose_name='Плюсы', blank=True, null=True)
    cons = models.TextField(verbose_name='Минусы', blank=True, null=True)
    likes = models.IntegerField(verbose_name='Лайки')
    dislikes = models.IntegerField(verbose_name='Дизлайки')
    rating = models.FloatField(verbose_name='Оценка')
# Create your models here.
