from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import uuid




class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Product Categories'



class ProductSubCategory(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Product Sub-Categories'
        ordering = ['name']



class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, blank=True, null=True)
    product_image = models.ImageField(upload_to='product_image', null=True, blank=True)
    description = models.TextField(max_length=300)
    detail = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    num_of_times_solid = models.IntegerField(default=0)
    likes = models.DecimalField(max_digits=5, decimal_places=1 ,default=0.0)

    def __str__(self):
        return self.name
    
    def get_product_image_url(self):
        return self.product_image.url
    
    def get_absolute_url(self):
        return reverse('products:product-detail', args=[str(self.id)])
    
    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Products'



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name_plural = 'Product Images'



class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name
    
    def calculate_rating(self):
        reviews = ProductReview.objects.filter(product__id = self.product.id)
        total_reviews = reviews.count()
        added_review = sum([review.rating for review in reviews])
        rating_average = (added_review / ( total_reviews * 5)) * 5
        return rating_average
    
    class Meta:
        ordering = ['-created']