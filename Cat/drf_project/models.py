# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from datetime import datetime


# Create your models here.


class GoodsCategory(models.Model):
    """
    商品类别
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
        (3, "三级类目"),
    )

    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    # 自连接序列化的 核心思想就是 related_name = "sub_cat"
    #
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
                                        related_name="sub_cat", on_delete=models.CASCADE)
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    name = models.CharField(max_length=20)
    # 生成的是 category_id
    category = models.ForeignKey(GoodsCategory, verbose_name="商品类目", on_delete=models.CASCADE)
    price = models.IntegerField(default=0)

    class Meta:
        db_table = "goods"


from django.contrib.auth.models import AbstractUser


# class UserMMD(AbstractUser):
#     """
#     用户
#     """
#     name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
#     birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
#     gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="female",
#                               verbose_name="性别")
#     mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
#     email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
#
#     class Meta:
#         verbose_name = "用户"
#         # verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.username
