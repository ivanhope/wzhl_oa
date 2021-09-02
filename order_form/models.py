# -*- coding: utf-8 -*-
from django.db import models

class user(models.Model):
    class Meta:
        permissions = (
            ("can_upload_menu", "Can upload menu"),
        )
    name = models.CharField(verbose_name='员工名', max_length=30, blank=False)
    department = models.CharField(verbose_name='部门', max_length=30, blank=False)
    comment = models.CharField(verbose_name='备注', max_length=256)

class order(models.Model):
    name = models.CharField(verbose_name='被订餐者', max_length=30, blank=False)
    type = models.CharField(verbose_name='订餐类型', max_length=30)
    add_time = models.DateTimeField(verbose_name='订餐时间', auto_now_add=True)
    order_name = models.CharField(verbose_name='订餐者姓名', max_length=30)
    comment = models.CharField(verbose_name='备注', max_length=256)
    star = models.FloatField(verbose_name='星数', max_length=10)