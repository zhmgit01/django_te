from django.contrib import admin

# Register your models here.

from demo01 import models


# =============一对多关系===============
@admin.register(models.Bank)
class ControlBank(admin.ModelAdmin):
    # 显示的字段
    list_display = ['bank_name', 'city', 'point']


@admin.register(models.CardInfo)
class ControlCardInfo(admin.ModelAdmin):
    # 显示的字段
    list_display = ['card_id', 'card_name', 'info']


@admin.register(models.Author)
class ControlAuthor(admin.ModelAdmin):
    # 显示字段
    list_display = ['name', 'city', 'mail']


@admin.register(models.Book)
class ControlBook(admin.ModelAdmin):
    # 显示字段
    list_display = ['book_name', 'auth']

    def auth(self, obj):
        # 定义一个方法，遍历book的auth 然后用列表返回
        return [a.name for a in obj.auth.all()]
