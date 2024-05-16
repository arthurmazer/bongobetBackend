import logging
from .celery import app
from bet.models import Bet, BetLol
from leagueoflegends.utils import map_response_match_history, check_lol_streaming_now, get_live_match, get_user__summoners_rift_rank_stats, get_user_by_puuid, get_streamer_details, get_account_user_by_puuid
from leagueoflegends.models import StreamerTwitchPlayersLol
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
    lolStreamers = StreamerTwitchPlayersLol.objects.all()

    for lol_streamer in lolStreamers:

        channel_id = lol_streamer.channelId
        region = lol_streamer.region
        puuid = lol_streamer.puuid

        #update rank status
        lolUser = get_user_by_puuid(puuid)
        lolAccount = get_account_user_by_puuid(puuid)

        if lolAccount:
            lol_streamer.gameNickName = lolAccount.get('gameName')
            lol_streamer.gameTag = lolAccount.get('tagLine')
        
        if lolUser is None:
            continue

        streamer_rank = get_user__summoners_rift_rank_stats(lolUser['id'])


        if streamer_rank is None:
            continue

        # Filtra os objetos com 'queueType' igual a 'RANKED_SOLO_5x5'
        ranked_solo_queue_stats = list(filter(lambda item: item["queueType"] == "RANKED_SOLO_5x5", streamer_rank))

        #Pega o Rank da SoloQ ou FlexQ
        if ranked_solo_queue_stats.__len__() > 0:
            lol_streamer.rank = ranked_solo_queue_stats[0].get('rank')
            lol_streamer.tier = ranked_solo_queue_stats[0].get('tier')
            lol_streamer.pdl = ranked_solo_queue_stats[0].get('leaguePoints')
            #update rank
        else:
            ranked_flex_queue_stats = list(filter(lambda item: item["queueType"] == "RANKED_FLEX_SR", streamer_rank))
            if ranked_flex_queue_stats.__len__() > 0:
                lol_streamer.rank = ranked_flex_queue_stats[0].get('rank')
                lol_streamer.tier = ranked_flex_queue_stats[0].get('tier')
                lol_streamer.pdl = ranked_flex_queue_stats[0].get('leaguePoints')
            else:
                #Streamer sem rank no LoL
                lol_streamer.rank = "Unranked"
                lol_streamer.tier = ""
                lol_streamer.pdl = 0

        #Get Streamer Details
        streamer_profile = get_streamer_details(channel_id)
        lol_streamer.thumbUrl = streamer_profile.get('data')[0].get('profile_image_url')


        #Check if streamer is online
        streamer_online = check_lol_streaming_now(channel_id)
        if streamer_online and streamer_online.get('data').__len__() > 0:

            streamer_data = streamer_online.get('data')
            
            #Ve se ele ta jogando Lolzinho
            if streamer_data.__len__() > 0 and streamer_data[0].get('type') == 'live' and streamer_data[0].get('game_id') == "21779":
                #Esta online na Twitch, pega a data de inicio da live
                lol_streamer.started_at = streamer_data[0].get('started_at')
                lol_streamer.isOnline = True

                #confere se esta jogando LOL pela API Riot
                current_match = get_live_match(puuid)
                print(current_match)
                if current_match:
                    #rint("Streamer online e jogando Lolzinho do Povo Brasileiro")
                    lol_streamer.isPlaying = True
                else:
                    #"Streamer online mas não jogando"
                    lol_streamer.isPlaying = False
        else:
            #Streamer Offline
            lol_streamer.isOnline = False
            lol_streamer.isPlaying = False

        #Por fim, salva as atualizações

        lol_streamer.save()