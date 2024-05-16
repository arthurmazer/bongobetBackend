import requests
from django.conf import settings
from datetime import datetime

RIOT_API_KEY = settings.RIOT_API_KEY
TWITCH_CLIENT_ID = settings.TWITCH_CLIENT_ID_KEY
TWITCH_SECRET = settings.TWITCH_SECRET_KEY
RIOT_API_AMERICAS_URL = 'https://americas.api.riotgames.com/'
RIOT_API_BR_URL = 'https://br1.api.riotgames.com/lol'
RIOT_API_BR_TFT_URL = 'https://br1.api.riotgames.com/tft'
headers = {'X-Riot-Token': RIOT_API_KEY}
RIOT_API_BR_REGION = 'BR1'

TWITCH_API_BASE_URL = 'https://api.twitch.tv/helix'

DEFAULT_MAX_PARTIDAS_HISTORICO = 5

####### RIOT API ##########lol

def get_user_by_summoner_name_tagline(summoner_name, tag):
    endpoint = f'{RIOT_API_AMERICAS_URL}riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag}'
    headers = {'X-Riot-Token': RIOT_API_KEY}
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        userLolAccount = response.json()
        return userLolAccount
    
    return None

def get_account_user_by_puuid(puuid):
    endpoint = f'{RIOT_API_AMERICAS_URL}riot/account/v1/accounts/by-puuid/{puuid}'
    headers = {'X-Riot-Token': RIOT_API_KEY}
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        userLolAccount = response.json()
        return userLolAccount
    
    return None

def get_user_by_puuid(puuid):
    endpoint = f'{RIOT_API_BR_URL}/summoner/v4/summoners/by-puuid/{puuid}'
    headers = {'X-Riot-Token': RIOT_API_KEY}
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        userProfile = response.json()
        return userProfile
    
    return None


#TO DO: Passar TFT para um módulo Novo
def get_user_tft_rank_stats(account_id):
    endpoint = f'{RIOT_API_BR_TFT_URL}/league/v1/entries/by-summoner/{account_id}'
    headers = {'X-Riot-Token': RIOT_API_KEY}
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        userStatsData = response.json()
        return userStatsData
    
    return None

def get_user__summoners_rift_rank_stats(account_id):
    endpoint = f'{RIOT_API_BR_URL}/league/v4/entries/by-summoner/{account_id}'
    print(endpoint)
    headers = {'X-Riot-Token': RIOT_API_KEY}
    response = requests.get(endpoint, headers=headers)
    print(response)

    if response.status_code == 200:
        userStatsData = response.json()
        return userStatsData
    
    return None

def get_last_matches_id(puuid, maxMatches=DEFAULT_MAX_PARTIDAS_HISTORICO):
    if puuid:
        match_history_endpoint = f'{RIOT_API_AMERICAS_URL}lol/match/v5/matches/by-puuid/{puuid}/ids'
        match_history_response = requests.get(match_history_endpoint, headers=headers)

        if match_history_response.status_code == 200:
            matches_data = match_history_response.json()

            if isinstance(matches_data, list):
                return matches_data[0:maxMatches]
    return None

def get_match_history_api(puuid, maxMatches=DEFAULT_MAX_PARTIDAS_HISTORICO):
    if puuid:
        ultimasPartidas = get_last_matches_id(puuid, maxMatches)

        if ultimasPartidas:
            results = []
            for id in ultimasPartidas:
                results.append(get_match_by_id(id))       
            return results
        return None
    return None


def get_live_match(puuid):
    if puuid:
        endpoint = f'{RIOT_API_BR_URL}/spectator/v5/active-games/by-summoner/{puuid}'
        response = requests.get(endpoint, headers=headers)

        if response.status_code == 200:
            matche_data = response.json()
            return matche_data
        
    return None


def get_match_by_id(id):
    endpoint = f'{RIOT_API_AMERICAS_URL}lol/match/v5/matches/{id}'
    headers = {'X-Riot-Token': RIOT_API_KEY}
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        match = response.json()
        return match
    
    return None

def get_queue_json():
    urlJson = "https://static.developer.riotgames.com/docs/lol/queues.json"
    response = requests.get(urlJson)

    if response.status_code == 200:
        queueJson = response.json()
        return queueJson

def obter_primeira_versao_ddragon():
    url_ddragon = "https://ddragon.leagueoflegends.com/api/versions.json"
    response = requests.get(url_ddragon)

    if response.status_code == 200:
        versions_json = response.json()

        if versions_json:
            primeira_versao = versions_json[0]
            return primeira_versao
    else:
        print(f"Falha na solicitação. Código de status: {response.status_code}")


    return None

def get_champions_json():
    url_ddragon = "https://ddragon.leagueoflegends.com/cdn/" + str(obter_primeira_versao_ddragon()) + "/data/pt_BR/champion.json"
    response = requests.get(url_ddragon)

    if response.status_code == 200:
        champions = response.json()
        return champions
    else:
        print(f"Falha na solicitação. Código de status: {response.status_code}")


    return None

################ END API RIOT ######################

################ TWITCH API ######################


def check_lol_streaming_now(channel_id):
    endpoint = f'{TWITCH_API_BASE_URL}/streams?user_login={channel_id}'
    headers = {'Client-ID': TWITCH_CLIENT_ID, 'Authorization': f'Bearer {TWITCH_SECRET}'}
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        streamerDetails = response.json()
        return streamerDetails
    
    return None

def get_streamer_details(channel_id):
    endpoint = f'{TWITCH_API_BASE_URL}/users?login={channel_id}'
    headers = {'Client-ID': TWITCH_CLIENT_ID, 'Authorization': f'Bearer {TWITCH_SECRET}'}
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        streamerDetails = response.json()
        return streamerDetails
    
    return None

#def insert_player_online(famous_twitch_player_id, rank, tier, pdl, thumb_url, started_at):
#    player_online, created = PlayersOnline.objects.get_or_create(
#    famousTwitchPlayersLol_id=famous_twitch_player_id,
#    defaults={
#        'rank': rank,
#        'tier': tier,
#        'pdl': pdl,
#        'thumbUrl': thumb_url,
#        'started_at': started_at
#    }
#)

################ RESPONSE MAPS & UTILS ##############################

def map_response_live_match(puuid, live_match):
    try:
        queueJson = get_queue_json()
        championsJson = get_champions_json()
        lolLastVersion = obter_primeira_versao_ddragon()

        queueId = live_match.get('gameQueueConfigId')
        championJsonData = championsJson.get('data')
        filtered_queues = [queue for queue in queueJson if queue["queueId"] == queueId]
  
        if len(filtered_queues) > 0:
            game_type = filtered_queues[0].get('description')
        else:
            game_type = "Desconhecido"
    
        gameId = str(RIOT_API_BR_REGION) + "_" + str(live_match.get('gameId'))
        gamestartTime = live_match.get('gameStartTime')
        gameLength = live_match.get('gameLength')
        participatnts = live_match.get('participants')
        championPlayed = ""

        players_in_match = []
        for participant in participatnts:
        
            campeao_filtrado = {nome: dados for nome, dados in championJsonData.items() if dados.get('key') == str(participant.get('championId'))}
            for nome_campeao, dados_campeao in campeao_filtrado.items():
                nomeCampeao = dados_campeao['name']
                championImg = f'https://ddragon.leagueoflegends.com/cdn/{lolLastVersion}/img/champion/{nomeCampeao}.png'

            if participant.get('puuid') == puuid:
                championPlayed = championImg
            players_in_match.append({
                'summonerName': participant.get('riotId'),
                'teamId': participant.get('teamId'),
                'championId': participant.get('championId'),
                'puuid': participant.get('puuid'),
                'championName': nomeCampeao,
                'championImg': championImg,
            })

        game_end_time = datetime.fromtimestamp(gamestartTime / 1000.0)
        response = {
            'queueId': queueId,
            'gameType': game_type,
            'gamestartTime': format_time_string(game_end_time),	
            'gameLength': gameLength,
            'gameId': gameId,
            'championPlayed': championPlayed,
            'participants': players_in_match,

        }

        return response
    except Exception as e:
        print(e.with_traceback)




def map_response_match_history(puuid, match_history):
    #call riot api to get match history
    try:
        myMatchhistory = []

        queueJson = get_queue_json()
        lolLastVersion = obter_primeira_versao_ddragon()
        for match in match_history:
            queueId = match.get('info').get('queueId')
            matchId = match.get('metadata').get('matchId')
            filtered_queues = [queue for queue in queueJson if queue["queueId"] == queueId]


            #gam    eType = RANKED SOLO 5x5 , RANKED_FLEX_SR etc...
            gameType = filtered_queues[0].get('description')

            # --------- Game Date ------------
            # e.g 3 Dias atrás
            gameStartTime = match.get('info').get('gameStartTimestamp')
            gameEndTime = match.get('info').get('gameEndTimestamp')
            duration = match.get('info').get('gameDuration') 
        
            game_end_time = datetime.fromtimestamp(gameEndTime / 1000.0)

            # Obtenha a diferença em dias

            time_string = format_time_string(game_end_time)


            # --    ------- Game Duration ------------
            gameDuration = gameEndTime - gameStartTime
            # Converta para segundos
            gameDuration_in_seconds = gameDuration / 1000

            # Calcule minutos e segundos
            minutes = int(gameDuration_in_seconds // 60)
            seconds = int(gameDuration_in_seconds % 60)

            # Formate a string
            duration_string = f"{minutes}m {seconds}s"

            # --------- Match Result  ------------
            # e.g Vitoria
            participants = match.get('info').get('participants') if match_history else []
            myPlayer = list(filter(lambda p: p.get("puuid") == puuid, participants))

            win = myPlayer[0]["win"]
            result = "Vitória" if win else "Derrota"

            if minutes <= 6:
                result = "Remake"

            # --------- Champion Details  ------------
            # e.g Garen
            championId = myPlayer[0]["championId"]
            championName = myPlayer[0]["championName"]
            championLevel = myPlayer[0]["champLevel"]
            championImg = f'https://ddragon.leagueoflegends.com/cdn/{lolLastVersion}/img/champion/{championName}.png'
            kills = myPlayer[0]["kills"]
            deaths = myPlayer[0]["deaths"] 
            assists = myPlayer[0]["assists"]
            kda = f'{kills} / {deaths} / {assists}'
            kdaRatio = myPlayer[0]["challenges"]["kda"]
            teamBaronKills = myPlayer[0]["challenges"]["teamBaronKills"]
            teamElderDragonKills = myPlayer[0]["challenges"]["teamElderDragonKills"]
            teamRiftHeraldKills = myPlayer[0]["challenges"]["teamRiftHeraldKills"]
            doubleKills = myPlayer[0]["doubleKills"]
            dragonKills = myPlayer[0]["dragonKills"]
            multikills = myPlayer[0]["challenges"]["multikills"]
            soloKills = myPlayer[0]["challenges"]["soloKills"]
            killingSprees = myPlayer[0]["killingSprees"]
            firstBloodKill = myPlayer[0]["firstBloodKill"]
            firstTowerKill = myPlayer[0]["firstTowerKill"]
            item0 = myPlayer[0]["item0"]
            item1 = myPlayer[0]["item1"]
            item2 = myPlayer[0]["item2"]
            item3 = myPlayer[0]["item3"]
            item4 = myPlayer[0]["item4"]
            item5 = myPlayer[0]["item5"]
            trinket = myPlayer[0]["item6"] 
            lanePlayed = myPlayer[0]["lane"]
            controlWardsPlaced = myPlayer[0]["challenges"]["controlWardsPlaced"]
            totalMinionsKilled = myPlayer[0]["totalMinionsKilled"]

            utlItem0 = f'https://ddragon.leagueoflegends.com/cdn/{lolLastVersion}/img/item/{item0}.png'
            utlItem1 = f'https://ddragon.leagueoflegends.com/cdn/{lolLastVersion}/img/item/{item1}.png'
            utlItem2 = f'https://ddragon.leagueoflegends.com/cdn/{lolLastVersion}/img/item/{item2}.png'
            utlItem3 = f'https://ddragon.leagueoflegends.com/cdn/{lolLastVersion}/img/item/{item3}.png'
            utlItem4 = f'https://ddragon.leagueoflegends.com/cdn/{lolLastVersion}/img/item/{item4}.png'
            utlItem5 = f'https://ddragon.leagueoflegends.com/cdn/{lolLastVersion}/img/item/{item5}.png'
            urklTrinket = f'https://ddragon.leagueoflegends.com/cdn/{lolLastVersion}/img/item/{trinket}.png'

            # --------- Teams  ------------
            teams = []
            for players in participants:
                playerName = players["summonerName"]
                championPlayed = players["championName"]
                champImg = f'https://ddragon.leagueoflegends.com/cdn/{lolLastVersion}/img/champion/{championPlayed}.png'

                teams.append({
                    "playerName": playerName,
                    "champImg": champImg,
                    "championPlayed": championPlayed
                })


            myMatchhistory.append({
                "gameId": matchId,
                "gameType": gameType,
                "time_string": time_string,
                "duration_string": duration_string,
                "duration": duration,
                "result": result,
                "championId": championId,
                "championName": championName,
                "championLevel": championLevel,
                "championImg": championImg,
                "kda": kda,
                "kills": kills,
                "assists": assists,
                "deaths": deaths,
                "kdaRatio": kdaRatio,
                "doubleKills": doubleKills,
                "dragonKills": dragonKills,
                "firstBloodKill": firstBloodKill,
                "firstTowerKill": firstTowerKill,
                "multikills": multikills,
                "teamBaronKills": teamBaronKills,
                "soloKills": soloKills,
                "teamElderDragonKills": teamElderDragonKills,
                "teamRiftHeraldKills": teamRiftHeraldKills,
                "killingSprees": killingSprees,
                "item0": utlItem0,
                "item1": utlItem1,
                "item2": utlItem2,
                "item3": utlItem3,
                "item4": utlItem4,
                "item5": utlItem5,
                "trinket": urklTrinket,
                "lanePlayed": lanePlayed,
                "teams": teams,
                "controlWardsPlaced": controlWardsPlaced,
                "totalMinionsKilled": totalMinionsKilled,
                "win": win
            })
        return myMatchhistory
    except Exception as e:
        print(e)

def format_time_string(game_end_time):
    diff = datetime.now() - game_end_time
    diff_months = diff.days // 30
    diff_years = diff.days // 365
    diff_hours = diff.seconds // 3600
    diff_minutes = (diff.seconds % 3600) // 60
    diff_seconds = diff.seconds % 60

    time_string = ""
    if diff_years > 0:
        time_string = f"Há {diff_years} anos atrás"
    elif diff_months > 0:
        if diff_months == 1:
            time_string = f"{diff_months} mês atrás"
        else:
            time_string = f"{diff_months} meses atrás"
    elif diff.days > 0:
        if diff.days == 1:
            time_string = f"{diff.days} dia atrás"
        else:
            time_string = f"{diff.days} dias atrás"
    elif diff_hours > 0:
        if diff_hours == 1:
            time_string = f"{diff_hours} hora atrás"
        else:
            time_string = f"{diff_hours} horas atrás"
    elif diff_minutes > 0:
        if diff_minutes == 1:
            time_string = f"{diff_minutes} minuto atrás"
        else:
            time_string = f"{diff_minutes} minutos atrás"
    else:
        if diff_seconds == 1:
            time_string = f"{diff_seconds} segundo atrás"
        else:
            time_string = f"{diff_seconds} segundos atrás"
    return time_string
