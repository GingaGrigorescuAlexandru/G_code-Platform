from groq import Groq
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from .models import User
from .serializers import UserSerializer
from rest_framework import viewsets

def openai_response(request):
    client = Groq(
        api_key=settings.SECRET_OPENAI_KEY
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Explain the importance of fast language models",
            }
        ],
        model="llama3-8b-8192",
    )

    return JsonResponse({'response': chat_completion.choices[0].message.content})



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

