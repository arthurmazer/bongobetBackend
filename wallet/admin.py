from django.contrib import admin

from wallet.models import Wallet, WalletHistory
# Register your models here.

admin.site.register(Wallet)
admin.site.register(WalletHistory)