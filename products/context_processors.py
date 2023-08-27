from django.contrib.auth.models import User



def get_basket_total(request):
    user = request.user
    discount_amount = []
    try:
        customer = User.objects.get(username=user.username)
    except Exception as e:
        return {'error': f'{e}', 'num_of_product': 0}
    if customer:
        query_set = customer.order_set.all()
        for obj in query_set:
            if obj.product.get_discount_price():
                discount = (obj.product.price - obj.product.get_discount_price()) * obj.quantity
                if discount:
                    discount_amount.append(float(discount))
        orders = [order.quantity for order in customer.order_set.all()]
        sub_total = [product.get_order_total() for product in customer.order_set.all()]
        if orders:
            return {'num_of_product': sum(orders), 'sub_total': sum(sub_total), 'discount_amount': str(sum(discount_amount))[0:-2]}
        return {'num_of_product': 0}
    
# discount_amount = 0
# amount = {'discount_amount': int(str(sum(discount_amount))[0:-2])}