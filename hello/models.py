from django.db import models

# Create your models here.
"""
字段类型

1、models.AutoField　　自增列= int(11)
　　如果没有的话，默认会生成一个名称为 id 的列，如果要显示的自定义一个自增列，必须将给列设置为主键 primary_key=True。
2、models.CharField　　字符串字段
　　必须 max_length 参数
3、models.BooleanField　　布尔类型=tinyint(1)
　　不能为空，Blank=True
4、models.ComaSeparatedIntegerField　　用逗号分割的数字=varchar
　　继承CharField，所以必须 max_lenght 参数
5、models.DateField　　日期类型 date
　　对于参数，auto_now =True则每次更新都会更新这个时间；auto_now_add 则只是第一次创建添加，之后的更新不再改变。
6、models.DateTimeField　　日期类型 datetime
　　同DateField的参数
7、models.Decimal　　十进制小数类型= decimal
　　必须指定整数位max_digits和小数位decimal_places
8、models.EmailField　　字符串类型（正则表达式邮箱）=varchar
　　对字符串进行正则表达式
9、models.FloatField　　浮点类型= double
10、models.IntegerField　　整形
11、models.BigIntegerField　　长整形
　　integer_field_ranges ={
　　　　‘SmallIntegerField’:(-32768,32767),
　　　　‘IntegerField’:(-2147483648,2147483647),
　　　　‘BigIntegerField’:(-9223372036854775808,9223372036854775807),
　　　　‘PositiveSmallIntegerField’:(0,32767),
　　　　‘PositiveIntegerField’:(0,2147483647),
　　}
12、models.IPAddressField　　字符串类型（ip4正则表达式）
13、models.GenericIPAddressField　　字符串类型（ip4和ip6是可选的）
　　参数protocol可以是：both、ipv4、ipv6
　　验证时，会根据设置报错
14、models.NullBooleanField　　允许为空的布尔类型
15、models.PositiveIntegerFiel　　正Integer
16、models.PositiveSmallIntegerField　　正smallInteger
17、models.SlugField　　减号、下划线、字母、数字
18、models.SmallIntegerField　　数字
　　数据库中的字段有：tinyint、smallint、int、bigint
19、models.TextField　　字符串=longtext
20、models.TimeField　　时间 HH:MM[:ss[.uuuuuu]]
21、models.URLField　　字符串，地址正则表达式
22、models.BinaryField　　二进制
23、models.ImageField图片
24、models.FilePathField文件
"""

"""
字段参数

1、null=True
　　数据库中字段是否可以为空
2、blank=True
　　django的 Admin 中添加数据时是否可允许空值
3、primary_key = False
　　主键，对AutoField设置主键后，就会代替原来的自增 id 列
4、auto_now 和 auto_now_add
　　auto_now 自动创建—-无论添加或修改，都是当前操作的时间
　　auto_now_add 自动创建—-永远是创建时的时间
5、choices
GENDER_CHOICE = (
(u’M’, u’Male’),
(u’F’, u’Female’),
)
gender = models.CharField(max_length=2,choices = GENDER_CHOICE)
6、max_length
7、default　　默认值
8、verbose_name　　Admin中字段的显示名称
9、name|db_column　　数据库中的字段名称
10、unique=True　　不允许重复
11、db_index = True　　数据库索引
12、editable=True　　在Admin里是否可编辑
13、error_messages=None　　错误提示
14、auto_created=False　　自动创建
15、help_text　　在Admin中提示帮助信息
16、validators=[]
17、upload-to
"""

"""
django操作数据库
python manage.py makemigrations
python manage.py migrate
"""


class Test(models.Model):
    """类名表示数据库表名"""
    # 类里面的字段代标数据表中字段(name)
    # 数据类型则由 CharField(相当于varchar)
    # DateField相当于 datatime
    # max_lenth参数限定长度
    name = models.CharField(max_length=20)


class Person(models.Model):
    """用户信息"""
    # 未设置主键 通过django新增表后 person表中自动主键字段：id
    name = models.CharField(max_length=30)
    age = models.IntegerField()

    def __str__(self):
        return self.__doc__ + ":name>" + self.name


class User(models.Model):
    """注册表"""
    # 将 user_name 设置为主键，表新增成功之后 会默认替代 id 的主键
    user_name = models.CharField(max_length=30, primary_key=True)
    psw = models.CharField(max_length=30)
    mail = models.CharField(max_length=30)

    # 优化显示，显示具体的表名称
    def __str__(self):
        return self.__doc__ + ":user_name>" + self.user_name


class Article(models.Model):
    """文章"""
    # verbose_name 设置数据表字段在admin页面显示的中文名称
    title = models.CharField(max_length=30, verbose_name='标题')  # 标题
    # 当文本内容很多时，使用 TextField
    body = models.TextField(verbose_name='正文')  # 正文
    auth = models.CharField(max_length=10, verbose_name='作者')  # 作者

    # 创建时间
    # auto_now_add 默认为false，设置为True时，会在model对象第一次被创建时，iang字段的值设置为创建时的时间
    # 之后进行修改对象时，字段的支部会更新
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='新增时间')

    # 最后更新时间
    # auto_now 默认为false，设置为true时，能够在保存该字段时，将其值设置为当前时间，并且每次修改该model时，都会更新
    # 当设置为true时，并不是简单地将字段地默认值置为当前时间，而是指字段被"强制"更新到当前时间，无法在程序中手动为字段赋值
    # 如果使用django自带的admin管理器，那么该字段在admin中是只读的
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    # auto_now、auto_now_add设置为True后会导致字段属性editable=False和blank=True的状态。
    # editable=False将导致字段不会被呈现在admin中
    # blank=True表示允许在表单中不输入值

    def __str__(self):
        return self.__doc__ + 'title->' + self.title

    # 表名称Articles这地方也可以改成中文显示，在class Meta中加verbose_name_plural属性
    # class Meta 嵌套入class Article中
    class Meta:
        verbose_name_plural = '文章列表'
