from django.urls import path
from . import views

app_name = 'ai'

urlpatterns = [
    path('translate/', views.translate_text, name='translate_text'),  # 翻译功能
    path('recommend/', views.ai_recommend, name='ai_recommend'),     # 旅行推荐
]
