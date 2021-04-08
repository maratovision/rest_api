from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from .models import *

#
# def get_pay(order_id):
#     obj = Order.objects.get(id=order_id)
#     card = obj.userprofile.cards.filter(status='default')[0]
#     if obj.payment_type == 'card' and obj.status != 'closed':
#         try:
#             card.balance -= obj.total_price
#             card.save()
#             obj.status = 'closed'
#             obj.save()
#         except IntegrityError:
#             return ValidationError('Not enough money')


# def count_order(order_id): my homework
#     order = Order.objects.get(id=order_id)
#     if order.status == 'closed':
#         order.worker.order_count += 1
#         if order.worker.order_count == 100:
#             order.worker.salary += 5000
#         if order.worker.order_count == 500:
#             order.worker.order_count += 10000
#         order.worker.save()

def worker_count_order(worker):
    len_worker_orders = Order.objects.filter(worker=worker, status='closed').count()
    worker.order_count = len_worker_orders
    worker.save()


def salary_increase(worker):
    if worker.order_count == 100:
        worker.salary += 5000
    elif worker.order_count == 200:
        worker.salary += 10000
    worker.save()