"""
Django settings for django_te project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ===========xadmin 安装时添加=============
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
sys.path.insert(0,os.path.join(BASE_DIR,'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ti-)v-+hy*hsql+fck3w$y*54z=(gun)n_8j&19=j6%b2a#24v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',  # 管理站点
    'django.contrib.auth',  # 认证系统
    'django.contrib.contenttypes',  # 用于内容类型的框架
    'django.contrib.sessions',  # 会话框架，默认启用 session应用
    'django.contrib.messages',  # 消息框架
    'django.contrib.staticfiles',  # 管理静态文件框架
    # -----------注册app-------------
    'hello',  # 应用app
    'demo01',
    'demo02',
    # ===========xadmin 安装时添加=========
    'xadmin',
    'crispy_forms'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # 默认启用session中间层
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_te.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + "/hello/templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_te.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',  # 数据库名
        'USER': 'root',  # 用户名
        'PASSWORD': 'root',  # 密码
        'HOST': 'localhost',  # 数据库地址
        'PORT': '3306'  # mysql数据库端口
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-Hans'  # 设置简体中文 zh-Hant是繁体中文

# TIME_ZONE = 'UTC'   # 时区
TIME_ZONE = 'Asia/Shanghai'  # 设置为中国的时区

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False  # 设置为False，要不然数据库时间和当前时间不一致

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

"""
发送邮件的配置信息

EMAIL_USE_SSL 和 EMAIL_USE_TLS 是互斥的，只能有一个为 True
"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True        # SSL加密方式
EMAIL_HOST = 'smtp.qq.com'   # 发送邮件的邮箱 的 SMTP服务器，这里用了163邮箱
EMAIL_PORT = 465    # SMTP服务器端口
EMAIL_HOST_USER = '283340479@qq.com'   # 发件人
EMAIL_HOST_PASSWORD = '授权码'   # 密码(这里使用的是授权码)
EMAIL_FROM = 'yoyo<283340479@qq.com>'   # 邮件显示的发件人