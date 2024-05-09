from django.shortcuts import render

# Create your views here.
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import GameType, BetType
from leagueoflegends.utils import get_user_tft_rank_stats, get_user__summoners_rift_rank_stats, get_user_by_puuid
from leagueoflegends.utils import get_live_match, map_response_live_match, map_response_match_history, get_match_history_api
from datetime import datetime
from .models import Bet, BetLol
from leagueoflegends.utils import RIOT_API_BR_REGION
from wallet.utils import bet_value_wallet, check_funds, refund_bet_value_wallet



class GamesBetTypeAPIView(APIView):	
    def get(self, request):
        try:
            gameType = GameType.objects.all()
            response = []
            for game in gameType:
                response.append({
                    'id': game.id,
                    'name': game.name,
                    'game': game.game.name
                })
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Game not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class BetTypeAPIView(APIView):	
    def get(self, request):
        try:
            gametype_id = request.query_params.get('id')
            puuid = request.query_params.get('puuid')

            if gametype_id:
                bet_type = BetType.objects.filter(gametype_id=gametype_id)
            else:
                bet_type = BetType.objects.all()


            gameType = GameType.objects.get(id=gametype_id)

            lolUser = get_user_by_puuid(puuid)
            
            if gameType.id == 4:
                userTftRank = get_user_tft_rank_stats(lolUser['id'])
                rank =  [rank for rank in userTftRank if rank['queueType'] == gameType.tag]
            else:
                userSummonersRiftRank = get_user__summoners_rift_rank_stats(lolUser['id'])
                rank =  [rank for rank in userSummonersRiftRank if rank['queueType'] == gameType.tag]


            if len( rank) == 0:
                #user sem rank
                tier = 'UNRANKED'
                wins = 10
                losses = 0
            else:
                tier = rank[0]['tier']
                wins = rank[0]['wins']
                losses = rank[0]['losses']  

            response = []
            for betType in bet_type:
                odds = calculate_odds(tier,wins, losses, betType.multiplicadorMin, betType.multiplicadorMax)
                print(odds)
                response.append({
                    'id': betType.id,
                    'name': betType.name,
                    'condicao': betType.condicao,
                    'urlThumb': betType.urlThumb,
                    'color': betType.color,
                    'gametype': betType.gametype.name,
                    'subDetails': betType.subDetails,
                    'odds': "{:.2f}".format(round(odds, 2))
                })
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Bets not found, try again later!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class BetApiView(APIView):
    def post(self, request):
        try:
            dados_post = request.data
            id_bet_type_list = dados_post.get('idBets')
            quantity_list = dados_post.get('idQuantities')
            puuid = dados_post.get('puuid')
            id_user = dados_post.get('userEmail')

            lista_ids = id_bet_type_list.split(';')
            lista_quantidades = quantity_list.split(';')


            totalGasto = sum(list(map(float, lista_quantidades)))
            print(totalGasto)
            if check_funds(id_user, totalGasto) == False:
                print('Insufficient funds')
                print(id_user)
                return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

            if (lista_ids.__len__() != lista_quantidades.__len__()):
                return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

            #check live match
            live_match = get_live_match(puuid)
            if live_match:
                queueId = live_match.get('gameQueueConfigId')
                if queueId != 0:
                    last_match = map_response_live_match(puuid, live_match)
                    gameId = str(RIOT_API_BR_REGION) + "_" + str(live_match.get('gameId'))
                else:
                    match_history = get_match_history_api(puuid, 1)
                    last_match = map_response_match_history(puuid, match_history)
                    gameId = last_match[0]["gameId"]
            else:
                match_history = get_match_history_api(puuid, 1)
                last_match =  map_response_match_history(puuid, match_history)
                gameId = last_match[0]["gameId"]

            isCashUsado = False
            bet = create_new_bet(id_user, puuid, gameId)
            wallet = bet_value_wallet(id_user, totalGasto)
            if (wallet != None):
                isCashUsado = True

            for lista_id, lista_quantidade in zip(lista_ids, lista_quantidades):
                id_bet_type = int(lista_id)
                bet_type = BetType.objects.filter(id=id_bet_type).first()
                lolUser = get_user_by_puuid(puuid)
            
                if bet_type.gametype.id == 4:
                    userTftRank = get_user_tft_rank_stats(lolUser['id'])
                    rank =  [rank for rank in userTftRank if rank['queueType'] == bet_type.gametype.tag]
                else:
                    userSummonersRiftRank = get_user__summoners_rift_rank_stats(lolUser['id'])
                    rank =  [rank for rank in userSummonersRiftRank if rank['queueType'] == bet_type.gametype.tag]


                if len( rank) == 0:
                    #user sem rank
                    tier = 'UNRANKED'
                    wins = 10
                    losses = 0
                else:
                    tier = rank[0]['tier']
                    wins = rank[0]['wins']
                    losses = rank[0]['losses']  

                odds = calculate_odds(tier,wins, losses, bet_type.multiplicadorMin, bet_type.multiplicadorMax)

                quantity = float(lista_quantidade)
                save_bet_lol(bet, id_bet_type, quantity, odds)


            responseData = {
                'code': status.HTTP_200_OK,
                'userEmail': id_user,
                'lastMatchId': gameId,
                'totalValue': totalGasto
            }

            return Response(responseData, status=status.HTTP_200_OK) 
        except Exception as e:
            print(e)
            if isCashUsado:
                refund_bet_value_wallet(id_user, totalGasto)
            return Response({'error': 'Bet not created'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class BetHistoryApiView(APIView):
    def get(self, request):
        try:
            user_email = request.query_params.get('user_email')
            
            bets = Bet.objects.filter(userEmail=user_email).order_by('-date')
            
            print(user_email)
            print(bets)
            response = []
            for bet in bets:
                betLol = BetLol.objects.filter(bet=bet)
                betList = []
                for betlol in betLol:
                    betList.append({
                        'id': betlol.betType.id,
                        'betType': betlol.betType.name,
                        'condicao': betlol.betType.condicao,
                        'color': betlol.betType.color,
                        'gametype': betlol.betType.gametype.name,
                        'quantity': betlol.quantity,
                        'subDetails': betlol.betType.subDetails,
                        'odds': betlol.odds,
                        'statusBet': betlol.statusBet,
                    })
                response.append({
                    'date': bet.date,
                    'idUltimoJogo': bet.idUltimoJogo,
                    'puuid': bet.puuid,
                    'bets': betList
                })
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': 'Bet not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def create_new_bet(user, lolUser, idUltimoJogo):
    bet = Bet()
    bet.userEmail = user
    bet.date = datetime.now()
    bet.idUltimoJogo = idUltimoJogo
    bet.puuid = lolUser
    bet.save()
    return bet

def save_bet_lol(bet, betType, quantity, odds):
    bet_type = BetType.objects.get(id=betType)
    
    betLol = BetLol()
    betLol.bet = bet
    betLol.statusBet = 0
    betLol.betType = bet_type
    betLol.quantity = quantity
    betLol.odds = odds
    betLol.save()
    return betLol
    
def calculate_odds (tier, wins, losses, multiplicadorMin, multiplicadorMax):
    print(tier)
    if tier == 'UNRANKED':
        return multiplicadorMin
    elif tier == 'IRON':
        return calc_odds_by_winrate(wins, losses, multiplicadorMin, multiplicadorMax, 0.5)
    elif tier == 'BRONZE':
        return calc_odds_by_winrate(wins, losses, multiplicadorMin, multiplicadorMax, 0.5)
    elif tier == 'SILVER':
        return calc_odds_by_winrate(wins, losses, multiplicadorMin, multiplicadorMax, 0.4)
    elif tier == 'GOLD':
        return calc_odds_by_winrate(wins, losses, multiplicadorMin, multiplicadorMax, 0.3)
    elif tier == 'PLATINUM':
        return calc_odds_by_winrate(wins, losses, multiplicadorMin, multiplicadorMax, 0.3)
    elif tier == 'EMERALD':
        return calc_odds_by_winrate(wins, losses, multiplicadorMin, multiplicadorMax, 0.2)
    elif tier == 'DIAMOND':
        return calc_odds_by_winrate(wins, losses, multiplicadorMin, multiplicadorMax, 0.1)
    elif tier == 'MASTER':
        return calc_odds_by_winrate(wins, losses, multiplicadorMin, multiplicadorMax, 0.0)
    elif tier == 'GRANDMASTER':
        return calc_odds_by_winrate(wins, losses, multiplicadorMin, multiplicadorMax, 0.0)
    elif tier == 'CHALLENGER':
        return calc_odds_by_winrate(wins, losses, multiplicadorMin, multiplicadorMax, 0.0)
            


def calc_odds_by_winrate(wins, losses,multiplicadorMin, multiplicadorMax, tierPenalty):
    total_games = wins + losses
    winrate = wins / total_games
    odds = (multiplicadorMax - (winrate * ((multiplicadorMax-multiplicadorMin)/100))-tierPenalty)
    if (odds < multiplicadorMin):
        return multiplicadorMin
    return odds