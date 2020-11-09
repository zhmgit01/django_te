from django.db import models


# Create your models here.

class Bank(models.Model):
    """银行信息"""
    bank_name = models.CharField(max_length=50, verbose_name='银行名称')
    city = models.CharField(max_length=30, verbose_name='城市')
    point = models.CharField(max_length=60, verbose_name='网点')

    class Meta:
        verbose_name_plural = '银行卡'

    def __str__(self):
        return self.bank_name


class CardInfo(models.Model):
    """卡信息"""
    card_id = models.CharField(max_length=30, verbose_name='卡号')
    card_name = models.CharField(max_length=10, verbose_name='姓名')
    # ForeignKey 必须参数：
    # 1、关联到对应的表
    # 2、on_delete 是指通过ForeignKey连接的对象被删除后，当前字段如何变化
    #   models.CASCADE,对象删除后，包含ForeignKey的字段也会被删除
    #   models.PROTECT,删除时会引起ProtectedError
    #   models.SET_NULL,注意只有当当前字段设置null设置为True才有效，此情况会将ForeignKey字段设置为null
    #   models.SET_DEFAULT ,同样，当前字段设置了default才有效，此情况会将ForeignKey 字段设置为default 值
    #   moels.SET,此时需要指定set的值
    #   models.DO_NOTHING ,什么也不做
    info = models.ForeignKey(Bank, on_delete=models.CASCADE, verbose_name='选择银行')

    class Meta:
        verbose_name_plural = '卡号信息'

    def __str__(self):
        return self.card_id


# =======多对多关系表 回生成book_auth表（记录对应关系）========
class Author(models.Model):
    """作者"""
    name = models.CharField(max_length=10, verbose_name='作者')
    mail = models.CharField(max_length=20, verbose_name='邮箱')
    city = models.CharField(max_length=30, verbose_name='城市')

    class Meta:
        verbose_name_plural = '作者'

    def __str__(self):
        return self.name


class Book(models.Model):
    """书籍详情"""
    book_name = models.CharField(max_length=50, verbose_name='书名')
    auth = models.ManyToManyField(Author, verbose_name='作者')

    class Meta:
        verbose_name_plural = '书籍详情'

    def __str__(self):
        return self.book_name


"""
增加测试数据：
D:\web_djo\helloworld>python manage.py shell

>>> from hello.models import Card, BankName
>>> a = BankName.objects.create(bank_name='上海银行', city='上海', point='徐家汇区')
>>> a.save
>>> c = Card.objects.create(card_id='62270121022100000', card_user='张三', bank_info=a)
>>> c.save

================================================================
正向查询：根据Card表的card_id，去查询关联的对应的BankName相关信息
>>> from hello.models import BankName, Card
>>> cardxx=Card.objects.get(card_id='62270121022100000')
>>> cardxx.card_user
'张三'
>>> cardxx.bank_info
<BankName: 上海银行>
>>> cardxx.bank_info.bank_name
'上海银行'
>>> cardxx.bank_info.city
'上海'
>>>

===============================================================
反向查询_set：
如果想通过银行名称“上海银行”，查询到此银行关联多少张卡，并且查询其中一个银行卡的信息。
反向查询，当ForeignKey没设置related_name参数，默认是通过关联表的名称加_set去查询
查询结果是QuerySet集合对象
count()函数统计查询个数
[0].card_id 下标取值，获取对应属性

>>> bank = BankName.objects.get(bank_name='上海银行')
>>> bank.city
'上海'
# 反向查询，表名称_set
>>> bank.card_set.all()
<QuerySet [<Card: 62270121022100000>]>
# count()函数统计
>>> bank.card_set.all().count()
1
>>> bank.card_set.all()[0].card_id
'62270121022100000'
>>>
"""


class BankName(models.Model):
    """银行信息"""
    bank_name = models.CharField(max_length=50, verbose_name='银行名称', default='')
    city = models.CharField(max_length=30, verbose_name='城市', default='')
    point = models.CharField(max_length=60, verbose_name='网点', default='')

    class Meta:
        verbose_name = '银行'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.bank_name


class CardGrade(models.Model):
    '''会员等级'''
    nub = models.CharField(max_length=50, verbose_name="会员等级", default="")

    class Meta:
        verbose_name = '会员等级'
        verbose_name_plural = verbose_name


# ==========一对一关系============
class Card(models.Model):
    """银行卡，基本信息"""
    card_id = models.CharField(max_length=30, verbose_name='卡号', default='')
    card_user = models.CharField(max_length=10, verbose_name="姓名", default="")
    add_time = models.DateField(auto_now=True, verbose_name="添加时间")
    bank_info = models.ForeignKey(BankName,
                                  related_name='card_bank',  # related_name参数相当于给这个外键取了个别名，方便多个外键时候去识别
                                  on_delete=models.CASCADE,
                                  default='')
    grade = models.ForeignKey(CardGrade,
                              related_name='card_grade',
                              on_delete=models.CASCADE,
                              default='')

    class Meta:
        verbose_name_plural = '银行卡帐户'
        verbose_name = '银行卡帐户_基本信息'

    def __str__(self):
        return self.card_id


class CardDetail(models.Model):
    """银行卡 详细信息"""

    # OneToOneField里面有两个参数必填，
    # 第一个参数传关联的表名称，
    # 第二个参数on_delete=models.CASCADE（对象删除后，包含OneToOneField的字段也会被删除）
    card = models.OneToOneField(Card,
                                on_delete=models.CASCADE,
                                verbose_name='卡号')
    tel = models.CharField(max_length=30, verbose_name='电话', default='')
    mail = models.CharField(max_length=30, verbose_name='邮箱', default='')
    city = models.CharField(max_length=10, verbose_name='城市', default='')
    address = models.CharField(max_length=30, verbose_name='详细地址', default='')

    class Meta:
        verbose_name_plural = '个人资料'
        verbose_name = '帐户_个人资料'

    def __str__(self):
        return self.card.card_id


class Teacher(models.Model):
    """老师表"""
    teacher_name = models.CharField(max_length=30, verbose_name='老师', default='')
    tel = models.CharField(max_length=30, verbose_name='电话', default='')
    mail = models.CharField(max_length=30, verbose_name='邮件', default='')

    class Meta:
        verbose_name = '老师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.teacher_name


# 使用 xadmin
class Student(models.Model):
    '''学生成绩'''
    student_id = models.CharField(max_length=30, verbose_name="学号", default='')
    name = models.CharField(max_length=30, verbose_name="姓名", default='')
    age = models.IntegerField(verbose_name="年龄", default='')
    score = models.IntegerField(verbose_name="分数", default='')
    # 多对多
    teachers = models.ManyToManyField(Teacher, verbose_name='老师')

    gender_choices = (
        (u'M',u'男'),
        (u'F',u'女'),
    )
    gender = models.CharField(max_length=10,
                              choices=gender_choices,
                              verbose_name='性别',
                              default='')

    class Meta:
        verbose_name = "学生"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


"""
=================================================
多对多表的数据新增：

>>> from hello.models import Teacher, Student
>>> t1=Teacher.objects.create(teacher_name='刘老师',tel='155300001111',mail='1000@qq.com')
>>> t1.save()
>>> t1
<Teacher: Teacher object (1)>
>>> t2=Teacher.objects.create(teacher_name='万老师',tel='155300001112',mail='1001@qq.com')
>>> t2.save()
>>> t2
<Teacher: Teacher object (2)>
>>> s1=Student.objects.create(student_id='11002200',name='张三',age=19)
>>> s1.save()

# 方法一：添加id
# 可以添加Teacher对应的id
>>> s1.teachers.add(1)
# 也可以添加多个id，逗号隔开
>>> s1.teachers.add(1,2)
# 如果添加的是传一个可迭代对象(list或tupule),可以用*分开传入这种方法
>>> s1.teachers.add(*[1,2])

# 方法二、直接添加对象
>>> s1.teachers.add(t1)
>>> s1.teachers.add(t2)
>>> s1.teachers.add(t1,t2)

# 也可以先查询需要添加的对象
>>> ob=Teacher.objects.get(teacher_name='刘老师')
>>> ob
<Teacher: Teacher object (1)>
>>> s2=Student.objects.create(student_id='11002201',name='李四',age=19)
>>> s2.teachers.add(ob)

==============================================
正向查询：通过student 表对象查询对应的teacher
>>> from hello.models import Teacher, Student
>>> stu=Student.objects.filter(name='李四').first()
>>> stu
<Student: Student object (2)>
>>> stu.student_id
'11002201'

# 正向查询
>>> stu.teachers.all()
<QuerySet [<Teacher: Teacher object (1)>]>

>>> stu.teachers.all()[0].teacher_name
'刘老师'
>>> stu.teachers.all()[0].tel
'155300001111'

===========================================
反向查询_set:通过老师名称，查询对应关联的学生，反向查询的时候在关联表名称后面加_set
    如果设置 related_name参数使用对应的名称查询
>>> tea=Teacher.objects.filter(teacher_name='刘老师').first()
>>> tea
<Teacher: Teacher object (1)>
>>> tea.tel
'155300001111'

# 反向查询
>>> tea.student_set.all()
<QuerySet [<Student: Student object (1)>, <Student: Student object (2)>]>
>>> tea.student_set.all()[0].name
'张三'
>>>
"""


# xadmin详情页面布局 form_layout
class ArticleClassify(models.Model):
    '''文章分类'''
    n = models.CharField(max_length=30, verbose_name="分类", default="")

    def __str__(self):
        return self.__doc__ + "->" + self.n

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name


class ArticleDetail(models.Model):
    '''文章'''
    title = models.CharField(max_length=30, verbose_name="标题", default="输入你的标题")  # 标题
    classify = models.ForeignKey(ArticleClassify,
                                 on_delete=models.CASCADE,
                                 related_name="classify_name",
                                 verbose_name="文章分类",
                                 )

    body = models.TextField(verbose_name="正文", default="输入正文")  # 正文
    auth = models.CharField(max_length=10, verbose_name="作者", default="admin",
                            blank=True,null=True # 如何想设置非必填字段
                            )  # 作者

    detail = models.TextField(verbose_name="备注", default="添加备注")

    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 最后更新时间
    update_time = models.DateTimeField(auto_now=True, verbose_name="最后更新时间")

    def __str__(self):
        return self.__doc__ + "title->" + self.title

    class Meta:
        verbose_name = "文章列表"
        verbose_name_plural = '文章列表'
