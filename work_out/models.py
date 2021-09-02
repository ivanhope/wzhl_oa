#coding:utf8
from django.db import models

class table(models.Model):
    class Meta:
        permissions = (
            ("can_view_all", "Can view all"),
        )
    name = models.CharField(verbose_name='员工名', max_length=30, blank=False)
    reason = models.CharField(verbose_name='请假原由', max_length=30, blank=False)
    city = models.CharField(verbose_name='城市', max_length=10, blank=False)
    place = models.CharField(verbose_name='地点', max_length=64, blank=False)
    target = models.CharField(verbose_name='拜访对象', max_length=30, blank=False)
    apply_time = models.DateTimeField(verbose_name='申请时间', auto_now_add=True)
    vacation_date = models.CharField(verbose_name='请假日期', max_length=64, blank=False)
    days = models.FloatField(verbose_name='请假天数', max_length=10, blank=False)
    handover_to = models.CharField(verbose_name='工作交接人', max_length=30, blank=False)
    state_interface = models.CharField(verbose_name='状态显示', max_length=30, blank=False)
    state = models.PositiveSmallIntegerField(verbose_name='状态', max_length=1)
    approve_now = models.CharField(verbose_name='当前审批人', max_length=30, blank=False)
    real_days = models.FloatField(verbose_name='请假天数', max_length=10, blank=False)

class operation_log(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=30, blank=False)
    operation = models.CharField(verbose_name='操作', max_length=256, blank=False)
    operation_time = models.DateTimeField(verbose_name='操作时间', auto_now_add=True)