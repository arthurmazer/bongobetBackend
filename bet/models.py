from django.db import models
from enum import Enum
from django.contrib.auth.models import User

#Status da Aposta
class StatusBet(Enum):
    APOSTADO = 0
    VITORIA = 1
    DERROTA = 2
    EXPIRADA = 3
    PEDIDO_REEMBOLSO = 4
    REEMBOLSADO = 6

#Modelo para Jogos. Ex: League of Legends, Runeterra, TFT, etc
class Game(models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return f"{self.name}"

#Modelo para Modos de Jogo. Ex: Ranked, Normal, ARAM, etc    
class GameType(models.Model):
    name = models.CharField(max_length=400)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="game")
    tag = models.CharField(max_length=200, default="")
    queueId = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"

#Modelo para Bets
class BetType(models.Model):
    name = models.CharField(max_length=400)
    condicao = models.CharField(max_length=400)
    multiplicadorMin = models.FloatField()
    multiplicadorMax = models.FloatField()
    urlThumb = models.TextField(default="")
    color = models.TextField(default="")
    gametype = models.ForeignKey(GameType, on_delete=models.CASCADE, related_name="gameType")
    subDetails = models.TextField(default="", null=True, blank=True)
    type = models.CharField(max_length=400, default="")
    

    def __str__(self):
        return f"{self.color} {self.name} {self.multiplicadorMin} {self.condicao} {self.gametype}"
    

    
#Modelo de aposta
class Bet(models.Model):
    userEmail = models.CharField(max_length=200, default="")
    date = models.DateTimeField(auto_now_add=True)
    idUltimoJogo = models.TextField()
    puuid = models.TextField(null=True)

    def __str__(self):
        return f"{self.userEmail}  {self.puuid}  {self.date}"
    

#Aposta em LOL
class BetLol(models.Model):
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE)
    betType = models.ForeignKey(BetType, on_delete=models.CASCADE)
    statusBet = models.IntegerField(choices=[(tag.value, tag.name) for tag in StatusBet], default=0)
    odds = models.FloatField(default=0.0)
    quantity = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"{self.bet} {self.betType} {self.quantity} {self.statusBet}"
    
