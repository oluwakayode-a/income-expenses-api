from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Expense
from .permissions import IsOwner
from .serializers import ExpenseSerializer
from rest_framework import permissions

# Create your views here.
class ExpenseList(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ExpenseDetail(RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)