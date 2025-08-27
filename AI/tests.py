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

def test_api():
    # 从Django设置中获取API Key
    api_key = getattr(settings, 'ERNIE_API_KEY', None)

    if not api_key:
        print("错误：请先在settings.py中配置ERNIE_API_KEY")
        return

    print(f"API Key长度: {len(api_key)}")

    # 使用正确的API端点
    url = "https://www.blueshirtmap.com/v1/chat/completions"

    # 请求数据
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": "你好，请用中文回复：这是一条测试消息"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }

    # 请求头
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    print(f"正在发送请求到API: {url}")
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        print(f"响应状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("API调用成功！")
            print("响应内容:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

            # 提取回复内容
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                print(f"\nAI回复: {content}")
            else:
                print("响应格式不符合预期")
        else:
            print(f"API调用失败: {response.status_code}")
            print(f"响应内容: {response.text}")

    except Exception as e:
        print(f"请求出错: {str(e)}")

if __name__ == "__main__":
    test_api()
