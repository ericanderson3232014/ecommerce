from django.contrib import admin
from .models import (
    ProductCategory, 
    Product, 
    ProductImage,
    ProductReview,
)



class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register( ProductCategory, ProductCategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'created', 'updated', 'available']
    search_fields = ['name', 'id']

admin.site.register(Product, ProductAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product']
    search_fields = ['product__name']

admin.site.register(ProductImage, ProductImageAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'rating', 'created', 'updated']

admin.site.register(ProductReview, ProductReviewAdmin)
