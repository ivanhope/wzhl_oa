# -*- coding: utf-8 -*-
from django.db import models

class user_table(models.Model):
    class Meta:
        permissions = (
            ("can_view", "Can view the page"),
        )
    name = models.CharField(verbose_name='员工名', max_length=30, blank=False, unique=True)
    work_site = models.CharField(verbose_name='员工名', max_length=30, blank=False)
    department = models.CharField(verbose_name='中心', max_length=30, blank=False)
    department_sub = models.CharField(verbose_name='部门', max_length=30, blank=True)
    supervisor = models.CharField(verbose_name='上级主管', max_length=30)
    principal = models.CharField(verbose_name='中心负责人', max_length=30)
    join_date = models.DateField(verbose_name='入职日期', auto_now_add=False)
    graduate_year = models.DateField(verbose_name='毕业日期', auto_now_add=False)
    email = models.CharField(verbose_name='邮箱', max_length=128, blank=False)
    sick_leave_num = models.FloatField(verbose_name='已请病假数', max_length=10)
    statutory_annual_leave_available = models.FloatField(verbose_name='可用法定年假', max_length=10)
    statutory_annual_leave_used = models.FloatField(verbose_name='已用法定年假', max_length=10)
    statutory_annual_leave_total = models.FloatField(verbose_name='总共法定年假', max_length=10)
    company_annual_leave_available = models.FloatField(verbose_name='可用公司年假', max_length=10)
    company_annual_leave_used = models.FloatField(verbose_name='已用公司年假', max_length=10)
    company_annual_leave_total = models.FloatField(verbose_name='总共公司年假', max_length=10)
    seasons_leave_available = models.FloatField(verbose_name='可用季度假', max_length=10)
    seasons_leave_used = models.FloatField(verbose_name='已用季度假', max_length=10)
    seasons_leave_total = models.FloatField(verbose_name='总共季度假', max_length=10)
    leave_in_lieu = models.FloatField(verbose_name='可用调休', max_length=10)
    has_approve = models.PositiveSmallIntegerField(verbose_name='有审批', max_length=10)
    approved_id = models.CharField(verbose_name='经审批的id', max_length=5120, blank=True)
    has_KPI_commit = models.PositiveSmallIntegerField(verbose_name='有KPI审核', max_length=10)
    KPI_commit_id = models.CharField(verbose_name='经KPI审核的id', max_length=5120, blank=True)
    subordinate = models.CharField(verbose_name='下属', max_length=10240, blank=True)
    positive_date = models.DateField(verbose_name='转正日期', auto_now_add=False)
    last_year_leave = models.FloatField(verbose_name='去年假期')
    cc = models.CharField(verbose_name='抄送', max_length=30, blank=True, unique=True)
    birthday_date = models.CharField(verbose_name='生日', max_length=30, blank=True)

class state(models.Model):
    class Meta:
        permissions = (
            ("can_view_all", "Can view all"),
        )
    name = models.CharField(verbose_name='员工名', max_length=30, blank=False)
    type = models.CharField(verbose_name='请假类型', max_length=30, blank=False)
    reason = models.CharField(verbose_name='请假原由', max_length=30, blank=False)
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
