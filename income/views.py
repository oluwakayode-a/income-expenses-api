from multiprocessing.spawn import import_main_path
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Income
from .permissions import IsOwner
from .serializers import IncomeSerializer
from rest_framework import permissions

# Create your views here.
class IncomeList(ListCreateAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class IncomeDetail(RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)