from django.forms import ModelForm
from .models import CashMemo,FixBudetModel

class CashMemoForm(ModelForm):
    class Meta:
        model = CashMemo
        fields = ['title','memo','cost','taken','given']

class FixBudetForm(ModelForm):
    class Meta:
        model = FixBudetModel
        fields = ['budget']
