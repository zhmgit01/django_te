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
