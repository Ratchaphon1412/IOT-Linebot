from django.urls import include, path
from .views import *

urlpatterns = [
    path('message/',LineBotView.as_view()),
    path('googlesheet/',GoogleAPI.as_view()),
    
]