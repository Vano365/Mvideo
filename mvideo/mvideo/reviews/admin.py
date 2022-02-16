from django.contrib import admin
from .models import Review, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'sku_id', 'reviews_amount')
    search_fields = ['name', 'sku_id']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'date', 'rating', 'likes', 'dislikes')
    search_fields = ['product__name', 'product__sku_id']

admin.site.register(Review, ReviewAdmin)
admin.site.register(Product, ProductAdmin)
# Register your models here.
