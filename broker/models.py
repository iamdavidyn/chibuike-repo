from django.db import models
from django.contrib.auth.models import  User
# Create your models here.




class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    initial = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    welcome = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    avaliable = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    withdrawal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pending_withdrawal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class CurrencySetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency= models.CharField(max_length=10, default='$')

    def __str__(self):
        return self.currency
    
class BankDeposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    bank_currency = models.CharField(max_length=10)
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    )
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    proof = models.ImageField(upload_to='proof/')
    is_credited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.bank_currency} - {self.status}" 




class BankTransferSetting(models.Model):
    bank_name = models.CharField(max_length=100, blank=True, null=True)    
    account_number = models.CharField(max_length=100, blank=True, null=True)
    accounts_name = models.CharField(max_length=100, blank=True, null=True)
    swift_code = models.CharField(max_length=100, blank=True, null=True)
    routing_number = models.CharField(max_length=100, blank=True, null=True)
    important_note = models.TextField( blank=True, null=True)


    def __str__(self):
        return f"{self.bank_name} - {self.account_number} - {self.accounts_name}"


class CryptoDeposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_amount = models.IntegerField()
    crypto_type = models.CharField(max_length=100)
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    )
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    proof = models.ImageField(upload_to='proof/')
    is_credited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user} - {self.crypto_amount} - {self.status}"
    
class CryptoWalletSetting(models.Model):
    crypto_type = models.CharField(max_length=100)    
    wallet_address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.crypto_type} - {self.wallet_address}"


class WithdrawalRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    withdrawal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    withdrawal_currency = models.CharField(max_length=10)
    withdrawal_method = models.CharField(max_length=20)
    destination_account = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
  


class EmailsHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    greeting = models.CharField(max_length=255)
    content =  models.TextField()
    url = models.URLField(blank=True, null=True)
    link_anchor = models.CharField(blank=True, null=True)
    sent = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)