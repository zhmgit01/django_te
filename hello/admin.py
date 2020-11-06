from django.contrib import admin

# Register your models here.

from hello import models
from hello.models import User, Person, Article

# 修改django admin 收益和标题
admin.site.site_header = '项目管理系统'
admin.site.site_title = '登录系统后台'
admin.site.index_title = '后台管理'


# 第二种方式：使用装饰器
@admin.register(User)
class ControlUser(admin.ModelAdmin):
    """自定义列表栏目，添加list_display属性"""
    # 设置显示的字段
    list_display = ('user_name', 'mail', 'psw')
    # 搜索条件 页面显示搜索框
    search_fields = ('user_name', 'psw')


# 添加表信息，使显示在后台管理页面
# User表
# 第一种方式 ：传入参数
# admin.site.register(models.User, ControlUser)

# admin.site.register(models.Person)

@admin.register(Article)
class ControlArticle(admin.ModelAdmin):
    """文章自定义列表栏"""
    # 设置字段
    list_display = ('id', 'title', 'body', 'auth', 'create_time', 'update_time')
    # 搜索条件
    search_fields = ('title',)

    # 按字段排序， - 表示降序
    ordering = ('-create_time',)

    # 分页 每页显示10条
    list_per_page = 10

    # 设置默认可编辑页面，在列表页中就可以编辑
    # 注意：连接字段是不可以添加到 list_editable 中的，否则报错
    list_editable = ('auth',)

    # 设置 link 链接，点击进入编辑页面
    list_display_links = ('title', 'body')

    # 过滤器 快速找到作者对应的文字，现在在列表页面的右边
    list_filter = ('auth', 'title')

    # 按时间分层 设置一个时间字段，可以按时间分层筛选
    date_hierarchy = 'create_time'
