from django.contrib import admin

# Register your models here.
from .models import CashMemo,FixBudetModel
class CashMemoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(CashMemo,CashMemoAdmin)
admin.site.register(FixBudetModel)
