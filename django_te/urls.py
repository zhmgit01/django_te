"""django_te URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from . import view, testdb
from hello import views
from django.urls import re_path, path

from demo01.views import test_qq, result_qq, user, register, login, reset_pwd, mail, mail_html, file_html_mail

urlpatterns = [
    path("index/", views.index),
    re_path(r"^$", views.index),
    url('^demo/$', views.demo, name='demo_page'),
    url(r'^demo/page=(\d+$)', views.page),
    # 匹配 archive/2018/10.html
    # path('archive/<year>/<month>.html', views.home),
    # 使用正则匹配，显示输入的内容
    # url(r'^archive1/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2}).html$', views.home1),
    url('^home/$', views.home, name='home_page'),
    path('yoyo/', views.yoyo),
    path('page1/', views.page1),
    # 模板继承
    path('sonpage/', views.sonpage),
    # 数据库操作
    url(r'^testdb$', testdb.testdb),

    # ----------操作表中数据-------------
    url(r'^register$', testdb.add_user),
    # 修改数据
    url(r'^update$', testdb.update_psw),
    # 删除数据
    url(r'^delete$', testdb.delete_user),
    # 查询user中的 mail
    url(r'^mail$', testdb.select_mail),
    # 查询user中的所有的值
    url(r'^slc_all$', testdb.select_all),
    # 查询可迭代的字典序列values()
    url(r'^slc_values', testdb.sele_values),
    # 获取json格式数据
    url(r'^get_json$', testdb.get_json),
    # 使用model_to_dict获取json格式数据
    url(r'^to_dict$', testdb.to_dict),
    # 使用values()获取的可迭代对象转为list
    url(r'^json_data$', testdb.json_data),

    # ----------创建admin后台的访问路径-------------
    url(r'^admin/', admin.site.urls),

    # -----get请求-----
    # 访问测试qq页面
    url(r'^qq/', test_qq),
    url(r'^result/', result_qq),

    # 查询数据中的数据
    url(r'^email/', user),

    # ------post请求---
    url(r'user_register/',register),
    url(r'^user_login/', login),
    url(r'^reset/', reset_pwd),

    # 发送邮件
    url(r'send_mail/',mail),
    # 发送html格式邮件
    url(r'mail_html/', mail_html),
    # 发送附件 html格式
    url(r'file_html_mail/', file_html_mail),
]
