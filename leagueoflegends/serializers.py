from rest_framework import serializers

class ImagemSerializer(serializers.Serializer):
    caminho_imagem = serializers.CharField()