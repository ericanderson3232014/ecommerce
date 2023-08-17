from django.urls import path 
from .views import (
    home_view,
    product_list_view,
    product_detail_view,
    product_create_view,
    product_review_view,
    product_search_view
)


app_name = 'products'



urlpatterns = [
    path('', home_view, name='product-home'),
    path('products/', product_list_view, name='product-list'),
    path('product/create/', product_create_view, name='product-create'),
    path('product/<uuid:id>/detail/', product_detail_view, name='product-detail'),
    path('product/<uuid:id>/review/',product_review_view, name='product-review' ),
    path('product/search/', product_search_view, name='product-search')
]