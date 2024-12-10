from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/', admin.site.urls),

    path('ai_response/', views.openai_response, name = 'ai_response'),
    path('register/', views.register, name = 'register')
]
