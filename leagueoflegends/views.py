
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .utils import get_user_by_puuid
from .utils import get_live_match
from .utils import get_user_by_summoner_name_tagline
from .utils import obter_primeira_versao_ddragon
from .utils import get_user__summoners_rift_rank_stats
from .utils import get_user_tft_rank_stats
from .utils import map_response_match_history
from .utils import map_response_live_match
from .utils import get_match_history_api
from .utils import RIOT_API_BR_REGION
from bet.models import GameType, BetType, Bet, BetLol
import os


class RiotAccoutAPIView(APIView):
    def get(self,request):
        try:
            summoner_name = request.query_params.get('summoner_name')
            tag = request.query_params.get('tag')
            lolAccount = get_user_by_summoner_name_tagline(summoner_name, tag)
            print(lolAccount)
            if lolAccount:
                return Response(lolAccount, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': 'User not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class LolSummonerDataAPIView(APIView):
    def get(self, request):
        try:
            puuid = request.query_params.get('puuid')

            lolUser = get_user_by_puuid(puuid)

            userSummonersRiftRank = get_user__summoners_rift_rank_stats(lolUser['id'])
            userTftRank = get_user_tft_rank_stats(lolUser['id'])

            if lolUser:
                responseData = []
                rankSummonersResponseData = []
                lolLastVersion = obter_primeira_versao_ddragon()
                urlProfileImg = 'https://ddragon.leagueoflegends.com/cdn/' + str(lolLastVersion) + '/img/profileicon/' + str(lolUser['profileIconId']) + '.png'

                print(":d")
                print(userSummonersRiftRank)
                for result in userSummonersRiftRank:
                    if 'queueType' in result and result['queueType'] == 'RANKED_SOLO_5x5':
                        print("entro1")
                        rankSummonersResponseData.append({
                            'queueType': 'Ranked Solo/Duo',
                            'tier': str(result.get('tier')),
                            'rank': str(result.get('rank')),
                            'pdl': str(result.get('leaguePoints')),
                            'wins': result.get('wins'),
                            'losses':result.get('losses'),
                            'iconRankSolo': str(result.get('tier')).lower() + '.png',
                        })
                    elif 'queueType' in result and result['queueType'] == 'RANKED_FLEX_SR':
                        print("entro3")
                        rankSummonersResponseData.append({
                            'queueType': 'Ranked Flex',
                            'tier': str(result.get('tier')),
                            'rank': str(result.get('rank')),
                            'pdl': str(result.get('leaguePoints')),
                            'wins': result.get('wins'),
                            'losses':result.get('losses'),
                            'iconRankSolo': str(result.get('tier')).lower() + '.png',
                        })

                contains_ranked_solo_duo = any(item.get('queueType') == 'Ranked Solo/Duo' for item in rankSummonersResponseData)
                contains_ranked_flex = any(item.get('queueType') == 'Ranked Flex' for item in rankSummonersResponseData)

                if contains_ranked_solo_duo == False:
                    rankSummonersResponseData.append({
                        'queueType': 'Ranked Solo/Duo',
                        'tier': 'UNRANKED',
                        'rank': "",
                        'pdl': "0",
                        'wins': 1,
                        'losses': 1,
                        'iconRankSolo': 'unranked.png',
                    })
                if contains_ranked_flex == False:
                    rankSummonersResponseData.append({
                        'queueType': 'Ranked Flex',
                        'tier': 'UNRANKED',
                        'rank': "",
                        'pdl': "0",
                        'wins': 1,
                        'losses': 1,
                        'iconRankSolo': 'unranked.png',
                    })

                
                if userTftRank:
                    rankSummonersResponseData.append({
                        'queueType': 'Ranked TFT',
                        'tier': str(userTftRank[0].get('tier')),
                        'rank': str(userTftRank[0].get('rank')),
                        'pdl': str(userTftRank[0].get('leaguePoints')),
                        'wins': userTftRank[0].get('wins'),
                        'losses':userTftRank[0].get('losses'),
                        'iconRankSolo': str(userTftRank[0].get('tier')).lower() + '.png',
                    })
                else:
                    rankSummonersResponseData.append({
                        'queueType': 'Ranked TFT',
                        'tier': 'UNRANKED',
                        'rank': "",
                        'pdl': "0",
                        'wins': 1,
                        'losses': 1,
                        'iconRankSolo': 'unranked.png',
                    })
                responseData = {
                    'id': lolUser['id'],
                    'puuid': lolUser['puuid'],
                    'accountId': lolUser['accountId'],
                    'urlProfile': urlProfileImg,
                    'summonerLevel': lolUser['summonerLevel'],
                    'ranks': rankSummonersResponseData
                }

                print(responseData)
                return Response(responseData, status=status.HTTP_200_OK)
            else:
                if lolUser is None:
                    print("Usuário não encontrado na API RIOT")
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
                else: 
                    if userSummonersRiftRank is None:
                        return Response({'error': 'Rank not found'}, status=status.HTTP_406_NOT_ACCEPTABLE) 
                    else:
                        return Response({'error': 'Unknown error'}, status=status.HTTP_404_NOT_FOUND)
        except: 
            return Response({'error': 'User not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class LolMatchHistoryAPIView(APIView):
     def get(self, request):
        try:
            puuid = request.query_params.get('puuid')
    
            if puuid:
                quantMatches = request.query_params.get('quant_matches')
                if (quantMatches):
                    quantMatches = int(quantMatches)
                else:
                    quantMatches = 6               

                print("entro")
                match_history = get_match_history_api(puuid, quantMatches)
                print(match_history)
                print("toma")
                matchHistoryResponse = map_response_match_history(puuid, match_history)
                print("zedume?")


                live_match = get_live_match(puuid)
                if live_match:
                    last_match = map_response_live_match(puuid,live_match)
                
    
                if matchHistoryResponse:
                    if live_match:
                        return  Response({'summoners_rift': matchHistoryResponse, 'live_match': last_match}, status=status.HTTP_200_OK)
                    return  Response({'summoners_rift': matchHistoryResponse}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Match3 not found'}, status=status.HTTP_404_NOT_FOUND)

            else:
                return Response({'error': 'Match1 not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'error': 'User not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class LiveMatchApiView(APIView):
    def get(self, request):

        puuid = request.query_params.get('puuid')
        print(puuid)
        if puuid:
            live_match = get_live_match(puuid)
            if live_match:
                return Response(map_response_live_match(puuid, live_match), status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Live match not found'}, status=status.HTTP_404_NOT_FOUND)



