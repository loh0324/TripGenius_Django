from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import UserProfile, TravelPreference, TravelPlan, Itinerary, Destination, Attraction, TravelItem  # 确保导入所有模型
import json
from django.utils import timezone
from datetime import datetime
from django.db import transaction

# 用户相关视图
@login_required
def user_profile(request):
    """获取用户资料"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    try:
        preference = request.user.travel_preference
    except TravelPreference.DoesNotExist:
        preference = TravelPreference.objects.create(user=request.user)

    return JsonResponse({
        'ret': 0,
        'data': {
            'username': request.user.username,
            'email': request.user.email,
            'phone': profile.phone,
            'birth_date': profile.birth_date,
            'preferred_activities': preference.preferred_activities,
            'budget_range_min': preference.budget_range_min,
            'budget_range_max': preference.budget_range_max,
            'preferred_climate': preference.preferred_climate,
            'special_requirements': preference.special_requirements,
        }
    })

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def update_profile(request):
    """更新用户资料"""
    try:
        data = json.loads(request.body)
        profile_data = data.get('profile', {})
        preference_data = data.get('preference', {})

        # 更新用户资料
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        for field, value in profile_data.items():
            if hasattr(profile, field):
                setattr(profile, field, value)
        profile.save()

        # 更新旅行偏好
        preference, created = TravelPreference.objects.get_or_create(user=request.user)
        for field, value in preference_data.items():
            if hasattr(preference, field):
                setattr(preference, field, value)
        preference.save()

        return JsonResponse({'ret': 0, 'msg': '资料更新成功'})
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'更新失败: {str(e)}'})

# 旅行计划相关视图
@login_required
def list_plans(request):
    """列出用户的旅行计划"""
    try:
        plans = request.user.travel_plans.values()
        return JsonResponse({
            'ret': 0,
            'data': list(plans),
            'total': len(list(plans))
        })
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'获取计划列表失败: {str(e)}'})

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def create_plan(request):
    """创建旅行计划"""
    try:
        data = json.loads(request.body)
        plan_data = data.get('plan', {})

        plan = TravelPlan.objects.create(
            user=request.user,
            title=plan_data.get('title', ''),
            destination=plan_data.get('destination', ''),
            start_date=plan_data.get('start_date'),
            end_date=plan_data.get('end_date'),
            description=plan_data.get('description', ''),
            budget=plan_data.get('budget')
        )

        return JsonResponse({
            'ret': 0,
            'msg': '计划创建成功',
            'plan_id': plan.id
        })
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'创建计划失败: {str(e)}'})

@login_required
def plan_detail(request, plan_id):
    """获取旅行计划详情"""
    try:
        plan = get_object_or_404(TravelPlan, id=plan_id, user=request.user)

        # 获取相关的每日行程
        itineraries = list(plan.itineraries.values())

        return JsonResponse({
            'ret': 0,
            'data': {
                'plan': {
                    'id': plan.id,
                    'title': plan.title,
                    'destination': plan.destination,
                    'start_date': plan.start_date,
                    'end_date': plan.end_date,
                    'description': plan.description,
                    'budget': plan.budget,
                    'created_at': plan.created_at,
                    'updated_at': plan.updated_at,
                },
                'itineraries': itineraries
            }
        })
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'获取计划详情失败: {str(e)}'})

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def update_plan(request, plan_id):
    """更新旅行计划"""
    try:
        plan = get_object_or_404(TravelPlan, id=plan_id, user=request.user)
        data = json.loads(request.body)
        plan_data = data.get('plan', {})

        for field, value in plan_data.items():
            if hasattr(plan, field):
                setattr(plan, field, value)
        plan.save()

        return JsonResponse({'ret': 0, 'msg': '计划更新成功'})
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'更新计划失败: {str(e)}'})

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def delete_plan(request, plan_id):
    """删除旅行计划"""
    try:
        plan = get_object_or_404(TravelPlan, id=plan_id, user=request.user)
        plan.delete()
        return JsonResponse({'ret': 0, 'msg': '计划删除成功'})
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'删除计划失败: {str(e)}'})

# 每日行程相关视图
@login_required
@csrf_exempt
@require_http_methods(["POST"])
def create_itinerary(request, plan_id):
    """创建每日行程"""
    try:
        plan = get_object_or_404(TravelPlan, id=plan_id, user=request.user)
        data = json.loads(request.body)
        itinerary_data = data.get('itinerary', {})

        itinerary = Itinerary.objects.create(
            plan=plan,
            date=itinerary_data.get('date'),
            title=itinerary_data.get('title', ''),
            description=itinerary_data.get('description', ''),
            start_time=itinerary_data.get('start_time'),
            end_time=itinerary_data.get('end_time'),
            location=itinerary_data.get('location', ''),
            notes=itinerary_data.get('notes', '')
        )

        return JsonResponse({
            'ret': 0,
            'msg': '行程创建成功',
            'itinerary_id': itinerary.id
        })
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'创建行程失败: {str(e)}'})

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def update_itinerary(request, itinerary_id):
    """更新每日行程"""
    try:
        itinerary = get_object_or_404(Itinerary, id=itinerary_id, plan__user=request.user)
        data = json.loads(request.body)
        itinerary_data = data.get('itinerary', {})

        for field, value in itinerary_data.items():
            if hasattr(itinerary, field):
                setattr(itinerary, field, value)
        itinerary.save()

        return JsonResponse({'ret': 0, 'msg': '行程更新成功'})
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'更新行程失败: {str(e)}'})

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def delete_itinerary(request, itinerary_id):
    """删除每日行程"""
    try:
        itinerary = get_object_or_404(Itinerary, id=itinerary_id, plan__user=request.user)
        itinerary.delete()
        return JsonResponse({'ret': 0, 'msg': '行程删除成功'})
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'删除行程失败: {str(e)}'})
