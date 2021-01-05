from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expenses 
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreferences
import datetime
# Create your views here.


@login_required(login_url='/authentication/login')
def search_expenses(request):
    if request.method =='POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expenses.objects.filter(
            amount__istartswith = search_str,owner=request.user) |Expenses.objects.filter(
            date__istartswith = search_str,owner=request.user) |Expenses.objects.filter(
            description__icontains = search_str,owner=request.user) |Expenses.objects.filter(
            category__icontains = search_str,owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data),safe=False)




@login_required(login_url='/authentication/login')
def index(request):
    categpries = Category.objects.all()
    expenses=Expenses.objects.filter(owner=request.user)
    paginator = Paginator(expenses,5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    exists = UserPreferences.objects.filter(user=request.user).exists()
    if exists:
        currency = UserPreferences.objects.get(user=request.user).currency

    else:
        currency = 'USD - United States Dollar'
    context = {
        "expenses":expenses,
        'page_obj':page_obj,
        'currency':currency
    }
    return render(request,'expenses/index.html',context)

@login_required(login_url='/authentication/login')
def add_expenses(request):
    categpries = Category.objects.all()

    context = {
        'categpries':categpries,
        'values':request.POST,
    }

    if request.method == 'GET':

        return render(request,'expenses/add_expenses.html',context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expens_date']
        category = request.POST['category']

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'expenses/add_expenses.html',context)

        if not category:
            messages.error(request,'Category is required')
            return render(request,'expenses/add_expenses.html',context)

    

        if not description:
            messages.error(request,'Description is required')
            return render(request,'expenses/add_expenses.html',context)
            
        if not date:
            messages.error(request,'Date is required')
            return render(request,'expenses/add_expenses.html',context)
        
        Expenses.objects.create(amount=amount,date=date,description=description,category=category,owner=request.user)
        messages.success(request,'Expenses saved successfully')
        return redirect('expenses')

@login_required(login_url='/authentication/login')
def expense_edit(request,id):
    expense = Expenses.objects.get(pk=id)
    categpries = Category.objects.all()

    context = {
        'expense':expense,
        'values':expense,
        'categpries':categpries
    }
    if request.method=='GET':
        return render (request,'expenses/edit-expense.html',context)

    if request.method=='POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expens_date']
        category = request.POST['category']

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'expenses/edit-expense.html',context)

        if not description:
            messages.error(request,'Description is required')
            return render(request,'expenses/edit-expense.html',context)
            
        if not date:
            messages.error(request,'Date is required')
            return render(request,'expenses/edit-expense.html',context)
        
        
        expense.owner=request.user
        expense.amount=amount
        expense.date=date
        expense.category=category
        expense.description=description
        expense.save()


        messages.success(request,'Expenses Updated successfully')
        return redirect('/')

@login_required(login_url='/authentication/login')
def delete_expense(request,id):
    expense = Expenses.objects.get(pk=id)
    expense.delete()
    messages.success(request,'Expense removed')
    return redirect('/')


def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_month_ago= todays_date-datetime.timedelta(days=30*6)
    expenses = Expenses.objects.filter(date__gte= six_month_ago,date_lte=todays_date)
