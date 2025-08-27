import pytest
import requests
from django.test import Client
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    """创建一个用于API测试的客户端"""
    return Client()

@pytest.fixture
def auth_headers():
    """返回认证所需的headers"""
    # 先登录获取session
    client = requests.Session()
    login_data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    response = client.post('http://localhost:8000/api/mgr/signin', data=login_data)

    # 返回带有认证信息的headers
    return {
        'Cookie': f"sessionid={client.cookies.get('sessionid')}"
    }

@pytest.fixture
def test_user(django_user_model):
    """创建测试用户"""
    return django_user_model.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )

@pytest.fixture
def authenticated_client(test_user):
    """创建一个已认证的Django测试客户端"""
    client = Client()
    client.login(username='testuser', password='testpass123')
    return client

@pytest.fixture
def authenticated_requests_session(test_user):
    """创建一个已认证的requests会话"""
    session = requests.Session()
    login_data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    login_response = session.post('http://localhost:8000/api/mgr/signin', data=login_data)
    
    # 确保登录成功
    assert login_response.status_code == 200
    assert 'sessionid' in login_response.cookies
    
    return session
