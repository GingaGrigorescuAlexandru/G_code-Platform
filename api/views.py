from groq import Groq
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import User
from .forms import UserForm
from .serializers import UserSerializer
from rest_framework import viewsets
import json
from django.contrib.auth import login

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status = 400)
        form = UserForm(data)

        if form.is_valid():
            user = form.save(commit = False)
            user.save()
            login(request, user)

            return JsonResponse({'message': 'User created successfully'}, status = 201)
        else:
            return JsonResponse({'error': form.errors}, status = 400)

    return JsonResponse({'message': 'Invalid Request'}, status = 400)

@csrf_exempt
def openai_response(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body) # Gets a dictionary out of the json response
            user_content = body.get('content', '') # Retrieves the prompt from the dictionary

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

