#coding:utf8
from django.db import models

class table(models.Model):
    class Meta:
        permissions = (
            ("can_view", "Can view the button"),
            ("can_view_all", "Can view all"),
        )
    KPI_name = models.CharField(verbose_name='绩效考评名称', max_length=30, blank=False)
    name = models.CharField(verbose_name='被考评人名称', max_length=30, blank=False)
    final_score = models.FloatField(verbose_name='最终分数', max_length=10, blank=True)
    status_interface = models.CharField(verbose_name='状态显示', max_length=30, blank=False)
    status = models.PositiveSmallIntegerField(verbose_name='状态', max_length=1)
    self_comment = models.TextField(verbose_name='自我评价', blank=True)
    supervisor_comment = models.TextField(verbose_name='直属主管评价', blank=True)
    principal_comment = models.TextField(verbose_name='中心负责人评价', blank=True)
    commit_now = models.CharField(verbose_name='当前流程人', max_length=30, blank=True)
    KPI_level = models.CharField(verbose_name='KPI等级', max_length=2, blank=True)
    rejected_reason = models.TextField(verbose_name='主管驳回理由', blank=True)

class table_detail(models.Model):
    KPI_name = models.CharField(verbose_name='绩效考评名称', max_length=30, blank=False)
    name = models.CharField(verbose_name='被考评人名称', max_length=30, blank=False)
    objective = models.CharField(verbose_name='绩效目标', max_length=256, blank=False)
    description = models.CharField(verbose_name='描述', max_length=256, blank=False)
    weight = models.IntegerField(verbose_name='权重', max_length=10, blank=False)
    self_report_value = models.FloatField(verbose_name='自评分值', max_length=10, blank=True)
    self_report_score = models.FloatField(verbose_name='自评分数', max_length=10, blank=True)
    supervisor_report_value = models.FloatField(verbose_name='直属主管所评分值', max_length=10, blank=True)
    supervisor_report_score = models.FloatField(verbose_name='直属主管所评分数', max_length=10, blank=True)
    principal_report_value = models.FloatField(verbose_name='中心负责人所评分值', max_length=10, blank=True)
    principal_report_score = models.FloatField(verbose_name='中心负责人所评分数', max_length=10, blank=True)

class ban(models.Model):
    KPI_name = models.CharField(verbose_name='绩效考评名称', max_length=30, blank=False)
    ban_date = models.DateField(verbose_name='封禁日期', blank=False)

