import xadmin
from .models import Student, Card, CardDetail, Teacher, ArticleDetail


class ControlStudent(object):
    # 显示的字段
    list_display = ('student_id', 'name', 'age', 'score', 'teacher')
    # 搜索条件
    search_fields = ('name',)

    # 每页显示10条
    list_per_page = 10

    def teacher(self, obj):
        return [x.teacher_name for x in obj.teachers.all()]


class MoreInfo(object):
    model = CardDetail


class ControlCard(object):
    # 定义关联函数查询关联字段，显示在列表中
    list_display = ["card_id", "card_user", 'telphone', 'city', "add_time"]

    # 在Card页面显示更多信息CardDetail
    inlines = [MoreInfo]

    # 查询关联表的tel字段
    def telphone(self, obj):
        return obj.carddetail.tel

    def city(self, obj):
        return obj.carddetail.city


class ControlTeacher(object):
    list_display = ['teacher_name', 'tel', 'mail']


class ControlActicl(object):
    list_display = ['title', 'body', 'auth']


# 注册Student表
xadmin.site.register(Student, ControlStudent)

# 注册card表，关联CardDetail
xadmin.site.register(Card, ControlCard)

xadmin.site.register(Teacher, ControlTeacher)

from xadmin.layout import Main, TabHolder, Fieldset, Row, Col, AppendedText, Side, Field, Tab


class MoreActicl(object):
    list_display = ['title', 'body', 'auth']

    readonly_fields = ['detail']  # 只读字段

    exclude = ['auth']  # 不显示某个字段

    form_layout = (
        Fieldset(u'',
                 Row('title', 'auth'),  # Row表示将里面的字段作为一行显示
                 Row('classify'),
                 css_class='unsort'  # 不让区块拖动
                 ),
        Fieldset(('正文内容'),  # Fieldset第一个参数表示区块名称
                 'body',
                 ),
        Fieldset(('备注'),
                 Row('detail'),
                 css_class='unsort no_title'  # no_title是不显示区块的title名称
                 ),
        TabHolder(
            Tab('body-raw',
                Field('title', css_class="extra"),  # css_class="extra"可以将输入框占一整行
                Field('body'),
                css_class='unsort'
                ),
            Tab('body-json',
                Field('body', )
                ),
            css_class='unsort',
        )
    )


xadmin.site.register(ArticleDetail, MoreActicl)
