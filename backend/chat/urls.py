from django.urls import path

from chat import views

app_name = "chat"


urlpatterns = [
    path('conversations/', views.conversations_list, name='conversations'),
]