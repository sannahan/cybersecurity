from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import connection
from .models import Account, Card, User
from django.views.decorators.csrf import csrf_exempt
from utils.exceptions import CustomError

@login_required
def index(request):
    return render(request, 'accounts/index.html', {})

# @login_required
def secret(request):
    return render(request, 'accounts/secret.html', {})

@login_required
def accounts(request):
    accounts = Account.objects.filter(owner=request.user)
    error_message = request.GET.get('error_message')

    if error_message:
        return render(request, 'accounts/accounts.html', {'accounts': accounts, 'error_message': error_message})
    
    return render(request, 'accounts/accounts.html', {'accounts': accounts})

@login_required
def transfer_money(request):
    error_message = None
    if request.method == "POST":
        source_account_iban = request.POST.get("sourceAccount")
        destination_account_iban = request.POST.get("destinationAccount")
        try:  
            amount = float(request.POST.get("amount"))
            source_account = Account.objects.get(iban=source_account_iban)

            if source_account.balance >= amount:
                with connection.cursor() as cursor:
                    source_account.balance -= amount
                    source_account.save()

                    # non-parametrized query allowing for sql injection
                    cursor.execute("UPDATE accounts_account SET balance = balance + %s WHERE iban = \"%s\"" % (amount, destination_account_iban))

                    # query that prevents sql injection
                    # cursor.execute("UPDATE accounts_account SET balance = balance + %s WHERE iban = %s", [amount, destination_account_iban])
            else:
                error_message = 'Insufficient funds for the transfer'
        except ValueError:
            error_message = 'Please enter an amount in numbers'

    if error_message:
        return redirect(reverse('accounts') + f'?error_message={error_message}')
    
    return redirect(reverse('accounts'))

@login_required
def cards(request):
    cards = Card.objects.filter(owner=request.user)
    return render(request, 'accounts/cards.html', {'cards': cards})

@login_required
@csrf_exempt # does not prevent a CSRF attack
def message(request):
    if request.method == "POST":
      message = request.POST.get("message")
      # the message is just printed here, but it could be stored to the bank's database and processed
      print(message)

    return render(request, 'accounts/message.html', {})

@login_required
def error(request):
    raise CustomError(f"Currently on user {request.user} out of all users {list(User.objects.values_list('username', flat=True))}")


