from django.urls import path
from .views import IncomeList, IncomeDetail

urlpatterns = [
    path("", IncomeList.as_view(), name="incomes"),
    path("<int:id>/", IncomeDetail.as_view(), name="income_detail")
]