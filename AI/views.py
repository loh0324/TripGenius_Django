from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from travel.models import TravelPreference

# 导入文心一言服务 (修改导入路径)
from .ernie_service import ErnieService  # 改为正确的文件名

# 设置日志
logger = logging.getLogger(__name__)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def translate_text(request):
    """通过文心一言API实现文本翻译功能"""
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        target_language = data.get('target_language', 'zh')

        if not text:
            return JsonResponse({'ret': 1, 'msg': '请输入需要翻译的文本'})

        # 构造翻译提示
        language_names = {
            'zh': '中文',
            'en': '英文',
            'ja': '日文',
            'ko': '韩文',
            'fr': '法文',
            'de': '德文'
        }
        
        target_lang_name = language_names.get(target_language, '中文')
        
        prompt = f"请将以下文本翻译成{target_lang_name}，只返回翻译结果，不要添加任何其他内容：\n\n{text}"

        # 调用文心一言API
        service = ErnieService()
        translated_text = service.chat_completion(prompt)

        return JsonResponse({
            'ret': 0,
            'data': {
                'original_text': text,
                'translated_text': translated_text,
                'target_language': target_language
            }
        })
    except Exception as e:
        logger.error(f"翻译失败: {str(e)}")
        return JsonResponse({'ret': 1, 'msg': f'翻译失败: {str(e)}'})

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def ai_recommend(request):
    """通过文心一言API实现AI旅行推荐功能"""
    try:
        # 获取用户的旅行偏好
        try:
            preference = request.user.travel_preference
            preferences_info = {
                'preferred_activities': preference.preferred_activities,
                'budget_range_min': preference.budget_range_min,
                'budget_range_max': preference.budget_range_max,
                'preferred_climate': preference.preferred_climate,
                'special_requirements': preference.special_requirements,
            }
        except TravelPreference.DoesNotExist:
            preferences_info = {}

        data = json.loads(request.body)
        user_input = data.get('preferences', '')
        
        # 构造推荐提示
        prompt = "你是一个专业的旅行规划师，请根据以下信息为用户推荐旅行计划：\n\n"
        
        if preferences_info:
            prompt += "用户偏好信息：\n"
            if preferences_info['preferred_activities']:
                prompt += f"- 偏好的活动类型: {preferences_info['preferred_activities']}\n"
            if preferences_info['budget_range_min'] and preferences_info['budget_range_max']:
                prompt += f"- 预算范围: {preferences_info['budget_range_min']}-{preferences_info['budget_range_max']}元\n"
            if preferences_info['preferred_climate']:
                prompt += f"- 偏好的气候: {preferences_info['preferred_climate']}\n"
            if preferences_info['special_requirements']:
                prompt += f"- 特殊要求: {preferences_info['special_requirements']}\n"
        
        if user_input:
            prompt += f"\n用户具体需求: {user_input}\n"
        
        prompt += "\n请给出详细的旅行计划推荐，包括目的地、行程安排、注意事项等。以清晰的格式返回结果。"

        # 调用文心一言API
        service = ErnieService()
        recommendation = service.chat_completion(prompt)

        return JsonResponse({
            'ret': 0,
            'data': {
                'recommendation': recommendation
            }
        })
    except Exception as e:
        logger.error(f"获取AI推荐失败: {str(e)}")
        return JsonResponse({'ret': 1, 'msg': f'获取AI推荐失败: {str(e)}'})
