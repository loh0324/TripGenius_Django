import pytest
import json

class TestAITranslateAPI:
    base_url = 'http://localhost:8000/api/ai'

    def test_translate_text_success(self, authenticated_requests_session):
        """测试文本翻译成功"""
        # 准备翻译数据
        payload = {
            'text': 'Hello, how are you today?',
            'target_language': 'zh'
        }

        response = authenticated_requests_session.post(
            f'{self.base_url}/translate/',
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )

        assert response.status_code == 200
        data = response.json()
        assert data['ret'] == 0
        assert 'data' in data
        assert 'original_text' in data['data']
        assert 'translated_text' in data['data']
        assert data['data']['original_text'] == payload['text']
        assert data['data']['target_language'] == payload['target_language']

    def test_translate_text_without_login(self, api_client):
        """测试未登录用户尝试翻译"""
        payload = {
            'text': 'Hello, how are you today?',
            'target_language': 'zh'
        }

        response = api_client.post(
            '/api/ai/translate/',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # 未登录应该返回403 Forbidden
        assert response.status_code == 403

    def test_translate_text_empty_content(self, authenticated_requests_session):
        """测试翻译空文本"""
        payload = {
            'text': '',  # 空文本
            'target_language': 'zh'
        }

        response = authenticated_requests_session.post(
            f'{self.base_url}/translate/',
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )

        assert response.status_code == 200
        data = response.json()
        assert data['ret'] == 1  # 应该返回错误
        assert '请输入需要翻译的文本' in data['msg']

    def test_translate_text_various_languages(self, authenticated_requests_session):
        """测试多种语言翻译"""
        test_cases = [
            {'text': 'Hello, world', 'target_language': 'zh'},
            {'text': '你好，世界', 'target_language': 'en'},
            {'text': 'Hello, world', 'target_language': 'ja'},
            {'text': 'Hello, world', 'target_language': 'ko'},
        ]

        for case in test_cases:
            payload = {
                'text': case['text'],
                'target_language': case['target_language']
            }

            response = authenticated_requests_session.post(
                f'{self.base_url}/translate/',
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )

            assert response.status_code == 200
            data = response.json()
            assert data['ret'] == 0
            assert 'data' in data
            assert 'translated_text' in data['data']

    def test_translate_text_invalid_language(self, authenticated_requests_session):
        """测试无效目标语言"""
        payload = {
            'text': 'Hello, how are you today?',
            'target_language': 'invalid_lang'  # 无效语言代码
        }

        response = authenticated_requests_session.post(
            f'{self.base_url}/translate/',
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )

        # 即使语言代码无效，也应该正常处理（默认为中文）
        assert response.status_code == 200
        data = response.json()
        assert data['ret'] == 0
        assert 'data' in data
