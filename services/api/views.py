from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from decouple import config
from django.views.decorators.csrf import csrf_exempt

from parinya import LINE




class LineBotView(APIView):
    def post(self, request):
         
        text = request.data.get('text')
        print(request.data)
        if request.headers.get('Authorization') is not None :
            token = request.headers.get('Authorization').split('Bearer ')[1]
            print(token)
            lineNotification = LINE(token)
            lineNotification.sendtext(text)
            del(lineNotification)
        else:
            lineNotification = LINE(config('TOKEN_NOTIFICATION_LINE'))
            lineNotification.sendtext(text)
            del(lineNotification)
        
        return Response({'status': 200})
        
    def get(self, request):
       
        return Response({'status': 200})
    
    
