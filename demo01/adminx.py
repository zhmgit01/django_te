import xadmin
from .models import Student, Card, CardDetail


class ControlStudent(object):
    # 显示的字段
    list_display = ('student_id', 'name', 'age', 'score')
    # 搜索条件
    search_fields = ('name',)

    # 每页显示10条
    list_per_page = 10


class MoreInfo(object):
    model = CardDetail


class ControlCard(object):
    list_display = ["card_id", "card_user", "add_time"]

    # 在Card页面显示更多信息CardDetail
    inlines = [MoreInfo]


# 注册Student表
xadmin.site.register(Student, ControlStudent)

# 注册card表，关联CardDetail
xadmin.site.register(Card, ControlCard)
