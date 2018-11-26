# -*- coding:utf-8 -*-

from rest_framework import serializers
from .models import Goods, GoodsCategory


# class GoodsSerializer(serializers.Serializer):
#     """ 要序列化的字段自己申明号 """
#     name = serializers.CharField(required=True, max_length=20)
#     category = serializers.CharField(required=True, max_length=20)
#     price = serializers.IntegerField(default=0)
#
#     def create(self, validated_data):  # validated_data就是上面的字段
#         """ 前端穿过来校验 """
#         return Goods.objects.create(**validated_data)


class GoodsSerializer(serializers.ModelSerializer):
    """ 要序列化的字段自己申明号 """

    # name = serializers.CharField(required=True, max_length=20)
    # category = serializers.CharField(required=True, max_length=20)
    # price = serializers.IntegerField(default=0)
    #
    # def create(self, validated_data):  # validated_data就是上面的字段
    #     """ 前端穿过来校验 """
    #     return Goods.objects.create(**validated_data)

    """ category = CategorySerializer() --->  替换覆盖category字段"""

    class Meta:
        model = Goods
        fields = ("name", "category", "price")
        # fields = "__all__"  # 默认取所有字段 外键会自动序列化程id 并且带MEDIA_URL

        # 外键的话要需要外键的信息的话 嵌套GoodsSerializer


class GoodsCategorySubSerializer2(serializers.ModelSerializer):
    """ 第三层 """

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsCategorySubSerializer1(serializers.ModelSerializer):
    """  第二层 """
    sub_cat = GoodsCategorySubSerializer2(many=True)  # 一定要实例化  一对多一定是many = True

    class Meta:
        model = GoodsCategory
        fields = "__all__"
        # sub_cat = GoodsCategorySubSerializer2


class GoodsCategorySerializer(serializers.ModelSerializer):
    sub_cat = GoodsCategorySubSerializer1(many=True)  # 一定要实例化  一对多一定是many = True

    class Meta:
        model = GoodsCategory
        fields = "__all__"
        # 这里没有sub_cat哦


from django.contrib.auth import get_user_model

User = get_user_model()
import re
from datetime import datetime, timedelta


class SmsSerializer(serializers.Serializer):  # 如果需要关联表的话才是 --> ModelSerializer
    """ serializers.ModelSerializer ？ 和表暂时没关系 """
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """ 验证手机号码 """

        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")
        if not re.match(r"\d{11}", mobile):
            raise serializers.ValidationError("非法号码")
        # 验证码频率验证
        one_minute_ago = datetime.now() - timedelta(seconds=60)
        if User.objects.filter(add_time__gt=one_minute_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60秒")
        return mobile

class UserSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, max_length=5, min_length=4)

    def validated_code(self,code):
        pass
        # varify_records = VerifyCode.objects.filter(mobile=self.initial_data)  """ self.initial_data """
        # order_by("-add_time")

    """ self.initial_data  """
