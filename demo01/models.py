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


# 使用 xadmin
class Student(models.Model):
    '''学生成绩'''
    student_id = models.CharField(max_length=30, verbose_name="学号")
    name = models.CharField(max_length=30, verbose_name="姓名")
    age = models.IntegerField(verbose_name="年龄")
    score = models.IntegerField(verbose_name="分数")

    class Meta:
        verbose_name = "学生成绩"
        verbose_name_plural = verbose_name
