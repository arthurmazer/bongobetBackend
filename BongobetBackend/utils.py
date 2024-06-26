from wallet.utils import refund_bet_value_wallet, add_to_wallet_loss_bet, add_to_wallet_win_bet
from bet.models import StatusBet
from datetime import datetime, timedelta
from leagueoflegends.utils import get_last_matches_id, get_match_by_id

def set_bet_winner(bet, betlol):
    add_to_wallet_win_bet(bet.userEmail, betlol.quantity, betlol.quantity * betlol.odds)
    betlol.statusBet = StatusBet.VITORIA.value
    betlol.save()         

def set_bet_loser(bet, betlol):
    add_to_wallet_loss_bet(bet.userEmail, betlol.quantity)
    betlol.statusBet = StatusBet.DERROTA.value
    betlol.save()

def set_refund(bet, betlol):
    refund_bet_value_wallet(bet.userEmail, betlol.quantity)
    betlol.statusBet = StatusBet.REEMBOLSADO.value
    betlol.save()

def check_win_condition(match, betType):
    if betType == "win":
        print("Win Confirmed")
        return True
    elif betType == "baron2":
        if match[0]["teamBaronKills"] >= 2:
            print("Baron2 Confirmed")
            return True
        return False
    elif betType == "firstblood":
        if match[0]["firstBloodKill"]:
            print("Firstblood Confirmed")
            return True
        return False
    elif betType == "double3":
        if match[0]["doubleKills"] >= 3:
            print("Double3 Confirmed")
            return True
        return False
    elif betType == "clashchampion":
        return False
    elif betType == "aphelios":
        if match[0]["championId"] == 523:
            print("Aphelios Confirmed")
            return True
        return False
    elif betType == "singed":
        if match[0]["championId"] == 27:
            return True
        return False
    elif betType == "imortal":
        if match[0]["deaths"] == 0:
            print("Imortal Confirmed")
            return True
        return False
    elif betType == "ggezsr":
        if match[0]["duration"] <= 1200:
            print("GGEZSR Confirmed")
            return True
        return False
    elif betType == "ggezaram":
        if match[0]["duration"] <= 1200:
            print("GGEZARAM Confirmed")
            return True
        return False
            
def check_match_queue(match, bet_game_type):
    queueId = match['info']['queueId']
    if queueId == bet_game_type:
        return True
    else:
        return False


def check_bet_expirada(bet_date):
    # Data fornecida
    data_fornecida = datetime.strptime(str(bet_date), "%Y-%m-%d %H:%M:%S.%f%z")

    # Remover informação de fuso horário (tornar offset-naive)
    data_fornecida = data_fornecida.replace(tzinfo=None)
    data_atual = datetime.now()
    data_ha_duas_horas = data_atual - timedelta(hours=2)
    if data_fornecida < data_ha_duas_horas:
        print("A data fornecida foi há mais de duas horas atrás. BET EXPIRADA")
        return True
    else:
        print("A data fornecida não foi há mais de duas horas atrás. Bet valida")
        return False


def check_next_game(puuid, idUltimoJogo):
    last_match = get_last_matches_id(puuid, 10)
    if last_match is None:
        return None
    
    indice = last_match.index(idUltimoJogo)

    if indice > 0:
        for i in range(indice-1, -1 , -1):
            partida_bet = last_match[i]
            match = get_match_by_id(partida_bet)

            #checa remake
            if match['info']['gameDuration'] > 420:
                return match
        return None
    else:
        print("O elemento especificado é o primeiro da lista. Não há elemento anterior.")
        return None        
