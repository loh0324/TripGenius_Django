import pytest
import requests
from django.contrib.auth.models import User

class TestAuthAPI:
    base_url = 'http://localhost:8000/api/mgr'

    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前准备"""
        # 创建测试用户
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.test_user.save()

    def test_valid_login(self):
        """测试有效用户登录"""
        payload = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = requests.post(f'{self.base_url}/signin', data=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['ret'] == 0
        assert 'sessionid' in response.cookies

    def test_invalid_username_login(self):
        """测试无效用户名登录"""
        payload = {
            'username': 'invaliduser',
            'password': 'testpass123'
        }
        response = requests.post(f'{self.base_url}/signin', data=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['ret'] == 1

    def test_invalid_password_login(self):
        """测试无效密码登录"""
        payload = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = requests.post(f'{self.base_url}/signin', data=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['ret'] == 1

    def test_logout(self):
        """测试用户登出"""
        # 先登录
        login_payload = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        login_response = requests.post(f'{self.base_url}/signin', data=login_payload)

        # 使用登录获得的session进行登出
        session_id = login_response.cookies.get('sessionid')
        headers = {'Cookie': f'sessionid={session_id}'}
        response = requests.get(f'{self.base_url}/signout', headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data['ret'] == 0
