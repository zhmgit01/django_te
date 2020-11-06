# -*- coding:utf-8 -*-
# @FileName  :view.py
# @Time      :2020/11/5 11:23
# @Author    :zhm

from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello World ! Django~')


def diy(request):
    return HttpResponse('zhm')
