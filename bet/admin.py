from django.contrib import admin

# Register your models here.
from bet.models import Bet, Game, BetType, GameType, BetLol

admin.site.register(Bet)
admin.site.register(Game)
admin.site.register(BetType)
admin.site.register(GameType)
admin.site.register(BetLol)