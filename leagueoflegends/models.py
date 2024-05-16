from django.db import models


class StreamerTwitchPlayersLol(models.Model):
    name = models.CharField(max_length=400)
    puuid = models.CharField(max_length=1000)
    channelId = models.CharField(max_length=500)
    region = models.CharField(max_length=100, default="BR")
    rank = models.CharField(max_length=400, default="I")
    tier = models.CharField(max_length=100, default="Unranked")
    pdl = models.IntegerField(default=0)
    thumbUrl = models.CharField(max_length=1400, default="", null=True, blank=True)
    started_at = models.DateTimeField(default=None, null=True, blank=True)
    isOnline = models.BooleanField(default=False)
    isPlaying = models.BooleanField(default=False)
    gameNickName = models.CharField(max_length=400, default="")
    gameTag= models.CharField(max_length=12, default="")

    def __str__(self):
        return f"{self.name}  {self.region} {self.isOnline}  {self.isPlaying} {self.puuid}"