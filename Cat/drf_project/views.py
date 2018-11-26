# -*- coding:utf-8 -*-

from django.shortcuts import render

# Create your views here.

from django.views.generic.base import View

from django.views.generic import ListView

from .models import *  # 引入当前目录运用点号
from django.http import HttpResponse, JsonResponse
import json
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class GoodListViewPre(View):

    def get(self, request):
        """ 通过django的view实现商品列表页 """

        json_list = []
        goods = Goods.objects.all()
        # for x in goods:
        #     model = {}
        #     model['name'] = x.name
        #     model['category'] = x.category
        #     model['price'] = x.price
        #     json_list.append(model)
        from django.forms.models import model_to_dict
        # for x in goods:
        #     json_dict = model_to_dict(x)  # image_field 和 datetime 会报错！！！！！ 不够强大
        #     json_list.append(json_dict)
        from django.core import serializers

        json_dict = serializers.serialize("json", goods)  # serilize后是一个string
        # json_list = json.loads(json_dict)  # 转换

        print(json_dict)
        # return JsonResponse(data={"data": json_list})  # 纯列表不是字典不行！！！！！！！
        # return JsonResponse(data={"data": json.loads(json_dict)})  # 纯列表不是字典不行！！！！！！！ 必须safe=False
        return JsonResponse(json.loads(json_dict), safe=False)  # 纯列表不是字典不行！！！！！！！ 必须safe=False
        # return HttpResponse(json.dumps(json_list), content_type="Application/json")


# 继承django的view 第一层view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import GoodsSerializer, GoodsCategorySerializer
from rest_framework.parsers import JSONParser
from .pagination_drf import Goods_pagination

# MiXIn start
from rest_framework import mixins
from rest_framework import generics


class GoodListViewPre(APIView):  # 一定要继承APIView

    def get(self, request, format=None):
        """
        文档！！！  drf会加上settings.py MEDIA_URL的值！！！
        :param request:123
        :return:321
        """
        goods = Goods.objects.all()
        res_serilizer = GoodsSerializer(goods, many=True)  # list 对象 多个就配many=tuue序列化为数组对象
        print(res_serilizer)
        return Response(res_serilizer.data)

    def post(self, request, format=None):
        """ post 请求 add"""
        data = JSONParser().parse(request)
        serializer = GoodsSerializer(data=request.data)  # 接过来的data  only drf 有request.data
        # serializer = GoodsSerializer(data=data)  # 接过来的data
        if serializer.is_valid():
            serializer.save()  # 调用serializer的create()方法
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoodListViewPre2(mixins.ListModelMixin, generics.GenericAPIView):  # 双继承

    queryset = Goods.objects.all()[:10]
    serializer_class = GoodsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GoodListViewPre3(generics.ListAPIView):
    #  ListAPIView 干了上面的活  # RetrieveAPIView  获取某一个商品的详情，商品详情页
    serializer_class = GoodsSerializer  # 指明要序列化的类
    queryset = Goods.objects.all()  # 指明要查询的集合
    pagination_class = Goods_pagination

    """ 'DEFAULT_PAGINATION_CLASS': None,  REST_FRAMEWORK里面的settings可以看到所有配置 """

    # # 原生理解  generics.ListAPIView  干了get的活
    # def get(self, request, *args, **kwargs):
    #     #  --> mixins.ListModelMixin  干了许多事情， 比如说分页，序列化
    #     return self.list(request, *args, **kwargs)


from rest_framework import viewsets

# 导入filter
from django_filters.rest_framework import DjangoFilterBackend  # dj filter 的filter
from rest_framework.filters import SearchFilter, OrderingFilter  # rest 的filter
from .filters import GoodsFilter


class GoodListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):  # meiyou get post  方法还需要Mixin
    """ 分页搜索过滤，排序，多字段搜索 """
    #  ListAPIView 干了上面的活  # RetrieveAPIView  获取某一个商品的详情，商品详情页
    serializer_class = GoodsSerializer  # 指明要序列化的类
    pagination_class = Goods_pagination

    queryset = Goods.objects.all()  # 指明要查询的集合  和 get_queryset 二取一

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # filter_fields = ('name', 'price', 'id')  # filter_fields 和 filter_classs 二取一
    filter_class = GoodsFilter  # 注意filter_class没有智能提示， 单字段的匹配
    search_fields = ('^name', 'category', '=price')  # 多字段模糊查询
    ordering_fields = ('name', 'category', 'price')
    # 全局settings.py里面不设置的话可以在这里设置
    # viewset 配置认证类
    # authentication_classes = ()
    authentication_classes = (JSONWebTokenAuthentication,)
    """ 没有django-filters只能自己接参数自己手写 """

    # def get_queryset(self):
    #     query = Goods.objects.all()
    #     min_price = self.request.query_params.get("param_price", 0)
    #     qy = query.filter(name__iendswith='pxd')
    #     return qy.filter(price__gt=min_price)
    # def filter_queryset(self):  # 和 queryset 最好不要冲突
    #     # .all()  也是懒惰加载不必担心
    #     query = Goods.objects.all()
    #     min_price = self.request.query_params.get("param_price", 0)
    #     query_set = query.filter(name__iendswith='mmd')
    #     return query_set.filter(price__gt=min_price)

    # query_SET = Goods.objects.all()
    # price_min = self.request.query_params("参数名")
    # return Goods.objects.filter()
    # return query_SET.filter()

    # """ 'DEFAULT_PAGINATION_CLASS': None,  REST_FRAMEWORK里面的settings可以看到所有配置 """

    # # 原生理解  generics.ListAPIView  干了get的活
    # def get(self, request, *args, **kwargs):
    #     #  --> mixins.ListModelMixin  干了许多事情， 比如说分页，序列化
    #     return self.list(request, *args, **kwargs)


class GoodsCategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = GoodsCategorySerializer
    queryset = GoodsCategory.objects.filter(category_type=1)


"""
# class GenericViewSet(ViewSetMixin, generics.GenericAPIView):
#     
#     The GenericViewSet class does not provide any actions by default,
#     but does include the base set of generic view behavior, such as
#     the `get_object` and `get_queryset` methods.
#     
#     pass
# Set the `.action` attribute on the view, depending on the request method.  动态设置序列化用到动作
"""

from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets

User = get_user_model()


# 权限认证自定义类  自己想定义用户验证
#  ModelBackend是默认的认证后台，并且大多数情况下会对auth_permission表进行查询
class CustomBackend(ModelBackend):
    """ 重写认证 """

    def authenticate(self, username=None, password=None, **kwargs):
        """ 不管怎样, authenticate 至少应该检查凭证, 如果凭证合法，它应该返回一个匹配于登录信息的 User 实例。如果不合法，则返回 None. """
        # def authenticate(self, token, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

    def has_perm(self, user_obj, perm, obj=None):
        return True


from random import choice


class SmsViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
       发送短信验证码
    """

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 400 错误码
        mobile = serializer.validated_data["mobile"]  # 验证过的mobile
        self.perform_create(serializer)
        # yun_pian = YunPian(APIKEY)
        #
        # code = self.generate_code()
        #
        # sms_status = yun_pian.send_sms(code=code, mobile=mobile)
        #
        # if sms_status["code"] != 0:
        #     return Response({
        #         "mobile": sms_status["msg"]
        #     }, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     code_record = VerifyCode(code=code, mobile=mobile)
        #     code_record.save()
        #     return Response({
        #         "mobile": mobile
        #     }, status=status.HTTP_201_CREATED)
