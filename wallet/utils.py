from .models import Wallet
from .models import WalletHistory

def create_new_wallet(userEmail):
    try:
        wallet = Wallet()
        wallet.user = userEmail
        wallet.quantityBetLocked = 0.0
        wallet.quantity = 0.0
        wallet.save()
        return wallet
    except Exception as e:
        print(str(e))
        return None

def check_funds(userEmail, value):
    wallet = Wallet.objects.filter(user=userEmail).first()
    print(wallet)
    if wallet:
        if wallet.quantity >= value:
            print("Tem fundos suficientes para a aposta")
            return True
        else:
            print("Não tem fundos suficientes para a aposta")
            return False
    else:
        return False

def bet_value_wallet(userEmail, value):
    wallet = Wallet.objects.filter(user=userEmail).first()
    if wallet:
        wallet.quantity -= value
        wallet.quantityBetLocked += value
        wallet.save()
        add_to_wallet_history(userEmail, value, "Aposta Feita - League of Legends")
        return wallet
    else:
        return None
    
def add_to_wallet_history(userEmail, value, description):
    wallet_history = WalletHistory()
    wallet_history.user = userEmail
    wallet_history.quantity = value
    wallet_history.description = description
    wallet_history.save()
    return wallet_history

def refund_bet_value_wallet(userEmail, value):
    wallet = Wallet.objects.filter(user=userEmail).first()
    if wallet:
        wallet.quantity += value
        wallet.quantityBetLocked -= value
        wallet.save()
        add_to_wallet_history(userEmail, value, "Valor Devolvido - League of Legends")
        return wallet
    else:
        return None
    
def add_to_wallet_win_bet(userEmail, bet_value, gain_value):
    wallet = Wallet.objects.filter(user=userEmail).first()
    if wallet:
        wallet.quantity += gain_value
        wallet.quantityBetLocked -= bet_value
        wallet.save()
        add_to_wallet_history(userEmail, gain_value, "Aposta Ganha - League of Legends")
        return wallet
    else:
        return None
    
def add_to_wallet_loss_bet(userEmail, bet_value):
    wallet = Wallet.objects.filter(user=userEmail).first()
    if wallet:
        wallet.quantityBetLocked -= bet_value
        wallet.save()
        add_to_wallet_history(userEmail, bet_value, "Aposta Perdida - League of Legends")
        return wallet
    else:
        return None
    
