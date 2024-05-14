from django.db import models


class FamousTwitchPlayersLol(models.Model):
    name = models.CharField(max_length=400)
    puuid = models.CharField(max_length=1000)
    channelId = models.CharField(max_length=500)
    region = models.CharField(max_length=100, default="BR")

    def __str__(self):
        return f"{self.name}  {self.region}"
    
class PlayersOnline(models.Model):
    famousTwitchPlayersLol = models.ForeignKey(FamousTwitchPlayersLol, on_delete=models.CASCADE, related_name="famousTwitchPlayersLol") 
    rank = models.CharField(max_length=400)
    tier = models.CharField(max_length=100)
    pdl = models.IntegerField(default=0)
    thumbUrl = models.CharField(max_length=1400)
    started_at = models.DateTimeField()

    def __str__(self):
        return f"{self.famousTwitchPlayersLol.name}  {self.rank}"