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
