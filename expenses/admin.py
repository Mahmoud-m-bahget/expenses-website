from django.contrib import admin
from .models import Expenses , Category
# Register your models here.


class EpensesAdmin(admin.ModelAdmin):
    list_display = ('amount','description' , 'owner','category','date')
    search_fields = ('description','category','date')
admin.site.register(Expenses)
admin.site.register(Category)