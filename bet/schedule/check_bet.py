# agendamento_script.py
# No início do seu script
import os
import sys
from bet.models import StatusBet
projeto_caminho = f'D:\Projects\BongobetBackend'
sys.path.append(os.path.abspath(projeto_caminho))


# Configure o ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BongobetBackend.settings')

# Importe e configure o Django
import django
django.setup()
import requests
import time
import schedule
from bet.models import Bet 

def check_bet_status():
    bets = Bet.objects.all()

    for bet in bets:
        # Realize ações com base no statusBet
        if bet.statusBet == StatusBet.APOSTADO.value:
            print("Status APOSTADO - Faça algo")
            print(bet.idUltimoJogo)
            print(bet.date)
            last_match = get_summoner_last_match(bet.lolUser)
            print(last_match)
            print(last_match)
            print(last_match['matchId'])
            #print(last_match[0])
            #print(last_match.matchId)
            valor_match_id = last_match.get('matchId', [])[0]
            print(valor_match_id)
            betlols_relacionadas = bet.betlol_set.all()


            '''if (bet.idUltimoJogo == last_match[0]):
                print("Usuário ainda não jogou a partida que apostou")
                pass
            else:
                print("USUÁRIO JOGOU A PARTIDA QUE APOSTOU")
                # CHECAR VITORIA OU DERROTA
                bet.statusBet = 2
                bet.save()'''

            # Agora você pode iterar sobre as BetLol relacionadas
            for betlol in betlols_relacionadas:
                print(betlol)
                last_match_details = get_summoner_last_match_details(bet.lolUser, 1)
                print(last_match_details)
                print(betlol.betType)
                print(betlol.quantity)

                
            pass
        elif bet.statusBet == StatusBet.VITORIA.value:
            print("Status VITORIA")
            # Status VITORIA
            pass
        elif bet.statusBet == StatusBet.DERROTA.value:
            print("Status DERROTA")
            # Status DERROTA
            pass


def get_summoner_last_match(loluser):
    # Substitua 'http://localhost:8000' pelo endereço do seu servidor Django em produção
    url = f'http://localhost:8000/api/get_last_match/?puuid={loluser}' # Substitua 'seu-endpoint' pelo caminho do seu endpoint


    # Realize a chamada HTTP usando a biblioteca requests
    response = requests.get(url)

    # Verifique a resposta
    if response.status_code == 200:
        print('Chamada bem-sucedida!')
        print('DESGRACA')
        print(response.json())  # Se a resposta é JSON
        return response.json()

def get_summoner_last_match_details(summoner_name, quant_matches):
    # Substitua 'http://localhost:8000' pelo endereço do seu servidor Django em produção
    url = f'http://localhost:8000/api/get_match_history/?summonerName={summoner_name}&quantMatches={quant_matches}' # Substitua 'seu-endpoint' pelo caminho do seu endpoint


    # Realize a chamada HTTP usando a biblioteca requests
    response = requests.get(url)

    # Verifique a resposta
    if response.status_code == 200:
        print('Chamada bem-sucedida!')
        print(response.json())  # Se a resposta é JSON
    else:
        print(f'Falha na chamada. Status Code: {response.status_code}')
        print(response.text)  # Se a resposta contém texto

def job():
    print("Verificando status das apostas...")
    check_bet_status()

# Agende a tarefa para ser executada a todo minuto
schedule.every().minutes.at(":00").do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
