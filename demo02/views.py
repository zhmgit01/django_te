from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def loginView(request):
    '''登录'''
    if request.method == "POST":
        username = request.POST.get('username', '')
        psw = request.POST.get('password', '')
        user = authenticate(username=username, password=psw)
        if user is not None:
            if user.is_active:
                login(request, user=user)
                request.session['user'] = username
                return HttpResponseRedirect('/success')  # 重定向到指定的 url
        else:
            return render(request, 'loginView.html', {'msg': '账号或密码错误！'})
    else:
        return render(request, 'loginView.html', {'msg': ''})


@login_required
def successView(request):
    '''登录成功页'''
    return render(request, 'success.html', {'msg': ''})


def logoutView(request):
    '''退出登陆'''
    logout(request)  # 该方法，会将存储在用户session的数据全部清空
    return render(request, 'loginView.html', {'msg': ''})
