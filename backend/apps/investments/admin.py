from django.contrib import admin
from .models import Investment

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'reactor', 
        'amount_invested', 
        'created_at'
    ]
    list_filter = ['created_at', 'reactor']
    search_fields = ['user__username', 'reactor__name']
    readonly_fields = ['created_at', 'updated_at']