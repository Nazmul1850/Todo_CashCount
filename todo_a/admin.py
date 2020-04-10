from django.contrib import admin
from .models import TODO

class TODOAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
admin.site.register(TODO,TODOAdmin)
