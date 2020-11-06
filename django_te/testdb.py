# -*- coding:utf-8 -*-
# @FileName  :testdb.py
# @Time      :2020/11/5 15:27
# @Author    :zhm
import json

from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from hello.models import Test, User


def testdb(request):
    test1 = Test(name='yoyo')
    test1.save()
    return HttpResponse('数据库hello_test添加name成功！')


def add_user(request):
    """新增数据"""
    test2 = User(user_name='zhm',
                 mail='qq@qq.com',
                 psw='111111')
    test2.save()
    return HttpResponse('数据新增成功！')


def update_psw(request):
    """更新数据"""
    test3 = User.objects.get(user_name='zhm')
    test3.mail = 'tt@qq.com'
    test3.psw = '222222'
    test3.save()

    # 另外一种方式
    # Test.objects.filter(id=1).update(name='google')

    # 修改所有的列
    # Test.objects.all().update(name='google')
    return HttpResponse('<p>密码修改成功</p>')


def delete_user(request):
    """删除数据"""
    # 删除数据 user_name='yoyo'
    test4 = User.objects.get(user_name='zhm')
    test4.delete()

    # 另外一种方式
    Test.objects.filter(id=1).delete()

    # 删除所有数据
    # Test.objects.all().delete()
    return HttpResponse('<p>删除成功</p>')


"""
关于查询：

1、通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
a = User.objects.all()

2、filter相当于SQL中的WHERE，可设置条件过滤结果
b = User.objects.filter(id=1)

3、获取单个对象
c = User.objects.get(id=1)

4、限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
d = User.objects.order_by('name')[0:2]

5、查询结果排序,前面加 - 代表降序
e = User.objects.order_by("id")

6、上面的方法可以连着使用
f = User.objects.filter(name="runoob").order_by("id")

7、exclude() 查询不包含筛选条件的对象
et = User.objects.exclude(user_name='zhm')

8、reverse() 将查询结果反向排序 与 order_by("id") 功能一致
ret = User.objects.order_by("mail").reverse()

9、values_list() 返回的是元组
ret=User.objects.all().values_list("user_name", "mail")

10、distinct() 从返回结果中剔除重复纪录
ret=User.objects.all().values("user_name", "mail").distinct()

11、first()：返回第一条记录
12、last()：返回最后一条记录
13、exists()：返回布尔值
14、count()：返回int类型
"""


def select_mail(request):
    """查询mail的值"""

    # 方式一、可以查询单个结果直接获取mail值
    # m = User.objects.get(user_name='zhm').mail

    # 方式二、filter相当于sql中的where，可设置条件过滤结果
    ret = User.objects.filter(user_name='zhm',
                              psw='111111')
    # 查询结果是list，取下标后，获取mail字段的值
    try:
        r = ret[0].mail
    except:
        r = 'null'
    return HttpResponse('<p>查询结果：{}</p>'.format(r))


def select_all(request):
    """查询user表中的所有数据"""
    users = ""
    psws = ""
    mails = ""
    ret = User.objects.all()

    # 返回queryset对象
    for i in ret:
        users += " " + i.user_name  # 获取user_name字段
        psws += " " + i.psw  # 获取psw字段
        mails += " " + i.mail  # 获取mail字段

    return HttpResponse("""
    <p>查询user结果：{}</p>
    <p>查询user结果：{}</p>
    <p>查询user结果：{}</p>
    """.format(users, psws, mails))


def sele_values(request):
    """可迭代的字典序列"""
    r = ''
    ret = User.objects.all().values('user_name', 'mail')
    for i in ret:
        r += str(i)
    return HttpResponse('<p>查询结果：{}</p>'.format(r))


"""
class JsonResponse(data, encoder=DjangoJSONEncoder, safe=True, json_dumps_params=None, **kwargs)  

　　data: 应该传递一个标准的 python 字典给它，它将其转换成 json 格式的数据。
　　encoder：默认为 django.core.serializers.json.DjangoJSONEncoder，用于序列化data。关于这个序列化的更多信息参见JSON 序列化。
　　safe ： 默认为True。如果设置为False，可以传递任何对象进行序列化（否则，只允许dict 实例）。如果safe 为True，而第一个参数传递的不是dict 对象，将抛出一个TypeError。
另外：它的默认 Content-Type 头部设置为application/json。
　　json_dumps_params：在1.9版本中新增，可以传递一个python标准的 json 库中，json.dump() 方法处理后的对象给它，用于生成一个响应。
"""


def get_json(request):
    """返回json数据"""
    data = {}
    a = User.objects.all()
    # django.core 中的serializers方法可以直接将结果转换为json数据
    data['result'] = json.loads(serializers.serialize('json', a))
    # 返回的结果中存在多余的 model 和 pk 字段
    return JsonResponse(data)


def to_dict(request):
    """将返回的结果转换成dict序列"""
    ret = User.objects.all()
    json_list = []
    for i in ret:
        json_dict = model_to_dict(i)
        json_list.append(json_dict)
    return JsonResponse(json_list, safe=False)


def json_data(request):
    """values()获取的可迭代dict对象转list"""
    data = {}
    ret = User.objects.all().values()
    data["data"] = list(ret)
    return JsonResponse(data, safe=False,
                        # 设置参数 解决中文乱码的问题
                        json_dumps_params={'ensure_ascii': False})
