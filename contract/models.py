#coding:utf8
from django.db import models

class table(models.Model):
    class Meta:
        permissions = (
            ("can_view_all", "Can view all"),
            ("can_view_part", "Can view part"),
            ("can_view_shangwu", "Can view shangwu"),
            ("can_view_liujie", "Can view liujie"),
            ("can_view_anchor_contract", "Can view anchor contract"),
        )
    party_a = models.CharField(verbose_name='我方签署公司', max_length=64, blank=False)
    apply_time = models.DateTimeField(verbose_name='申请时间', auto_now_add=True)
    name = models.CharField(verbose_name='申请人', max_length=8, blank=False)
    department = models.CharField(verbose_name='所属中心', max_length=32, blank=False)
    finance_class = models.CharField(verbose_name='财务分类', max_length=6, blank=False)
    contract_class = models.CharField(verbose_name='合同类型', max_length=8, blank=False)
    contract_uuid = models.CharField(verbose_name='合同编号', max_length=24, blank=False)
    origin_contract_uuid = models.CharField(verbose_name='原合同编号', max_length=24, blank=True)
    contract_name = models.CharField(verbose_name='合同名称', max_length=128, blank=False)
    party_b = models.CharField(verbose_name='合作方名称', max_length=64, blank=False)
    address = models.CharField(verbose_name='联系地址', max_length=256, blank=True)
    contacts = models.CharField(verbose_name='联系人', max_length=8, blank=False)
    e_mail = models.CharField(verbose_name='邮箱', max_length=128, blank=True)
    phone_1 = models.CharField(verbose_name='电话1', max_length=16, blank=False)
    phone_2 = models.CharField(verbose_name='电话2', max_length=16, blank=True)
    fax = models.CharField(verbose_name='传真', max_length=16, blank=True)
    bank = models.CharField(verbose_name='开户行', max_length=64, blank=True)
    bank_account = models.CharField(verbose_name='银行账号', max_length=24, blank=True)
    comment = models.CharField(verbose_name='备注', max_length=512, blank=True)
    contract_detail = models.CharField(verbose_name='合同概要', max_length=400, blank=False)
    currency_type = models.CharField(verbose_name='货币类型', max_length=16, blank=False)
    contract_amount_figures = models.FloatField(verbose_name='合同总金额小写', max_length=16, blank=False)
    contract_amount_words = models.CharField(verbose_name='合同总金额大写', max_length=32, blank=False)
    special_requirements = models.CharField(verbose_name='特殊要求', max_length=512, blank=True)
    contract_begin_time = models.DateField(verbose_name='开始时间', blank=False)
    contract_end_time = models.DateField(verbose_name='终止时间', blank=False)
    partner_qualification = models.CharField(verbose_name='合作方资质', max_length=256, blank=True)
    stamp_status = models.IntegerField(verbose_name='盖章情况', blank=False)
    archive_status = models.IntegerField(verbose_name='归档情况', blank=False)
    status = models.IntegerField(verbose_name='状态', max_length=2, blank=False)
    approve_now = models.CharField(verbose_name='当前审批人', max_length=30, blank=True)
    commit_time = models.DateTimeField(verbose_name='提交时间', blank=True)
    process_type = models.CharField(verbose_name='处理类型', max_length=2, blank=False)


class detail(models.Model):
    apply_time = models.DateTimeField(verbose_name='提交时间', auto_now_add=True)
    name = models.CharField(verbose_name='提交人', max_length=8, blank=False)
    operation = models.IntegerField(verbose_name='意见', max_length=2, blank=False)
    archive_path = models.CharField(verbose_name='附件', max_length=128, blank=True)
    comment = models.CharField(verbose_name='审批内容', max_length=512, blank=True)
    parent_id = models.IntegerField(verbose_name='父ID', max_length=8, blank=False)