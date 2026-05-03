from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import BankDeposit, Profile, CurrencySetting, CryptoDeposit, CryptoWalletSetting, BankTransferSetting, WithdrawalRequest, EmailsHistory
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.admin.views.decorators import staff_member_required




def home(request):

    home_data = {}

# creating random numbers for active trader

    amount = random.randint(70000, 99999)

    formated = f'{amount/1000:.1f}K'

    home_data['active'] = formated

#creating a random number for average feed latency

    latency = random.randint(5, 14)

    home_data['afl'] = latency

    return render(request, 'home/home.html', home_data)

# User Registration and Authentication Views

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password != confirm:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
        
        elif User.objects.filter(username=username).exists():
              messages.error(request, 'Username already exists')
              return redirect('signup')
                
        elif User.objects.filter(email=email).exists():
              messages.error(request, 'Account already exists')
              return redirect('login')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long')
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
        

        login(request, user)
        return redirect('dashboard')
    return render(request, 'regislogs/signup.html')

# User Login Views

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(email=email).first()

        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')

        messages.error(request, 'Invalid email or password')

    return render(request, 'regislogs/login.html')


# User Logout View

def logout_view(request):
    logout(request)
    return redirect('home')

# Dashboard View

@login_required
def dashboard(request):
    wallet, created = Profile.objects.get_or_create(user=request.user)
    if isinstance(created, Profile):
        created = False
    elif wallet:
        created = True
    else:
        created = False



    currencys, symbol = CurrencySetting.objects.get_or_create(user=request.user)
    
    if currencys:
        symbol = False
    else:
        symbol = True
    


    return render(request, 'dashboard/dashboard.html', {'data' : wallet,
                                                        'currency' : currencys})
@login_required
def deposit (request):
    if request.method == 'POST':

        if 'deposit_crypto' in request.POST:
            crypto_amount = request.POST.get('crypto_amount')
            crypto_type = request.POST.get('crypto_type')
            proof = request.FILES.get('proof')

            CryptoDeposit.objects.create(
                user=request.user,
                crypto_amount=crypto_amount,
                crypto_type=crypto_type,
                proof=proof
            )
            messages.info(request, 'Your crypto deposit has been submitted, you will be notified once it is confirmed.')
            return redirect('deposit')


        elif 'send_funds' in request.POST:
            amount = request.POST.get('amount')
            bank_currency = request.POST.get('bank_currency')
            proof = request.FILES.get('proof')

            BankDeposit.objects.create(
                user=request.user,
                amount=amount,
                bank_currency=bank_currency,
                proof=proof
            )
            messages.success(request, 'Your bank deposit has been submitted, you will be notified once it is confirmed.')
            return redirect('deposit')


    
    address = CryptoWalletSetting.objects.all()
    bank = BankTransferSetting.objects.all()

    return render(request, 'deposit/deposit.html', {'address' : address, 'bank' : bank})


@login_required
def withdraw(request):
    
    currency,_ = CurrencySetting.objects.get_or_create(user=request.user)
    data,_ = Profile.objects.get_or_create(user=request.user)
    
    
    if data.avaliable >= Decimal("1000"):
        data.formatted = f"{data.avaliable / Decimal('1000'):.1f}K"
    else:
        data.formatted = f"{data.avaliable}"
        


    if request.method == 'POST':
        withdrawal_amount = request.POST.get('withdrawal_amount')
        withdrawal_currency = request.POST.get('withdrawal_currency')
        withdrawal_method = request.POST.get('withdrawal_method')
        account_name = request.POST.get('account_name')
        bank_name = request.POST.get('bank_name')
        destination_account = request.POST.get('destination_account')

        WithdrawalRequest.objects.create(
            user=request.user,
            withdrawal_amount=withdrawal_amount,
            withdrawal_currency=withdrawal_currency,
            withdrawal_method=withdrawal_method,
            account_name=account_name,
            bank_name=bank_name,
            destination_account=destination_account
        )

        withdrawal_amount = Decimal(withdrawal_amount)

        if withdrawal_amount > data.withdrawal:
            messages.error(request, 'Insufficient funds for withdrawal')
            return redirect('withdraw')

            
        
    
        messages.error(request, "We couldn't process your withdrawal at this time. Please contact support for assistance")
        return redirect('withdraw')

    return render(request, 'withdrawal/withdrawal.html', { 'currency': currency, 'data' : data})


@login_required
def menu(request):
    return render(request, 'menu/menu.html')


@login_required
def support(request):
    return render(request, 'support/support.html')



def about(request):
    return render(request, 'about/about.html')


def password(request):
    return render(request, "regislogs/password_recovery.html")



class CustomPasswordResetView(auth_views.PasswordResetView):
    email_template_name = "regislogs/recovery_email.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["custom_message"] = "This link will expire in 24 hours."
        return context



@staff_member_required
def emails(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        subject = request.POST.get('subject')
        greeting = request.POST.get('greeting')
        content = request.POST.get('content')
        url = request.POST.get('url')
        link_anchor = request.POST.get('link_anchor')

        create = EmailsHistory.objects.create(
            user_id=user_id,
            subject=subject,
            greeting=greeting,
            content=content,
            url=url,
            link_anchor=link_anchor
        )

        user = User.objects.get(id=user_id)

          # HTML version
        html_content = render_to_string('emails/base_email.html', {
        'username': user.username,
        'content': content,
        'greeting' : greeting,
        'url' : url,
        'link_anchor' : link_anchor
        })

        email = EmailMultiAlternatives(
            subject,
            content,
            settings.EMAIL_HOST_USER,
            [user.email]
        )

        email.attach_alternative(html_content, "text/html")
    
        email.send()

        messages.success(request, "email has been successfully sent")
        return redirect("emails")

    users = User.objects.all()

    return render(request, "emails/admins.html", {'users' : users})





@receiver(post_save, sender=BankDeposit,)
def transactions( sender, instance, created, **kwargs):
    if not created:
        if instance.status == 'confirmed' and not instance.is_credited:
            data, _ = Profile.objects.get_or_create(user=instance.user)
            if sender == BankDeposit:
                data.initial += instance.amount 
                data.avaliable += instance.amount
            data.save()