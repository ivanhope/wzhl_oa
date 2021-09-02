#coding:utf8
from django.db import models

class table(models.Model):
    class Meta:
        permissions = (
            ("can_view_all", "Can view all"),
        )
    name = models.CharField(verbose_name='姓名', max_length=8, blank=False)
    date = models.CharField(verbose_name='日期', max_length=64, blank=False)
    apply_time = models.DateTimeField(verbose_name='申请时间', auto_now_add=True)
    travel_partner = models.CharField(verbose_name='同行人', max_length=64, blank=False)
    hotel_reservation = models.IntegerField(verbose_name='订酒店', max_length=2, blank=False)
    budget_sum = models.FloatField(verbose_name='总预算', max_length=10, blank=True)
    status = models.IntegerField(verbose_name='状态', max_length=2, blank=False)
    approve_now = models.CharField(verbose_name='当前审批人', max_length=30, blank=True)
    commit_time = models.DateTimeField(verbose_name='提交时间', blank=True)


class budget(models.Model):
    budget_type = models.CharField(verbose_name='预算类型', max_length=10, blank=False)
    budget = models.FloatField(verbose_name='预算费用', max_length=10, blank=True)
    parent_id = models.IntegerField(verbose_name='父id', max_length=8, blank=False)


class budget_sub(models.Model):
    airfare = models.FloatField(verbose_name='实际机票费用', max_length=10, blank=False)
    accommodation_cost = models.FloatField(verbose_name='实际住宿费用', max_length=10, blank=True)
    payment = models.CharField(verbose_name='住宿费用支付方式', max_length=10, blank=True)
    parent_id = models.IntegerField(verbose_name='父id', max_length=8, blank=False, unique=True)


class detail(models.Model):
    reason = models.CharField(verbose_name='事由', max_length=256, blank=True)
    origin = models.CharField(verbose_name='起点', max_length=20, blank=False)
    destination = models.CharField(verbose_name='终点', max_length=20, blank=False)
    date = models.CharField(verbose_name='日期', max_length=64, blank=False)
    vehicle = models.CharField(verbose_name='交通工具', max_length=8, blank=False)
    parent_id = models.IntegerField(verbose_name='父id', max_length=8, blank=False)