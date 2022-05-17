from django.urls import path
from .views import ExpenseList, ExpenseDetail

urlpatterns = [
    path("", ExpenseList.as_view(), name="expenses"),
    path("<int:id>/", ExpenseDetail.as_view(), name="expense_detail")
]