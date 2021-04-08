from django.urls import path
from .views import *

urlpatterns = [
    path('order/', OrderView.as_view(), name='order'),
    path('table/', TableView.as_view()),
    path('table/<str:table_area>', TableDetailView.as_view()),
    path('employee/', EmployeeView.as_view()),
    path('order/<int:order_id>/', ModifyOrderView.as_view(), name= 'update'),
    path('close/<int:order_id>/', AdminUserPutOrder.as_view())
]