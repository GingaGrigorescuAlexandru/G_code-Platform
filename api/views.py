from groq import Groq
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .serializers import UserSerializer
from rest_framework import viewsets
import json

@csrf_exempt
def openai_response(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body) # Gets a dictionary out of the json response
            user_content = body.get('content', '') # Retrieves the prompt from the dictionary

            print(user_content)

            if not user_content.strip():
                return JsonResponse({'error': 'Content cannot be emppty'}, status = 400)

            client = Groq(
                api_key=settings.SECRET_GROK_KEY
            )

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": user_content,
                    }
                ],
                model="llama3-8b-8192",
            )

            return JsonResponse({'response': chat_completion.choices[0].message.content})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status = 500)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

