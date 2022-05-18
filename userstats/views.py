from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from datetime import datetime, date, timedelta
from expenses.models import Expense
from income.models import Income

# Create your views here.
class ExpenseSummaryStats(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        today = date.today()
        a_year_ago = today - timedelta(days=365)

        expenses = Expense.objects.filter(owner=request.user)

        final = {}
        categories = list(map(self.get_category, expenses))

        print(categories)

        for expense in expenses:
            for category in categories:
                final[category] = self.get_amount_for_category(expenses, category)
        
        return JsonResponse({'category_data' : final}, status=status.HTTP_200_OK)
    
    def get_category(self, expense):
        return expense.category
    
    def get_amount_for_category(self, expenses, category):
        expenses = expenses.filter(category=category)
        amount = 0

        for expense in expenses:
            amount += expense.amount
        
        return {'amount' : str(amount)}


class IncomeSummaryStats(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        today = date.today()
        a_year_ago = today - timedelta(days=365)

        incomes = Income.objects.filter(owner=request.user)

        final = {}
        sources = list(map(self.get_source, incomes))


        for income in incomes:
            for source in sources:
                final[source] = self.get_amount_for_source(incomes, source)
        
        return JsonResponse({'source_data' : final}, status=status.HTTP_200_OK)
    
    def get_source(self, income):
        return income.source
    
    def get_amount_for_source(self, incomes, source):
        incomes = incomes.filter(source=source)
        amount = 0

        for income in incomes:
            amount += income.amount
        
        return {'amount' : str(amount)}
