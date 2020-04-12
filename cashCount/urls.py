from django.urls import path

from . import views
app_name = 'cashCount'

urlpatterns = [
    path('home/', views.cashMemo,name = 'cashMemo'),
    path('create/',views.createCashMemo,name="createCashMemo"),
    path('completed/',views.completedCashMemo,name="completedCashMemo"),
    path('FixBudget/',views.FixBudget,name="FixBudget"),
    path('show/<int:cash_pk>',views.showCashMemo,name="showCashMemo"),
    path('delete/<int:cash_pk>',views.deleteCashMemo,name="deleteCashMemo"),
    #path('update/<int:cash_pk>',views.updateBudget,name="updateBudget"),


]
