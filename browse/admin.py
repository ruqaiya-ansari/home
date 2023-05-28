from django.contrib import admin
from .models import Review
# Register your models here.

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'body']

