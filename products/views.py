from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.utils import timezone
from .models import (
    Product, 
    ProductImage,  
    ProductCategory,
    ProductReview,
    Order,
    Checkout,
    ShippingAddress,
    CheckoutReceipt,
)
from .forms import (
    CreateProductForm, 
    CreateProductImageForm, 
    ProductReviewForm,
    ShippingAddressForm,
)

from django.conf import settings
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

def home_view(request):
    category = ProductCategory.objects.all()
    products = Product.objects.all()
    for product in products:
        product.save()
    context = {'category': category}
    return render(request, 'products/home.html', context)


def product_list_view(request):
    query_set = Product.objects.all()
    laptops = query_set.filter(category__name__iexact='laptop')
    entry_level = laptops.filter(sub_category__name__iexact='entry-level')
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
def write_product_review_view(request, id):
    product = Product.objects.get(id=id)
    user = request.user
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
            return redirect('products:product-detail', id)
        print(form.errors)
        messages.error(request, 'There was an error. Try again later.')
        return redirect('products:product-review', id)
    else:
        checkouts = Checkout.objects.filter(customer=user, open=False)
        if not checkouts.exists():
            messages.error(request, 'You are not authorized to write review on this product.')
            return redirect('products:product-detail', id)
        elif checkouts.exists():
            purchase_verified = []
            for checkout in checkouts:
                orders = checkout.order.all().filter(product=product)
                for order in orders:
                    if order.product == product:
                        purchase_verified.append(order)
            print('PURCHASE VERIFIED:', purchase_verified)
            if purchase_verified:
                return render(request, 'products/product_review.html', {'query': product})
            else:
                messages.error(request, 'You are not authorized to write review on this product.')
                return redirect('products:product-detail', id)
    
    
def product_search_view(request):
    q = request.GET.get('q')
    query_set = Product.objects.filter(Q(category__name__icontains = q) | 
                                       Q(sub_category__name__icontains = q) |
                                       Q(name__icontains = q))
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
    order = Order.objects.filter(customer=request.user ,product=product, open=True).first()
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
    query_set = user.order_set.all().filter(open=True)
    context = {'query_set': query_set}

    if not query_set.exists():
        messages.info(request, 'Your basket is empty.')
        return redirect('products:product-list')
    
    return render(request, 'products/basket.html', context)


@login_required
def update_basket_view(request, string):
    user = request.user
    qty = request.GET.get('amount')
    order = Order.objects.get(customer=user, product__name=string, open=True)

    if order.quantity == int(qty):
        order.delete()
        checkout = Checkout.objects.filter(customer=user, open=True).first()
        if checkout:
            checkout.set_amount_due()
            checkout.save()
        messages.success(request, f'{string} has been deleted from your basket.')
        return redirect('products:product-basket')
    
    order.quantity = int(qty)
    order.save()

    messages.success(request, f'{string} quantity has been updated.')
    return redirect('products:product-basket')


@login_required
def checkout_view(request):
    user = request.user
    try:
        checkout = Checkout.objects.get(customer__username=user.username, open=True)
    except:
        checkout = Checkout.objects.create(customer=User.objects.get(username=user.username))
        orders = Order.objects.filter(customer__username=user.username, open=True)
        for product in orders:
            checkout.order.add(product)
        checkout.set_amount_due()
        return redirect('products:shipping-address')
    
    orders = Order.objects.filter(customer__username=user.username, open=True)

    for product in orders:
        checkout.order.add(product)

    checkout.set_amount_due()

    return redirect('products:shipping-address')


@login_required
def customer_address_view(request):
    instance = ShippingAddress.objects.filter(customer=request.user).first()
    form = ShippingAddressForm(instance=instance)
    context = {'form': form}

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=instance)
        if form.is_valid():
            shipping_address = form.save()
            shipping_address.customer = request.user
            shipping_address.save()
            return redirect('products:checkout-summary')
        else:
            context['form'] = form
    return render(request, 'products/address.html', context)


@login_required 
def checkout_summary_view(request):
    checkout = Checkout.objects.filter(customer=request.user, open=True).first()

    if not checkout:
        messages.error(request, 'You do not have any pending orders.')
        return redirect('products:product-list')
    
    query_set = checkout.order.all()
    context = {'checkout':checkout, 'query_set': query_set}
    return render(request, 'products/checkout_summary.html', context)


@login_required 
def create_checkout_session_view(request, id):
    DOMAIN = 'http://127.0.0.1:8000/'

    try:
        checkout_obj = Checkout.objects.get(id=id, open=True)
    except:
        messages.error(request, 'You do not have any pending orders.')
        return redirect('products:product-list')
    
    amount_due = int((checkout_obj.total_amount_due) * 100)
    print(amount_due)
    checkout_session = stripe.checkout.Session.create(
        line_items=[{ 
                'price_data': { 
                    'currency': 'php', 
                    'unit_amount': f'{amount_due}',
                    'product_data':{ 
                        'name': 'Total amount due'
                        }, 
                },
                'quantity': 1
            }],
        metadata={'receipt_url': 'http://127.0.0.1:8000/payment/success/7/'},
        mode='payment',
        success_url=DOMAIN + f'payment/success/{id}/',
        cancel_url=DOMAIN + 'payment/cancel/',
    )
    return redirect(checkout_session.url, code=303)


@login_required
def payment_cancel_view(request):
    return render(request, 'products/payment_cancel.html')


@login_required
def payment_success_view(request, id):
    DOMAIN = 'http://127.0.0.1:8000'
    customer = request.user
    orders = customer.order_set.filter(open=True)
    checkout_obj = Checkout.objects.filter(id=id, open=True).first()

    if not orders.exists() and not checkout_obj:
        messages.error(request, 'You do not have any pending orders.')
        return redirect('products:product-list')
    
    your_purchase = ''

    for item in checkout_obj.order.all():
        discount = ''
        if item.product.get_discount_price():
            discount = item.product.price - item.product.get_discount_price()
        else:
            discount = 0
        your_purchase += f'''
        Customer: {checkout_obj.customer.username},
        Product name: {item.product.name}, 
        Price: P{item.product.price}, 
        Discount price: P{item.product.get_discount_price()},
        Discount amount: P{discount}, 
        Quantity: {item.quantity},
        item_url: {DOMAIN}{item.product.get_absolute_url()}
        --------------------------------------------------
        '''
    your_purchase += f'Amount paid: {checkout_obj.set_amount_due()}'

    receipt = CheckoutReceipt.objects.create(
        checkout=checkout_obj, 
        customer=customer, 
        checkout_summary=your_purchase
    )
    address = ShippingAddress.objects.get(customer=request.user)
    email_from = settings.EMAIL_HOST_USER

    send_mail(
        subject = 'Your ordered items',
        message = f'''Thank you for shopping at AiAi Market. Here is your receipt:
                        \nReceipt ID: {receipt.id}{receipt.checkout_summary}
                ''',
        recipient_list = [address.email],
        from_email = email_from
    )

    receipt.receipt_sent_date = timezone.now()
    # receipt.sent = True
    receipt.save()

    for order in orders:
        order.open = False
        order.save()
    checkout_obj.open = False
    checkout_obj.checkout_date = timezone.now()
    checkout_obj.save()
    discount = []
    for order in checkout_obj.order.all():
        if order.product.get_discount_price():
            discount.append(
                {
                    'discount' : order.product.price - order.product.get_discount_price(),
                    'name' : order.product.name
                }
            )

    context = {
        'domain': DOMAIN
    }
    return render(request, 'products/payment_success.html', context)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        line_items = session.line_items

        print(session)

        # customer_email = session['customer_details']['email']
        # receipt_url = session['metadata']["receipt_url"]
        # email_from = settings.EMAIL_HOST_USER
        # send_mail(
        #     subject = 'Your ordered items',
        #     message = f'Thank you for shopping at AiAi Market. Here is your receipt @{receipt_url}',
        #     recipient_list = [customer_email],
        #     from_email = email_from
        # )
    return HttpResponse(status=200)