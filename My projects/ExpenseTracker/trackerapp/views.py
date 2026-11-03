
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.http import require_POST
from django.db.models import Sum
from django.utils import timezone
from django.contrib import messages

from datetime import date
from decimal import Decimal, InvalidOperation

from .models import Transaction


# REGISTER
def register(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('dashboard')

    else:
        form = UserCreationForm()

    return render(
        request,
        'trackerapp/register.html',
        {'form': form}
    )


# LOGIN
def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('dashboard')

    else:
        form = AuthenticationForm()

    return render(
        request,
        'trackerapp/login.html',
        {'form': form}
    )


# LOGOUT
@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')


# DASHBOARD
@login_required
def dashboard(request):

    user_transactions = Transaction.objects.filter(
        user=request.user
    )

    # ADD TRANSACTION
    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        transaction_type = request.POST.get(
            'transaction_type', ''
        ).capitalize()
        transaction_date = request.POST.get('date')
        description = request.POST.get('description', '')

        try:
            amount = Decimal(amount)

            if (
                title
                and category
                and transaction_date
                and amount > 0
                and transaction_type in ['Income', 'Expense']
            ):

                Transaction.objects.create(
                    user=request.user,
                    title=title,
                    amount=amount,
                    category=category,
                    transaction_type=transaction_type,
                    date=transaction_date,
                    description=description
                )

                messages.success(
                    request,
                    'Transaction added successfully!'
                )

                return redirect('dashboard')

        except (InvalidOperation, TypeError, ValueError):
            messages.error(
                request,
                'Please enter valid transaction details.'
            )

    # TRANSACTIONS
    transactions = user_transactions.order_by('-date')

    # INCOME
    income = user_transactions.filter(
        transaction_type='Income'
    ).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')

    # EXPENSES
    expenses = user_transactions.filter(
        transaction_type='Expense'
    ).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')

    # BALANCE
    balance = income - expenses

    # MONTHLY REPORT
    today = timezone.localdate()

    monthly_report = []

    for i in range(5, -1, -1):

        month_number = today.month - i
        year = today.year

        while month_number <= 0:
            month_number += 12
            year -= 1

        month_date = date(year, month_number, 1)

        month_name = month_date.strftime('%b %Y')

        month_transactions = user_transactions.filter(
            date__year=year,
            date__month=month_number
        )

        month_income = float(
            month_transactions.filter(
                transaction_type='Income'
            ).aggregate(
                total=Sum('amount')
            )['total'] or 0
        )

        month_expenses = float(
            month_transactions.filter(
                transaction_type='Expense'
            ).aggregate(
                total=Sum('amount')
            )['total'] or 0
        )

        monthly_report.append({
            'month': month_name,
            'income': month_income,
            'expenses': month_expenses,
            'savings': month_income - month_expenses,
        })

    # CATEGORY REPORT
    category_queryset = user_transactions.filter(
        transaction_type='Expense',
        date__year=today.year,
        date__month=today.month
    ).values(
        'category'
    ).annotate(
        total=Sum('amount')
    ).order_by('-total')

    category_data = [
        {
            'category': item['category'],
            'total': float(item['total'])
        }
        for item in category_queryset
    ]

    context = {
        'transactions': transactions,
        'income': income,
        'expenses': expenses,
        'balance': balance,
        'monthly_report': monthly_report,
        'category_data': category_data,
        'current_month': today.strftime('%B %Y'),
    }

    return render(
        request,
        'trackerapp/dashboard.html',
        context
    )


# EDIT TRANSACTION
@login_required
def edit_transaction(request, id):

    transaction = get_object_or_404(
        Transaction,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        transaction.title = request.POST.get('title', '').strip()

        try:
            amount = Decimal(request.POST.get('amount', ''))

            if amount <= 0:
                raise InvalidOperation

            transaction.amount = amount
            transaction.category = request.POST.get('category')

            transaction.transaction_type = (
                request.POST.get(
                    'transaction_type', ''
                ).capitalize()
            )

            transaction.date = request.POST.get('date')
            transaction.description = request.POST.get(
                'description', ''
            )

            transaction.save()

            messages.success(
                request,
                'Transaction updated successfully!'
            )

            return redirect('dashboard')

        except (InvalidOperation, TypeError, ValueError):
            messages.error(
                request,
                'Please enter a valid amount.'
            )

    return render(
        request,
        'trackerapp/edit.html',
        {'transaction': transaction}
    )


# DELETE TRANSACTION
@login_required
@require_POST
def delete_transaction(request, id):

    transaction = get_object_or_404(
        Transaction,
        id=id,
        user=request.user
    )

    transaction.delete()

    messages.success(
        request,
        'Transaction deleted successfully!'
    )

    return redirect('dashboard')
