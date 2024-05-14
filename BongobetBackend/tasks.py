import logging
from .celery import app
from bet.models import Bet, BetLol
from leagueoflegends.utils import map_response_match_history, check_lol_streaming_now, get_live_match, insert_player_online, get_user__summoners_rift_rank_stats, get_user_by_puuid, get_streamer_details
from leagueoflegends.models import FamousTwitchPlayersLol, PlayersOnline
from .utils import check_next_game, check_match_queue, check_bet_expirada, set_refund, set_bet_winner, set_bet_loser, check_win_condition

logger = logging.getLogger(__name__)

@app.task
def check_and_validate_bets():
    print("--------------- ################## ------------- CHECANDO BETS ------------ ################## ---------------")
    
    bets = Bet.objects.filter(betlol__statusBet=0).order_by('-date')

    #Itera sobre as bets com Status = 0 (Ainda não processadas)
    for bet in bets:
        betsLol = BetLol.objects.filter(bet=bet.id)
        print(betsLol)

        match = check_next_game(puuid=bet.puuid, idUltimoJogo=bet.idUltimoJogo)
            
        for betlol in betsLol:
            if check_bet_expirada(bet.date):
                print("EXPIRADA - REFUND")
                set_refund(bet, betlol)
            else:
                #-> verifica o jogo seguinte, se for diferente do tipo de jogo apostado, refund
                if match:
                    print("Jogo encontrado")
                    if check_match_queue(match, betlol.betType.gametype.queueId):
                        print("Queue ID Bate, foi o jogo apostado")
                        matchArray = []
                        matchArray.append(match)
                        matchResponse = map_response_match_history(bet.puuid, matchArray)
                        win = matchResponse[0]["win"]
                        if win:
                            #check bet conditions
                            if check_win_condition(matchResponse, betlol.betType.type):
                                set_bet_winner(bet, betlol)
                            else:
                                set_bet_loser(bet, betlol)
                        else:
                            set_bet_loser(bet, betlol)
                    else:
                        print("Queue ID não bate, jogou partida diferente da aposta")
                        set_refund(bet, betlol)
                else:
                    print("Jogo não encontrado - Partida ainda não ocorreu")

@app.task
def check_famous_players_online_twitch():
    print("--------------- ################## ------------- CHECANDO TWITCH ONLINE PLAYERS------------ ################## ---------------")
    lolStreamers = FamousTwitchPlayersLol.objects.all()

    for lol_streamer in lolStreamers:
        print(lol_streamer)
        channel_id = lol_streamer.channelId
        region = lol_streamer.region
        puuid = lol_streamer.puuid

        streamer_online = check_lol_streaming_now(channel_id)

        if streamer_online and streamer_online.get('data').__len__() > 0:

            streamer_profile = get_streamer_details(channel_id)

            streamer_data = streamer_online.get('data')

            if streamer_data.__len__() > 0 and streamer_data[0].get('type') == 'live' and streamer_data[0].get('game_id') == "21779":

                current_match = get_live_match(puuid)
                print(current_match)
                if current_match:
                    #rint("Streamer online e jogando Lolzinho do Povo Brasileiro")
                    lolUser = get_user_by_puuid(puuid)

                    streamer_rank = get_user__summoners_rift_rank_stats(lolUser['id'])

                    # Filtra os objetos com 'queueType' igual a 'RANKED_SOLO_5x5'
                    ranked_solo_queue_stats = list(filter(lambda item: item["queueType"] == "RANKED_SOLO_5x5", streamer_rank))

                    #Pega o Rank da SoloQ ou FlexQ
                    if ranked_solo_queue_stats.__len__() > 0:

                        insert_player_online(
                            lol_streamer.id, 
                            ranked_solo_queue_stats[0].get('rank'),
                            ranked_solo_queue_stats[0].get('tier'),
                            ranked_solo_queue_stats[0].get('leaguePoints'),
                            streamer_profile.get('data')[0].get('profile_image_url'),
                            streamer_data[0].get('started_at')
                            )
                    else:
                        ranked_flex_queue_stats = list(filter(lambda item: item["queueType"] == "RANKED_FLEX_SR", streamer_rank))
                        if ranked_flex_queue_stats.__len__() > 0:
                            insert_player_online(
                                lol_streamer.id, 
                                ranked_flex_queue_stats[0].get('rank'),
                                ranked_flex_queue_stats[0].get('tier'),
                                ranked_flex_queue_stats[0].get('leaguePoints'),
                                streamer_profile.get('data')[0].get('profile_image_url'),
                                streamer_data[0].get('started_at')
                            )
                        else:
                            #Streamer sem rank no LoL
                            insert_player_online(
                                lol_streamer.id, 
                                "Unranked",
                                "",
                                0,
                                streamer_profile.get('data')[0].get('profile_image_url'),
                                streamer_data[0].get('started_at')
                            )
                else:
                    #"Streamer online mas não jogando"
                    try:
                        player_online = PlayersOnline.objects.get(id=lol_streamer.id)
                        player_online.delete()
                        print("Registro removido com sucesso!")
                    except PlayersOnline.DoesNotExist:
                        print("O registro não foi encontrado.")
        else:
            try:
                player_online = PlayersOnline.objects.get(id=lol_streamer.id)
                player_online.delete()
                print("Registro removido com sucesso!")
            except PlayersOnline.DoesNotExist:
                print("O registro não foi encontrado.")