from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from decouple import config
from django.views.decorators.csrf import csrf_exempt
from decouple import config


from parinya import LINE
import gspread
import os

from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
def create_keyfile_dict():
    key ={
        "type": "service_account",
        "project_id": "iotservices-378810",
        "private_key_id": config('PRIVATE_KEY_ID'),
        "private_key":config('PRIVATE_KEY'),
        "client_email": "iot-service@iotservices-378810.iam.gserviceaccount.com",
        "client_id": "100507726436556655763",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/iot-service%40iotservices-378810.iam.gserviceaccount.com"
    }
    return key


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
# print(type(config('GOOGLE_CREDENTIALS')))
# print(config('GOOGLE_CREDENTIALS'))
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'cerdGoogle.json')
cerds = ServiceAccountCredentials.from_json_keyfile_name(file_path, scope)
client = gspread.authorize(cerds)


class LineBotView(APIView):
    def post(self, request):

        text = request.data.get('text')
        print(request.data)
        if request.headers.get('Authorization') is not None:
            token = request.headers.get('Authorization').split('Bearer ')[1]
            print(token)
            lineNotification = LINE(token)
            lineNotification.sendtext(text)
            del (lineNotification)
        else:
            lineNotification = LINE(config('TOKEN_NOTIFICATION_LINE'))
            lineNotification.sendtext(text)
            del (lineNotification)

        return Response({'status': 200})

    def get(self, request):

        return Response({'status': 200})

REQ_COUNTER = 1

class GoogleAPI(APIView):
    
    def get(self,request):
        global REQ_COUNTER
        sheet = client.open("temperature&humidity").worksheet('Sheet1') # เป็นการเปิดไปยังหน้าชีตนั้นๆ
        
        
        cell=sheet.cell(REQ_COUNTER,1).value
        pprint(cell)
        sheet.update_cell(REQ_COUNTER,1,"แก้ไข")
        cell=sheet.cell(REQ_COUNTER,1).value
        pprint(cell)
        REQ_COUNTER +=1
        return Response({'status': 200})
    
    def post(self,request):
        global REQ_COUNTER
        sheet = client.open("temperature&humidity").worksheet('Sheet1') # เป็นการเปิดไปยังหน้าชีตนั้นๆ
        print(request.data.get('temp'))
        if request.data.get('temp'):
            
            sheet.update_cell(REQ_COUNTER,1,request.data.get('temp'))
            sheet.update_cell(REQ_COUNTER,2,request.data.get('hum'))
            REQ_COUNTER +=1
            return Response({'status': 200})
        
            
        return Response({'status': 500})