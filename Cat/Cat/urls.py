# -*- coding:utf-8 -*-
"""Cat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
# from drf_project.views import GoodListView
from django.conf.urls import include, url

# 文档生成需要的命名空间
from rest_framework.documentation import include_docs_urls

from drf_project.views import *

# viewset 配置方法 基础版本不带 Route！！！！
good_list = GoodListViewSet.as_view({
    'get': 'list',  # get 请求绑定到list
    # 'post': 'create'  # post 请求绑定create
})

# Routers 引入
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#   ------------> r'^goodsroute/
router.register(r'goodsrt', GoodListViewSet, base_name='goods')  # 自动默认 get -> list  create -> post
router.register(r'goodscategory', GoodsCategoryViewSet, base_name='category')

urlpatterns = [
    # url('', include(router.urls)),
    url(r'^', include(router.urls), name='base'),  # inlude router 注册的路由

    url(r'^admin/', admin.site.urls),
    url(r'^goods2/', GoodListViewPre2.as_view(), name='goods_list'),

    url(r'^goods/', GoodListViewPre.as_view(), name='goods_list'),
    # viewset  单纯版
    url(r'^goodsvs/', good_list, name='goods_list'),

    url(r'^docs/', include_docs_urls(title='ttt')),  # 不可加$
    url(r'^api-auth/', include('rest_framework.urls'))

]
# class base view 入手  Tutorial 3: Class-based Views
from rest_framework.authtoken import views
urlpatterns += [
    url(r'^api-token-auth/', views.obtain_auth_token)
]

# jwt 认证模式  需要加的urls
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns += [
    # url(r'^api-token-auth-mmd/', obtain_jwt_token),
    url(r'^login/', obtain_jwt_token),   # 看jwt原理
]
"""
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImNhdCIsImV4cCI6MTU0MzA3OTMxMiwiZW1haWwiOiI0NTMzODg5MzdAcXEuY29tIn0.GtyvqZkM4g_Y5M9SL4CVeX3ISJ7wVHNSm3ua0VCODRs"
}
"""