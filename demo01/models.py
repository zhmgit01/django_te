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
