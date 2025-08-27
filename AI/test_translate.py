import requests
import json
import sys
import os

# 将项目路径添加到系统路径中，以便可以导入Django设置
sys.path.append('F:\\job\\django projects\\Django_demo')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_demo.settings')

import django
django.setup()

from django.conf import settings
from AI.ernie_service import ErnieService

def test_translation():
    """测试AI翻译功能"""
    print("=== AI翻译功能测试 ===")

    # 创建AI服务实例
    service = ErnieService()

    # 测试翻译文本
    test_texts = [
        "Hello, how are you today?",
        "The weather is beautiful today.",
        "I would like to visit China someday."
    ]

    # 测试不同语言的翻译
    target_languages = ['zh', 'ja', 'ko']
    language_names = {
        'zh': '中文',
        'ja': '日文',
        'ko': '韩文'
    }

    for text in test_texts:
        print(f"\n原文: {text}")

        for target_lang in target_languages:
            try:
                # 构造翻译提示
                target_lang_name = language_names.get(target_lang, '中文')
                prompt = f"请将以下文本翻译成{target_lang_name}，只返回翻译结果，不要添加任何其他内容：\n\n{text}"

                # 调用AI服务进行翻译
                translated_text = service.chat_completion(prompt)
                print(f"  {target_lang_name}翻译: {translated_text}")

            except Exception as e:
                print(f"  {target_lang_name}翻译失败: {str(e)}")

def test_ai_recommendation():
    """测试AI旅行推荐功能"""
    print("\n=== AI旅行推荐功能测试 ===")

    # 创建AI服务实例
    service = ErnieService()

    # 测试旅行推荐
    try:
        prompt = "我是一个喜欢自然风光和历史文化的旅行者，预算在5000元左右，希望进行一次为期5天的旅行。请推荐一个合适的旅行目的地和行程安排。"
        recommendation = service.chat_completion(prompt)
        print("旅行推荐结果:")
        print(recommendation)

    except Exception as e:
        print(f"旅行推荐失败: {str(e)}")

def test_basic_chat():
    """测试基本聊天功能"""
    print("\n=== 基本聊天功能测试 ===")

    # 创建AI服务实例
    service = ErnieService()

    # 测试简单对话
    test_prompts = [
        "你好，请简单介绍一下自己。",
        "请推荐一些适合夏天旅行的地方。",
        "告诉我一个有趣的小故事。"
    ]

    for prompt in test_prompts:
        try:
            print(f"\n问题: {prompt}")
            response = service.chat_completion(prompt)
            print(f"回答: {response}")

        except Exception as e:
            print(f"回答失败: {str(e)}")

if __name__ == "__main__":
    # 运行所有测试
    test_basic_chat()
    test_translation()
    test_ai_recommendation()

    print("\n=== 所有测试完成 ===")
