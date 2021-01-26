from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('' ,views.index,name='expenses'),
    path('add-expenses' ,views.add_expenses,name='add_expenses'),
    path('edit-expenses/<int:id>' ,views.expense_edit,name='expense-edit'),
    path('exoense-delete/<int:id>' ,views.delete_expense,name='exoense-delete'),
    path('search-expenses' ,csrf_exempt(views.search_expenses),name='search-expenses'),
    path('expense_category_summary',views.expense_category_summary,name='expense_category_summary'),
    path('stats',views.stat_view,name='stats'),
    path('export_csv',views.export_scv,name='export-scv'),
    path('export-excel',views.export_excel,name='export-excel'),
    #path('export_pdf',views.export_pdf,name='export_pdf'),

]