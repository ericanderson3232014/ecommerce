from django.contrib.auth.models import User



def get_basket_total(request):
    user = request.user
    try:
        customer = User.objects.get(username=user.username)
    except Exception as e:
        return {'error': f'{e}', 'num_of_product': 0}
    if customer:
        orders = customer.order_set.all().count()
        sub_total = [product.get_order_total() for product in customer.order_set.all()]
        print(sum(sub_total))
        if orders:
            return {'num_of_product': orders, 'sub_total': sum(sub_total)}
        return {'num_of_product': 0}