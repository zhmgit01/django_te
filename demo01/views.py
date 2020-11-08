import os

from django.core.mail import send_mail, send_mass_mail, EmailMessage, EmailMultiAlternatives
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


def mail(request):
    """发送邮件"""
    # 发送一个邮件
    send_mail(subject='Subject here',  # 主题
              message='Here is the message.',  # 正文
              from_email='2964502580@qq.com',  # 发件人
              recipient_list=['xxxx@qq.com'],  # 收件人
              fail_silently=False,
              # auth_user:（可选）SMTP服务器的认证用户名。没提供该参数的情况下，Django会使用EMAIL_HOST_USER 配置项的设置。
              # auth_password:（可选）SMTP服务器的认证密码，没提供该参数的情况下，Django会使用EMAIL_HOST_PASSWORD 配置项的设置。
              # html_message: （可选） send_mail方法独有，可以比较简单地实现一个html文本的传输
              )  # 为False 时，send_mail 会抛出smtplib.SMTPException 异常

    return HttpResponse('邮件发送成功！')


def mass_mail(request):
    """发送多个邮件"""
    message1 = ('Subject 1',
                'Here is the message',
                '2833404xx@qq.com',  # 发件人
                ['xxx@xx.com'])  # 收件人，多个收件人逗号隔开
    message2 = ('Another Subject2',
                'Here is another message',
                '2833404xx@qq.com',
                ['xxx@xx.com'])
    """
    send_mass_mail() 方法的参数说明：
     给定tuple数据类型（subject，message，from_email，recipient_list），发送每封邮件到每个收件人列表。 返回发送的电子邮件数量。

     如果from_email为None，请使用DEFAULT_FROM_EMAIL设置。
     如果设置了auth_user和auth_password，请使用它们登录。
     如果auth_user为None，请使用EMAIL_HOST_USER设置。
     如果auth_password为None，请使用EMAIL_HOST_PASSWORD设置。

     注意：此方法的API已冻结。 想要扩展的新代码功能应该直接使用EmailMessage类。
    """
    send_mass_mail((message1, message2),
                   fail_silently=False)
    return HttpResponse('邮件发送成功！')


def mail_html(request):
    """发送html格式的邮件"""
    h = """
     <!DOCTYPE HTML>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>带图片的邮件</title>
    </head>
    <body>
    <a href="https://yuedu.baidu.com/ebook/902224ab27fff705cc1755270722192e4536582b" target="_blank">
        <p>pytest教程,点图片进入：<br>
        <img src="https://img2018.cnblogs.com/blog/1070438/201902/1070438-20190228112918941-704279799.png" height="160" width="270" />
        </p></a>
    <p>
    其它图片：<br>
    <img src="http://www.w3school.com.cn/i/eg_chinarose.jpg" height=150 width=300/></p>
    <p>请注意，插入动画图像的语法与插入普通图像的语法没有区别。</p>
    </body>
    </html>
    """
    send_mail('Subject here',  # 主题
              'hell',  # 正文
              '2833404xx@qq.com',  # 发件人
              ['xxx@xx.com'],  # 收件人
              fail_silently=False,
              html_message=h)  # html邮件
    return HttpResponse('邮件发送成功！')


def file_mail(request):
    """发送附件"""
    email = EmailMessage(
        subject='hello',
        body='Body goes here',  # 邮件的主体内容文本，须是纯文本信息。
        from_email='xxx@qq.com',  # 发件人
        to=['xxx@qq.com', ],  # 收件人地址列表或元组。
        bcc=['xxx@qq.com'],  # 抄送 列表或元组
        reply_to=['another@example.com'],  # ‘回复’标题中使用的收件人地址列表或元组
        headers={'Message-ID': 'foo'},
    )
    cur = os.path.dirname(os.path.realpath(__file__))
    # templates 目录下的文件
    filepath = os.path.join(cur, 'templates', 'name.html')

    # 方式一：
    # attach_file 调用时，传入某个文件的完整路径，这种方法是最简单的，上传本地的某个文件。
    email.attach_file(filepath, mimetype=None)

    # 方法2 attach
    # attach() 传递三个参数: filename, content 和 mimetype.
    # filename 是出现在邮件中的附件文件的名称，
    # content 是附件的内容，
    # 而 mimetype 是附件所使用的MIME类型。
    file2 = os.path.join(cur, "templates", "b.png")
    img_data = open(file2, "rb")
    email.attach('b.png', img_data.read(), 'image/png')

    email.send()
    return HttpResponse('邮件发送成功！')


def file_html_mail(request):
    """
    使用 EmailMultiAlternatives 类
     发送附件+html正文
     一般推荐用EmailMultiAlternatives类，它继承了EmailMessage
     """
    email = EmailMultiAlternatives(
        'Hello',
        'Body goes here',
        '2833404xx@qq.com',  # 发件人
        ['2833404xx@qq.com', 'to2@example.com'],  # 收件人
        ['xxx@xxx.com'],  # cc抄送
        reply_to=['another@example.com'],  # “回复”标题中使用的收件人地址列表或元组
        headers={'Message-ID': 'foo'},
    )
    cur = os.path.dirname(os.path.realpath(__file__))
    # templates目录下有个a.png的图片
    file1 = os.path.join(cur, "templates", "a.png")

    # 方法1 attach_file
    email.attach_file(file1, mimetype=None)

    # 方法2 attach
    file2 = os.path.join(cur, "templates", "b.png")
    img_data = open(file2, "rb")
    email.attach('b.png', img_data.read(), 'image/png')

    # 添加html正文
    h = '''
    <!DOCTYPE HTML>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>带图片的邮件</title>
    </head>
    <body>
    <a href="https://yuedu.baidu.com/ebook/902224ab27fff705cc1755270722192e4536582b" target="_blank">
        <p>pytest教程,点图片进入：<br>
        <img src="https://img2018.cnblogs.com/blog/1070438/201902/1070438-20190228112918941-704279799.png" height="160" width="270" />
        </p></a>
    <p>
    其它图片：<br>
    <img src="http://www.w3school.com.cn/i/eg_chinarose.jpg" height=150 width=300/></p>
    <p>请注意，插入动画图像的语法与插入普通图像的语法没有区别。</p>
    </body>
    </html>
    '''
    email.attach_alternative(content=h, mimetype="text/html")
    email.send()
    return HttpResponse('邮件发送成功，收不到就去垃圾箱找找吧！')
