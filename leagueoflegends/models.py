from django.db import models


#Usado para armazenar dados do usuário do lol vindo da API para fins de cache
class LolUser(models.Model):
    lolUserid = models.TextField()
    puuid = models.TextField()
    summonerName = models.TextField()
    accountId = models.TextField(default="")
    profileIconUrl = models.TextField(default="")
    summonerLevel = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now_add=True)
    tierRankedSolo = models.TextField(default="", null=True)
    tierRankedFlex = models.TextField(default="", null=True )
    rankRankedSolo = models.TextField(default="", null=True)
    rankRankedFlex = models.TextField(default="", null=True)
    pdlRankedSolo = models.IntegerField(default=0, null=True)
    pdlRankedFlex = models.IntegerField(default=0, null=True)
    winsSolo = models.IntegerField(default=0, null=True)
    lossesSolo = models.IntegerField(default=0, null=True)
    winsFlex = models.IntegerField(default=0, null=True)
    lossesFlex = models.IntegerField(default=0, null=True)
    tierTFT = models.TextField(default="", null=True)
    rankTFT = models.TextField(default="", null=True)
    pdlTFT = models.IntegerField(default=0, null=True)
    winsTFT = models.IntegerField(default=0, null=True)
    lossesTFT = models.IntegerField(default=0, null=True)

