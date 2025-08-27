# 用来写管理员的登录和登出的api请求的
# 相当于把请求里面的参数密码 用户名取出来
# 去和数据库里面的对比 一致就通过 不一致就失败
# 加密是django内置app 里面库方法 直接做好了登录验证的功能

from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

# 登录处理
@csrf_exempt
def signin(request):
    # 从 HTTP POST 请求中获取用户名、密码参数
    userName = request.POST.get('username')
    passWord = request.POST.get('password')

    # 使用 Django auth 库里面的 方法校验用户名、密码 本身库直接比对
    user = authenticate(username=userName, password=passWord)

    # 如果能找到用户，并且密码正确
    if user is not None:
        if user.is_active:
            login(request, user)
            # 在session中存入用户信息
            request.session['usertype'] = 'user'  # 普通用户
            request.session['userid'] = user.id
            request.session['username'] = user.username
            request.session.save()  # 保存session
            return JsonResponse({'ret': 0, 'msg': '登录成功', 'userid': user.id, 'username': user.username})
        else:
            return JsonResponse({'ret': 1, 'msg': '用户已经被禁用'})
    # 否则就是用户名、密码有误
    else:
        return JsonResponse({'ret': 1, 'msg': '用户名或者密码错误'})

# 登出处理
def signout(request):
    # 清除session中的用户信息
    if 'userid' in request.session:
        del request.session['userid']
    if 'username' in request.session:
        del request.session['username']
    if 'usertype' in request.session:
        del request.session['usertype']
    
    # 使用登出方法
    logout(request)
    return JsonResponse({'ret': 0, 'msg': '登出成功'})

# 注册处理
@csrf_exempt
def register(request):
    # 从 HTTP POST 请求中获取注册信息
    userName = request.POST.get('username')
    passWord = request.POST.get('password')
    email = request.POST.get('email')

    # 检查必填字段
    if not userName or not passWord:
        return JsonResponse({'ret': 1, 'msg': '用户名和密码不能为空'})

    # 检查用户名是否已存在
    if User.objects.filter(username=userName).exists():
        return JsonResponse({'ret': 1, 'msg': '用户名已存在'})

    try:
        # 创建用户
        user = User.objects.create_user(
            username=userName,
            password=passWord,
            email=email
        )
        
        # 注册成功后自动登录
        login(request, user)
        # 在session中存入用户信息
        request.session['usertype'] = 'user'  # 普通用户
        request.session['userid'] = user.id
        request.session['username'] = user.username
        request.session.save()  # 保存session
        
        return JsonResponse({'ret': 0, 'msg': '注册成功', 'userid': user.id, 'username': user.username})
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'注册失败: {str(e)}'})

# 检查登录状态
def check_login(request):
    """
    检查用户登录状态
    """
    if request.user.is_authenticated:
        return JsonResponse({
            'ret': 0,
            'msg': '用户已登录',
            'userid': request.user.id,
            'username': request.user.username
        })
    else:
        # 检查session中是否有用户信息（备用方案）
        userid = request.session.get('userid', None)
        username = request.session.get('username', None)
        
        if userid and username:
            try:
                user = User.objects.get(id=userid)
                login(request, user)  # 重新登录用户
                return JsonResponse({
                    'ret': 0,
                    'msg': '用户已登录',
                    'userid': userid,
                    'username': username
                })
            except User.DoesNotExist:
                # 清除无效的session数据
                if 'userid' in request.session:
                    del request.session['userid']
                if 'username' in request.session:
                    del request.session['username']
                if 'usertype' in request.session:
                    del request.session['usertype']
                return JsonResponse({'ret': 1, 'msg': '用户未登录'})
        else:
            return JsonResponse({'ret': 1, 'msg': '用户未登录'})
