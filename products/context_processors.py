from django.contrib.auth.models import User
from .models import CheckoutReceipt


def get_basket_total(request):
    user = request.user
    discount_amount = []
    try:
        customer = User.objects.get(username=user.username)
    except Exception as e:
        return {'error': f'{e}', 'num_of_product': 0}
    if customer:
        query_set = customer.order_set.all().filter(open=True)
        for obj in query_set:
            if obj.product.get_discount_price():
                discount = (obj.product.price - obj.product.get_discount_price()) * obj.quantity
                if discount:
                    discount_amount.append(float(discount))
        orders = [order.quantity for order in customer.order_set.all().filter(open=True)]
        sub_total = [product.get_order_total() for product in customer.order_set.all().filter(open=True)]
        if orders:
            return {'num_of_product': sum(orders), 'sub_total': sum(sub_total), 'discount_amount': str(sum(discount_amount))[0:-2]}
        return {'num_of_product': 0}
    

def get_customer_receipt(request):
    customer = request.user
    try:
        receipt = CheckoutReceipt.objects.get(customer=customer, sent=False)
    except Exception as e:
       return {'error': f'{e}'}
    
    discount_amount = []
    orders = receipt.checkout.order.all()
    for order in orders:
        if order.product.get_discount_price():
            amount = (order.product.price - order.product.get_discount_price()) * order.quantity
            discount_amount.append(
                {
                    'name':order.product.name, 
                    'discount_amount': amount
                }
            )
    receipt.sent = True
    receipt.save()
    return {
        'receipt_id': receipt.id, 
        'customer': receipt.checkout.customer.username,
        'orders': orders, 
        'discount_amount': discount_amount,
        'total_amount_paid': receipt.checkout.total_amount_due
    }