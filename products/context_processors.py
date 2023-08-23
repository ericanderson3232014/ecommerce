from django.contrib.auth.models import User



def get_basket_total(request):
    try:
        user = request.user
        customer = User.objects.get(username=user.username)
    except Exception as e:
        return {'error': f'{e}', 'num_of_product': 0}
    if customer:
        orders = customer.order_set.all()
        if orders.exists():
            print(orders.count())
            return {'num_of_product': orders.count(), 'orders': orders}
        return {'num_of_product': 0}