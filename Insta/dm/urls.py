from django.urls import path
from dm.views import *

urlpatterns = [
    path('inbox/', inbox, name="inbox"),
    path('directs/<username>', Directs, name="directs"),
    path('send/', sendMessage, name="send-message"),
    
    ]