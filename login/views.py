from django.shortcuts import render,redirect
from . import models
from django.contrib.auth.hashers import make_password,check_password
import hashlib


# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'GET':
        pass
        return render(request, 'login.html')
    elif request.method == 'POST':
        context = {
            'message': ''
        }
        # 用户提交表单
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username,password)

        # 验证账户和密码
        user = models.User.objects.filter(name=username).first()
        if user:
            if _hash_password(password) == user.hash_password:                  # 匹配哈希密码，如果存在哈希密码可以登录，不存在登录不上
            # if user.password == password:
                context['message'] = '登录成功'
                # 服务器设置sessionid和其他用户信息。sessionid（服务器）
                request.session['is_login'] = True
                request.session['username'] = user.name
                request.session['userid'] = user.id
                return redirect('/index/')          # 返回的响应中包含set-cookie(sessionid='fghjdfSDFGH'),浏览器收到响应后会把sessionid存到cookie中。
            else:
                context['message'] = '密码不正确'
                return render(request, 'login.html', context=context)
        else:
            context['message'] = '未注册'
            return render(request,'login.html', context=context)


def register(request):
    if request.method == 'GET':
        # 注册表单
        return render(request,'register.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        ## 后端表单验证
        # if not(username.strip() and password.strip() and email.strip()):
        #     return render('/register',context={'message':'某个字段为空'})
        # if len(username) > 20 or len(password) > 20:
        #     print('用户名或密码长度不能超过20')

        # 'insert into login_user (name,password,email) values (%s,%s,%select )' %('','','')
        user = models.User.objects.filter(email=email).first()
        if user:
            return render(request,'register.html',context={'message':'用户已注册'})
        # 加密密码
        hash_password = _hash_password(password)
        # 写数据库
        try:
            user = models.User(name=username,password=password,hash_password=hash_password,email=email)
            user.save()
            print('注册成功')
            return render(request,'login.html',context={'message':'注册成功，请继续登录'})
        except Exception as e:
            print('保存失败',e)
            return redirect('/register/')



def logout(request):
    """ 退出 """

    # 清除session 登陆
    request.session.flush()                     # 清除此用户的sessionid对应的所有sessiondata
    # del request.session['user_id']            # 清除某个session键值
    return redirect('/index/')


def _hash_password(password):
    sha = hashlib.sha256()
    sha.update(password.encode(encoding='utf-8'))
    return sha.hexdigest()


# def _hash_password(password,salt='asdf'):
#     """ 哈希密码用户注册密码，加盐版 """
#     sha = hashlib.sha256
#     sha.update(password.encode(encoding='utf-8'))
#     return '$asdf$'+sha.hexdigest()


# 查询数据库             'select * from login_user where name=%s and password = %s' %(username,password)