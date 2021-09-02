#coding:utf8
from django.db import models

class table(models.Model):
    class Meta:
        permissions = (
            ("can_view", "Can view the page"),
        )
    FANO = models.CharField(verbose_name='固定资产编号', max_length=30, blank=False, unique=True)
    description = models.CharField(verbose_name='描述', max_length=30, blank=False)
    model = models.CharField(verbose_name='型号', max_length=30, blank=False)
    category = models.CharField(verbose_name='类别', max_length=30, blank=False)
    residual_life = models.IntegerField(verbose_name='剩余月', max_length=10)
    department = models.CharField(verbose_name='部门', max_length=30, blank=True)
    employee = models.CharField(verbose_name='员工', max_length=30, blank=True)
    purchase_date = models.DateField(verbose_name='购买日期')
    payment = models.FloatField(verbose_name='含税价格', max_length=10)
    cost = models.FloatField(verbose_name='价格', max_length=10)
    residual_value = models.FloatField(verbose_name='残值', max_length=10)
    depreciation = models.FloatField(verbose_name='单月折旧价格', max_length=10)
    total_depreciation = models.FloatField(verbose_name='累计折旧价格', max_length=10)
    netbook_value = models.FloatField(verbose_name='剩余价值', max_length=10)
    comment = models.CharField(verbose_name='备注', max_length=128, blank=True)
    serial_number = models.CharField(verbose_name='备注', max_length=20, blank=True)


class table2(models.Model):
    class Meta:
        permissions = (
            ("can_view", "Can view the page"),
        )
    FANO = models.CharField(verbose_name='固定资产编号', max_length=30, blank=False, unique=True)
    description = models.CharField(verbose_name='描述', max_length=30, blank=False)
    model = models.CharField(verbose_name='型号', max_length=30, blank=False)
    category = models.CharField(verbose_name='类别', max_length=30, blank=False)
    residual_life = models.IntegerField(verbose_name='剩余月', max_length=10)
    department = models.CharField(verbose_name='部门', max_length=30, blank=True)
    employee = models.CharField(verbose_name='员工', max_length=30, blank=True)
    purchase_date = models.DateField(verbose_name='购买日期')
    payment = models.FloatField(verbose_name='含税价格', max_length=10)
    cost = models.FloatField(verbose_name='价格', max_length=10)
    residual_value = models.FloatField(verbose_name='残值', max_length=10)
    depreciation = models.FloatField(verbose_name='单月折旧价格', max_length=10)
    total_depreciation = models.FloatField(verbose_name='累计折旧价格', max_length=10)
    netbook_value = models.FloatField(verbose_name='剩余价值', max_length=10)
    comment = models.CharField(verbose_name='备注', max_length=128, blank=True)
    serial_number = models.CharField(verbose_name='备注', max_length=20, blank=True)


class table3(models.Model):
    class Meta:
        permissions = (
            ("can_view", "Can view the page"),
        )
    FANO = models.CharField(verbose_name='固定资产编号', max_length=30, blank=False, unique=True)
    description = models.CharField(verbose_name='描述', max_length=30, blank=False)
    model = models.CharField(verbose_name='型号', max_length=30, blank=False)
    category = models.CharField(verbose_name='类别', max_length=30, blank=False)
    # residual_life = models.IntegerField(verbose_name='剩余月', max_length=10)
    department = models.CharField(verbose_name='部门', max_length=30, blank=True)
    employee = models.CharField(verbose_name='员工', max_length=30, blank=True)
    purchase_date = models.DateField(verbose_name='起租日期')
    payment = models.FloatField(verbose_name='月租金', max_length=10)
    expire_date = models.DateField(verbose_name='到期日期')
    # cost = models.FloatField(verbose_name='价格', max_length=10)
    # residual_value = models.FloatField(verbose_name='残值', max_length=10)
    # depreciation = models.FloatField(verbose_name='单月折旧价格', max_length=10)
    # total_depreciation = models.FloatField(verbose_name='累计折旧价格', max_length=10)
    # netbook_value = models.FloatField(verbose_name='剩余价值', max_length=10)
    comment = models.CharField(verbose_name='备注', max_length=128, blank=True)
    serial_number = models.CharField(verbose_name='备注', max_length=20, blank=True)


class table4(models.Model):
    class Meta:
        permissions = (
            ("can_view", "Can view the page"),
        )
    FANO = models.CharField(verbose_name='固定资产编号', max_length=30, blank=False, unique=True)
    description = models.CharField(verbose_name='描述', max_length=30, blank=False)
    model = models.CharField(verbose_name='型号', max_length=30, blank=False)
    category = models.CharField(verbose_name='类别', max_length=30, blank=False)
    residual_life = models.IntegerField(verbose_name='剩余月', max_length=10)
    department = models.CharField(verbose_name='部门', max_length=30, blank=True)
    employee = models.CharField(verbose_name='员工', max_length=30, blank=True)
    purchase_date = models.DateField(verbose_name='购买日期')
    payment = models.FloatField(verbose_name='含税价格', max_length=10)
    cost = models.FloatField(verbose_name='价格', max_length=10)
    residual_value = models.FloatField(verbose_name='残值', max_length=10)
    depreciation = models.FloatField(verbose_name='单月折旧价格', max_length=10)
    total_depreciation = models.FloatField(verbose_name='累计折旧价格', max_length=10)
    netbook_value = models.FloatField(verbose_name='剩余价值', max_length=10)
    comment = models.CharField(verbose_name='备注', max_length=128, blank=True)
    serial_number = models.CharField(verbose_name='备注', max_length=20, blank=True)


class log(models.Model):
    comment = models.CharField(verbose_name='备注', max_length=256)
    add_time = models.DateTimeField(verbose_name='记录时间', auto_now_add=True)