from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('' ,views.index,name='income'),
    path('add-income' ,views.add_income,name='add_income'),
    path('edit-income/<int:id>' ,views.income_edit,name='income-edit'),
    path('incmoe-delete/<int:id>' ,views.delete_income,name='income-delete'),
    path('search-income' ,csrf_exempt(views.search_income),name='search-income'),
    path('income_source_summary',views.income_source_summary,name='income_source_summary'),
    path('stats-income',views.stat_view,name='stats-income'),
    path('export_csv_income',views.export_scv,name='export_csv_income'),
    path('export_excel_income',views.export_excel_income,name='export_excel_income'),


]