#coding:utf8
from django.db import models

class budget(models.Model):
    class Meta:
        permissions = (
            ("can_view", "Can view the page"),
        )
    date = models.CharField(verbose_name='日期', max_length=8, blank=False)
    department = models.CharField(verbose_name='所属中心', max_length=32, blank=False)
    budget_class = models.CharField(verbose_name='预算类型', max_length=64, blank=False)
    budget_summary = models.FloatField(verbose_name='总预算', max_length=12, blank=False)
    budget_used = models.FloatField(verbose_name='已用预算', max_length=12, blank=False)
    budget_available = models.FloatField(verbose_name='剩余预算', max_length=12, blank=False)
    budget_added = models.FloatField(verbose_name='附加预算', max_length=12, blank=False)



class log(models.Model):
    apply_time = models.DateTimeField(verbose_name='提交时间', auto_now_add=True)
    name = models.CharField(verbose_name='提交人', max_length=8, blank=False)
    comment = models.CharField(verbose_name='内容', max_length=512, blank=True)



class repay(models.Model):
    name = models.CharField(verbose_name='申请人', max_length=8, blank=False)
    apply_time = models.DateTimeField(verbose_name='申请时间', auto_now_add=True)
    budget_class = models.CharField(verbose_name='预算类型', max_length=64, blank=False)
    budget_class_level2 = models.CharField(verbose_name='预算类型', max_length=64, blank=True)
    department = models.CharField(verbose_name='所属中心', max_length=32, blank=False)
    description = models.CharField(verbose_name='描述', max_length=256, blank=False)
    amount = models.FloatField(verbose_name='金额', max_length=12, blank=False)
    amount_words = models.CharField(verbose_name='大写金额', max_length=64, blank=False)
    payment_class = models.CharField(verbose_name='付款方式', max_length=16, blank=False)
    beneficiary_name = models.CharField(verbose_name='收款人', max_length=32, blank=False)
    beneficiary_account = models.CharField(verbose_name='收款人账户', max_length=64, blank=False)
    beneficiary_bank = models.CharField(verbose_name='收款人银行', max_length=64, blank=False)
    contract_uuid = models.CharField(verbose_name='合同编号', max_length=16, blank=True)
    payment_date = models.DateField(verbose_name='应付日期', auto_now_add=False, blank=False)
    payment_type = models.CharField(verbose_name='付款类型', max_length=16, blank=False)
    invoice_type = models.CharField(verbose_name='发票类型', max_length=16, blank=False)
    comment = models.CharField(verbose_name='备注', max_length=256, blank=True)
    status = models.PositiveSmallIntegerField(verbose_name='状态', max_length=1)
    approve_now = models.CharField(verbose_name='当前审批人', max_length=30, blank=False)



class detail(models.Model):
    apply_time = models.DateTimeField(verbose_name='提交时间', auto_now_add=True)
    name = models.CharField(verbose_name='提交人', max_length=8, blank=False)
    operation = models.IntegerField(verbose_name='意见', max_length=2, blank=False)
    comment = models.CharField(verbose_name='审批内容', max_length=512, blank=True)
    parent_id = models.IntegerField(verbose_name='父ID', max_length=8, blank=False)
