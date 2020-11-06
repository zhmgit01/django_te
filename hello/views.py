from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, Http404


def demo(request):
    return render(request, 'demo.html')


def index(request):
    return HttpResponse('Hello World ! Django~')


def page(request, num):
    try:
        num = int(num)
        return render(request, 'demo.html')
    except:
        raise Http404


# def home(request, year='2020', month='01'):
#     return HttpResponse('获取当前页面home时间标签：{}年{}月'.format(year, month))
#
#
# def home1(request, year='2020', month='01'):
#     return HttpResponse('获取当前页面home时间标签：{}年{}月'.format(year, month))


def home(request):
    return render(request, 'home.html')


def yoyo(request):
    context = {}
    context['name'] = 'yoyo'
    return render(request, 'yoyo.html', context)


def page1(request):
    context = {"name": "zhm"}
    return render(request, 'page1.html', context)


def sonpage(request):
    context = {
        'ads':['selenium', 'appium', 'requests']
    }
    return render(request, 'sonpage.html', context)
