from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import app_start, chat_start, on_message


urlpatterns = [
    path("app-start", csrf_exempt(app_start)),
    path('chat-start', csrf_exempt(chat_start)),
    path('hook/on-message', csrf_exempt(on_message)),
]
