"""
URL configuration for BongobetBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bet.views import GamesBetTypeAPIView, BetTypeAPIView, BetApiView, BetHistoryApiView
from leagueoflegends.views import LolSummonerDataAPIView, LolMatchHistoryAPIView, LiveMatchApiView, RiotAccoutAPIView
from django.urls import include
from wallet.views import WalletAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get_summoner_data/', LolSummonerDataAPIView.as_view(), name='get_summoner_data'),
    path('api/get_match_history/', LolMatchHistoryAPIView.as_view(), name='get_match_history'),
    path('api/get_games_bet_type/', GamesBetTypeAPIView.as_view(), name='get_games_bet_type'),
    path('api/get_bet_type/', BetTypeAPIView.as_view(), name='get_bet_type'),
    path('api/get_live_match/', LiveMatchApiView.as_view(), name='get_live_match'),
    path('api/get_riot_account/', RiotAccoutAPIView.as_view(), name='get_riot_account'),
    path('api/create_bet/', BetApiView.as_view(), name='create_bet'),
    path('api/get_wallet/', WalletAPIView.as_view(), name='get_wallet'),
    path('api/get_bet_history/', BetHistoryApiView.as_view(), name='get_bet_history')
    
]
