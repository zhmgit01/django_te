from django.shortcuts import render
from django.http import HttpResponse
from hello.models import User


# Create your views here.

# 测试get请求提交
def test_qq(request):
    """请求页面"""
    return render(request, 'get_demo.html')


# 提交后返回页面
def result_qq(request):
    """返回结果"""
    if request.method == 'GET':
        # 获取提交的数据
        # key 对应输入框中的name属性值 name="qq"
        # request.GET 可以看成一个字典，用GET方法传递的值都会保存到其中，
        # 可以用 request.GET['key_name']来取值,但是当key值不存在时，会报错“MultiValueDictKeyError”。
        r = request.GET.get('qq', None)  # key_name 不存在时，不会报错
        res = ''
        try:
            if int(r) % 2:
                res = '大吉大利！'
            else:
                res = '恭喜发财！'
        except:
            res = '请输入正确的qq号！'

        return HttpResponse('测试结果：{}'.format(res))
    else:
        render(request, 'get_demo.html')


def user(request):
    """获取用户的mail"""
    res = ''
    if request.method == 'GET':
        r = request.GET.get('name', None)
        # filter相当于SQL中的WHERE，可设置条件过滤结果
        res = User.objects.filter(user_name="%s" % r)
        try:
            res = res[0].mail
        except:
            res = "未查询到数据！"
        return render(request, 'name.html', {"email": res})
    else:
        return render(request, 'name.html', {"email": res})


# 加密密码，django 中提供
from django.contrib.auth.hashers import make_password, check_password


# post 请求处理流程
def register(request):
    """注册页面"""
    res = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        psw = request.POST.get('password')
        mail = request.POST.get('mail')

        # 查询数据库中是否由此用户名
        user_list = User.objects.filter(user_name=username)
        if user_list:
            # 如果已经注册给提示
            res = '{}用户已经被注册！'.format(username)
            return render(request, 'register.html', {'rename': res})
        else:
            # 如果没有注册过，进行注册
            # 第一种写法 （建议）
            user_new = User()
            user_new.user_name = username
            # 加密方法
            user_new.psw = make_password(psw)
            user_new.mail = mail
            user_new.save()

            # 第二种写法
            # user_new = User(user_name=username,
            #                 psw=psw,
            #                 mail=mail)
            # user_new.save()

            return render(request, 'login.html', {'rename': res})

    return render(request, 'register.html')


def login(request):
    """登录页面"""
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        # 获取页面用户名和密码
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 查询用户名和密码
        # user_obj = User.objects.filter(user_name=username,psw=password)

        ret = User.objects.filter(user_name=username).first()
        # 校验密码 一致返回True 不一致返回False
        is_psw_true = check_password(password, ret.psw)

        # if user_obj:
        if is_psw_true:
            return HttpResponse('登录成功！')
        else:
            return HttpResponse('用户名或密码错误！')


def reset_pwd(request):
    """修改密码"""
    res = ''
    if request.method == 'GET':
        return render(request, 'reset_pwd.html', {'msg': res})
    if request.method == 'POST':
        # 获取页面中值
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        new_pwd = request.POST.get('new')

        if pwd == new_pwd:
            res = '新密码和旧密码不能重复！'
            return render(request, 'reset_pwd.html', {'msg': res})
        else:
            # 查询数据库是否有此用户名
            user_list = User.objects.filter(user_name=username)
            if not user_list:
                # 如果没有此用户
                res = '{}用户未注册'.format(username)
                return render(request, 'reset_pwd.html', {'msg': res})
            else:
                # 如果注册过，判断密码对不对
                ret = User.objects.filter(user_name=username).first()
                # 校验密码
                is_pwd_true = check_password(pwd, new_pwd)
                if is_pwd_true:
                    user = User()
                    user.psw = make_password(new_pwd)
                    user.save()
                    res = '密码修改成功！'
                else:
                    res = '密码错误！'
                return render(request, 'reset_pwd.html', {'msg': res})
