from django.contrib import admin
from .models import BankDeposit, CryptoWalletSetting , CurrencySetting, Profile, BankTransferSetting, CryptoDeposit, WithdrawalRequest, EmailsHistory
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):

    list_display = ('user', 'initial', 'welcome', 'avaliable', 'profit', 'withdrawal', 'pending_withdrawal')

class CustomUserAdmin(UserAdmin):

    list_display = ('username', 'email', 'is_active')

class BankDepositAdmin(admin.ModelAdmin):

    list_display = ('user', 'amount', 'bank_currency', 'status')

class CurrencySettingAdmin(admin.ModelAdmin):

    list_display = ('user', 'currency')

class WithdrawalRequestAdmin(admin.ModelAdmin):

    list_display = ('user', 'withdrawal_amount', 'withdrawal_currency', 'withdrawal_method', 'destination_account', 'bank_name', 'account_name')

class CryptoDepositAdmin(admin.ModelAdmin):

    list_display = ('user', 'crypto_amount', 'crypto_type', 'status')


admin.site.site_header = "My Broker Admin Pannel"
admin.site.site_title = "BrokePro Admin Portal"


admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(CurrencySetting, CurrencySettingAdmin)
admin.site.register(BankTransferSetting)
admin.site.register(CryptoDeposit)
admin.site.register(BankDeposit, BankDepositAdmin)
admin.site.register(CryptoWalletSetting)
admin.site.register(WithdrawalRequest, WithdrawalRequestAdmin)
admin.site.register(EmailsHistory)