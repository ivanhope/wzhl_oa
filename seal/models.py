#coding:utf8
from django.db import models

class table(models.Model):
    class Meta:
        permissions = (
            ("can_view_all", "Can view all"),
            ("can_view_part", "Can view part"),
        )
    name = models.CharField(verbose_name='申请人', max_length=8, blank=False)
    uuid = models.CharField(verbose_name='编号', max_length=24, blank=False)
    department = models.CharField(verbose_name='所属中心', max_length=32, blank=False)
    seal_from = models.CharField(verbose_name='印章/证照归属', max_length=64, blank=False)
    seal_class = models.CharField(verbose_name='印章/证照类型', max_length=64, blank=False)
    usage = models.CharField(verbose_name='使用方式', max_length=16, blank=False)
    reason = models.CharField(verbose_name='事由', max_length=128, blank=False)
    archive_path = models.CharField(verbose_name='附件', max_length=128, blank=True)
    borrow_begin_time = models.DateField(verbose_name='外借开始时间', blank=False)
    borrow_end_time = models.DateField(verbose_name='外借终止时间', blank=False)
    comment = models.CharField(verbose_name='备注', max_length=512, blank=True)
    status = models.IntegerField(verbose_name='状态', max_length=2, blank=False)
    approve_now = models.CharField(verbose_name='当前审批人', max_length=30, blank=True)


class detail(models.Model):
    apply_time = models.DateTimeField(verbose_name='提交时间', auto_now_add=True)
    name = models.CharField(verbose_name='提交人', max_length=8, blank=False)
    operation = models.IntegerField(verbose_name='意见', max_length=2, blank=False)
    # archive_path = models.CharField(verbose_name='附件', max_length=128, blank=True)
    comment = models.CharField(verbose_name='审批内容', max_length=512, blank=True)
    parent_id = models.IntegerField(verbose_name='父ID', max_length=8, blank=False)