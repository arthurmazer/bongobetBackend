import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Wallet
from .utils import create_new_wallet, add_to_wallet_history

class WalletAPIView(APIView):
    def get(self,request):
        try:
            user_email = request.query_params.get('user_email')
            
            wallet = Wallet.objects.filter(user=user_email).first()
            if wallet:
                response = {
                    'wallet_quantity': wallet.quantity,
                    'wallet_quantityBetLocked': wallet.quantityBetLocked,
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                new_wallet = create_new_wallet(user_email)
                response = {
                    'wallet_quantity': new_wallet.quantity,
                    'wallet_quantityBetLocked': new_wallet.quantityBetLocked,
                }
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            #print(str(e))
            return Response({'error': 'User not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddFundsApiView(APIView):
    def post(self,request):
        try:
            user_email = request.data.get('user_email')
            quantity = request.data.get('quantity')
            
            wallet = Wallet.objects.filter(user=user_email).first()
            
            if wallet:
                wallet.quantity += float(quantity)
                wallet.save()                
            else:
                return Response({'error': 'Wallet Not Found'}, status=status.HTTP_404_NOT_FOUND)
            
            add_to_wallet_history(userEmail=user_email, value=quantity, description="PIX = Depósito de Fundos")
            response = {
                'wallet_quantity': wallet.quantity,
                'wallet_quantityBetLocked': wallet.quantityBetLocked,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'User not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

        