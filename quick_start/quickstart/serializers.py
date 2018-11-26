# -*- coding:utf-8 -*-
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
from rest_framework import permissions

"""
HyperlinkedModelSerializer
一种使用超级链接关系代替的“模型序列化程序”
主键关系。明确地：
*包含“URL”字段而不是“ID”字段。
*与其他实例的关系是超链接，而不是主键。
"""


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    class Meta:
        model = User
        # 因为'snippets' 在用户模型中是一个反向关联关系。在使用 ModelSerializer 类时它默认不会被包含，所以我们需要为它添加一个显式字段。
        fields = ('url', 'username', 'email', 'groups', 'snippets')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class SnippetSerializer(serializers.Serializer):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    class Meta:
        model = Snippet
        # source参数控制哪个属性用于填充字段，并且可以指向序列化实例上的任何属性
        # owner = serializers.ReadOnlyField(source='owner.username')
        owner = serializers.CharField(source='owner.username', read_only=True)
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # 购物车！！这些代码片段和创建它们的用户相关联
    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # code = serializers.CharField(style={'base_template': 'textarea.html'})
    # linenos = serializers.BooleanField(required=False)
    # language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    # style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
    #
    # def create(self, validated_data):  # 核心是validate
    #     """
    #     根据提供的验证过的数据创建并返回一个新的`Snippet`实例。
    #     """
    #     return Snippet.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     """
    #     根据提供的验证过的数据更新和返回一个已经存在的`Snippet`实例。
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.code = validated_data.get('code', instance.code)
    #     instance.linenos = validated_data.get('linenos', instance.linenos)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.style = validated_data.get('style', instance.style)
    #     instance.save()
    #     return instance


"""
dd =JSONParser().parse( BytesIO( JSONRenderer().render(serializer.data)))
>> type(serializer.data)
<class 'rest_framework.utils.serializer_helpers.ReturnDict'>
>>> JSONRenderer().render(serializer.data)
b'{"id":2,"title":"","code":"foo = hello world","linenos":false,"language":"python","style":"friendly"}'
>>> rest=JSONRenderer().render(serializer.data)
>>> type(rest)
<class 'bytes'>

"""
