from django.contrib import admin
from .models import (
    ProductCategory, 
    Product, 
    ProductImage,
    ProductReview,
    ProductSubCategory
)



class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register( ProductCategory, ProductCategoryAdmin)


class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(ProductSubCategory, ProductSubCategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'sub_category', 'created', 'updated', 'available']
    search_fields = ['name', 'category__name', 'sub_category__name']

admin.site.register(Product, ProductAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product']
    search_fields = ['product__name']

admin.site.register(ProductImage, ProductImageAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'rating', 'created', 'updated']

admin.site.register(ProductReview, ProductReviewAdmin)
