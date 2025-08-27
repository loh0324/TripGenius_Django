from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    # 用户相关
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),

    # 旅行计划相关
    path('plans/', views.list_plans, name='list_plans'),
    path('plans/create/', views.create_plan, name='create_plan'),
    path('plans/<int:plan_id>/', views.plan_detail, name='plan_detail'),
    path('plans/<int:plan_id>/update/', views.update_plan, name='update_plan'),
    path('plans/<int:plan_id>/delete/', views.delete_plan, name='delete_plan'),

    # 每日行程相关
    path('plans/<int:plan_id>/itineraries/create/', views.create_itinerary, name='create_itinerary'),
    path('itineraries/<int:itinerary_id>/update/', views.update_itinerary, name='update_itinerary'),
    path('itineraries/<int:itinerary_id>/delete/', views.delete_itinerary, name='delete_itinerary'),
]
