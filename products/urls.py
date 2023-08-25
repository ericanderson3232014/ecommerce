from django.urls import path 
from .views import (
    home_view,
    product_list_view,
    product_detail_view,
    product_create_view,
    product_review_view,
    product_search_view,
    add_to_basket_view,
    basket_view,
    update_basket_view,
    checkout_view,
)


app_name = 'products'



urlpatterns = [
    path('', home_view, name='product-home'),
    path('products/', product_list_view, name='product-list'),
    path('product/create/', product_create_view, name='product-create'),
    path('product/<uuid:id>/detail/', product_detail_view, name='product-detail'),
    path('product/<uuid:id>/review/',product_review_view, name='product-review' ),
    path('product/search/', product_search_view, name='product-search'),
    path('product/<uuid:id>/add-to-basket/', add_to_basket_view, name='add-to-basket'),
    path('my/basket/', basket_view, name='product-basket'),
    path('update/<str:str>/qty', update_basket_view, name='update-basket'),
    path('checkout/', checkout_view, name='checkout')
]