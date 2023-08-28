from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import (
    Product, 
    ProductImage,  
    ProductCategory,
    ProductReview,
    Order,
    Checkout,
    ShippingAddress,
)
from .forms import (
    CreateProductForm, 
    CreateProductImageForm, 
    ProductReviewForm,
    ShippingAddressForm,
)

from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.models import User


def home_view(request):
    user = request.user
    category = ProductCategory.objects.all()
    context = {'category': category}
    return render(request, 'products/home.html', context)


def product_list_view(request):
    query_set = Product.objects.all()
    laptops = query_set.filter(category__name__iexact='laptop')
    entry_level = laptops.filter(sub_category__name__iexact='entry level laptop')
    for query in query_set:
        obj = str(query.likes)
        if obj[2] == '0':
            query.likes = int(obj[0])
            query.save()
    for query in laptops:
        obj = str(query.likes)
        if obj[2] == '0':
            query.likes = int(obj[0])
            query.save()
    for query in entry_level:
        obj = str(query.likes)
        if obj[2] == '0':
            query.likes = int(obj[0])
            query.save()
    context = {'query_set': query_set[0:5], 'laptops':laptops[0:5], 'entry_level':entry_level}
    return render(request, 'products/product_list.html', context)


def product_detail_view(request, id):
    context = {}
    try:
        query = Product.objects.get(id=id)
        reviews = query.productreview_set.all()
        images = query.productimage_set.all()
    except Exception as e:
        messages.error(request, f'{e}')
        return redirect('products:home')
    obj = str(query.likes)
    if obj[2] == '0':
        query.likes = int(obj[0])
        query.save()
    context['query'] = query
    context['images'] = images
    context['reviews'] = reviews
    if request.user.is_authenticated:
        context['can_review'] = True
    return render(request, 'products/product_detail.html', context)


@login_required()
def product_create_view(request):
    image_form = CreateProductImageForm(request.POST or None, request.FILES or None)
    product_form = CreateProductForm(request.POST or None, request.FILES or None)
    context = {
        'product_form': product_form,
        'image_form': image_form
    }
    if image_form.is_valid() and product_form.is_valid():
        images = request.FILES.getlist('image')
        product = product_form.save()
        for img in images:
            ProductImage.objects.create(product=product, image=img)
    return render(request, 'products/product_create.html', context)


@login_required
def product_review_view(request, id):
    product = Product.objects.get(id=id)
    # here check if the user is verified buyer
    # purchased_item = Purchase.bojects.filter(product__id=id).first()
    # if purchased_item == True, then able to write review
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            author = request.user
            content = form.cleaned_data.get('content')
            rating = int(form.cleaned_data.get('rating'))
            title = form.cleaned_data.get('title')
            reveiw = ProductReview.objects.create(
                product=product, 
                author=author, 
                rating=rating, 
                title = title,
                content=content
            )
            product = Product.objects.get(id=id)
            product.likes = reveiw.calculate_rating()
            product.save()
            messages.success(request, f'{author.username}, thank you for the review!')
            return redirect('products:product-list')
        # print(form.errors)
        messages.error(request, 'There was an error. Try again later.')
        return redirect('products:product-review', id)
    return render(request, 'products/product_review.html', {'query': product})


def product_search_view(request):
    q = request.GET.get('q')
    query_set = Product.objects.filter(Q(category__name__icontains = q) | Q(sub_category__name__icontains = q) |Q(name__icontains = q))
    for query in query_set:
        obj = str(query.likes)
        if obj[2] == '0':
            query.likes = int(obj[0])
            query.save()
    context = {'query_set': query_set, 'q':q}
    return render(request, 'products/search_result.html', context)


@login_required
def add_to_basket_view(request, id):
    product = Product.objects.get(id=id)
    order = Order.objects.filter(customer=request.user ,product=product).first()
    if order:
        order.quantity += 1
        order.save()
        messages.success(request, f'{product.name} quantity has been updated.')
        return redirect('products:product-basket')
    else:
        Order.objects.create(customer=request.user, product=product, quantity=1)
        messages.success(request, f'{product.name} has been added to the basket.')
        return redirect('products:product-basket')


@login_required
def basket_view(request):
    user = request.user
    query_set = user.order_set.all()
    context = {'query_set': query_set}
    if not query_set.exists():
        messages.info(request, 'Your basket is empty.')
        return redirect('products:product-list')
    return render(request, 'products/basket.html', context)


@login_required
def update_basket_view(request, string):
    user = request.user
    qty = request.GET.get('amount')
    order = Order.objects.get(customer=user, product__name=string)
    if order.quantity == int(qty):
        order.delete()
        checkout = Checkout.objects.filter(customer=user).first()
        if checkout:
            checkout.set_amount_due()
            checkout.save()
        messages.success(request, f'{string} has been deleted from your basket.')
        return redirect('products:product-basket')
    order.quantity = int(qty)
    order.save()
    checkout = Checkout.objects.filter(customer=user).first()
    checkout.set_amount_due()
    messages.success(request, f'{string} quantity has been updated.')
    return redirect('products:product-basket')


@login_required
def checkout_view(request):
    user = request.user
    try:
        checkout = Checkout.objects.get(customer__username=user.username)
    except:
        checkout = Checkout.objects.create(customer=User.objects.get(username=user.username))
        orders = Order.objects.filter(customer__username=user.username)
        for product in orders:
            checkout.order.add(product)
        checkout.set_amount_due()
        return redirect('products:shipping-address')
    orders = Order.objects.filter(customer__username=user.username)
    for product in orders:
        checkout.order.add(product)
    checkout.set_amount_due()
    return redirect('products:shipping-address')


@login_required
def customer_address_view(request):
    instance = ShippingAddress.objects.filter(customer=request.user).first()
    form = ShippingAddressForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        shipping_address = form.save()
        shipping_address.customer = request.user
        shipping_address.save()
        return redirect('products:payment-center')
    return render(request, 'products/address.html', context)


@login_required 
def payment_center_view(request):
    checkout = Checkout.objects.filter(customer=request.user).first()
    query_set = checkout.order.all()
    context = {'checkout':checkout, 'query_set': query_set}
    return render(request, 'products/payment.html', context)