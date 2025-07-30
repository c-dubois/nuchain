from django.contrib import admin
from .models import Reactor

@admin.register(Reactor)
class ReactorAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'type',
        'location', 
        'price_per_token', 
        'annual_roi_rate', 
        'investment_percentage', 
        'is_active'
    ]
    list_filter = ['is_active', 'location', 'slug']
    search_fields = ['name', 'location', 'description']
    readonly_fields = ['created_at', 'updated_at', 'current_investments', 'investment_percentage']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'location', 'image_url', 'is_active')
        }),
        ('Investment Parameters', {
            'fields': ('price_per_token', 'annual_roi_rate', 'carbon_offset_tonnes_co2_per_nuc_per_year')
        }),
        ('Capacity', {
            'fields': ('total_capacity', 'current_investments')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def investment_percentage(self, obj):
        return f"{obj.investment_percentage:.1f}%"
    investment_percentage.short_description = "Investment %"