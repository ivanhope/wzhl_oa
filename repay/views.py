# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.db.models.query_utils import Q
from repay.models import budget, log, repay, detail
from vacation.models import user_table
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from libs.common import int_format
import json, re
from django.db import transaction
import datetime
from libs.common import Num2MoneyFormat
from libs.sendmail import send_mail
from threading import Thread



@login_required
def budget_table(request):
    path = request.path.split('/')[1]
    if not request.user.has_perm('repay.can_view'):
        return render(request,'public/no_passing.html')
    return render(request, 'repay/budget_table.html',{'user':'%s%s' % (request.user.last_name,request.user.first_name),
                                                       'path1':'repay',
                                                       'path2':path,
                                                       'page_name1':u'报销管理',
                                                       'page_name2':u'预算表'},context_instance=RequestContext(request))



@login_required
def budget_table_data(request):
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    aaData = []
    sort = ['date','department','budget_class','budget_summary','budget_used','budget_available','budget_added']

    if  sSortDir_0 == 'asc':
        if sSearch == '':
            result_data = budget.objects.all().order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = budget.objects.all().count()
        else:
            result_data = budget.objects.filter(Q(date__contains=sSearch) | \
                                                    Q(department__contains=sSearch) | \
                                                    Q(budget_class__contains=sSearch)) \
                                                    .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = budget.objects.filter(Q(date__contains=sSearch) | \
                                                    Q(department__contains=sSearch) | \
                                                    Q(budget_class__contains=sSearch)).count()
    else:
        if sSearch == '':
            result_data = budget.objects.all().order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = budget.objects.all().count()
        else:
            result_data = budget.objects.filter(Q(date__contains=sSearch) | \
                                                    Q(department__contains=sSearch) | \
                                                    Q(budget_class__contains=sSearch)) \
                                                    .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = budget.objects.filter(Q(date__contains=sSearch) | \
                                                    Q(department__contains=sSearch) | \
                                                    Q(budget_class__contains=sSearch)).count()

    for i in  result_data:
        i_dict = {}
        i_dict['budget_summary'] = int_format(float('%.2f' % i.budget_summary))
        i_dict['budget_used'] = int_format(float('%.2f' % i.budget_used))
        i_dict['budget_available'] = int_format(float('%.2f' % i.budget_available))
        i_dict['budget_added'] = int_format(float('%.2f' % i.budget_added))
        for j in i_dict.keys():
            i_dict[j] = re.sub(r'\.(?P<d>\d)$','.\g<d>0',i_dict[j])


        aaData.append({
                       '0':str(i.date),
                       '1':i.department,
                       '2':i.budget_class,
                       '3':i_dict['budget_summary'],
                       '4':i_dict['budget_used'],
                       '5':i_dict['budget_available'],
                       '6':i_dict['budget_added'],
                       '7':i.id
                      })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(json.dumps(result),content_type="application/json")




@login_required
@transaction.commit_on_success()
def budget_table_save(request):
    date = request.POST.get('date')
    department = request.POST.get('department')
    budget_class = request.POST.get('budget_class')
    budget_summary = request.POST.get('budget_summary')
    budget_added = request.POST.get('budget_added')
    _id = request.POST.get('id')
    print budget_added

    try:
        if not _id:
            orm = budget(date=date,department=department,budget_class=budget_class,budget_summary=float(budget_summary),\
                         budget_used=0.0,budget_available=float(budget_summary),budget_added=0.0)
            orm.save()

            comment = '给 <b>{0}</b> 设置了 <b>{1}</b> 额度的 <b>{2}</b>'.format(department, budget_summary, budget_class)
            orm_log = log(name=request.user.first_name,comment=comment)
            orm_log.save()

        else:
            orm = budget.objects.get(id=_id)
            orm.budget_added = orm.budget_added + float(budget_added)
            orm.budget_summary = float(budget_added) + orm.budget_summary
            orm.budget_available = orm.budget_summary - orm.budget_used
            orm.save()

            comment = '给 <b>{0}</b> 追加了 <b>{1}</b> 额度的 <b>{2}</b>'.format(orm.department, budget_added, orm.budget_class)
            orm_log = log(name=request.user.first_name,comment=comment)
            orm_log.save()

        return HttpResponse(json.dumps({'code':0,'msg':u'保存成功'}),content_type="application/json")
    except Exception,e:
        print e
        return HttpResponse(json.dumps({'code':1,'msg':str(e)}),content_type="application/json")



@login_required
def budget_table_del(request):
    _id = request.POST.get('id')
    orm = budget.objects.get(id=_id)
    if orm.budget_used != 0:
        return HttpResponse(json.dumps({'code':1,'msg':u'该项预算已被使用，无法删除'}),content_type="application/json")
    try:
        orm.delete()
        return HttpResponse(json.dumps({'code':0,'msg':u'删除成功'}),content_type="application/json")
    except Exception,e:
        print e
        return HttpResponse(json.dumps({'code':1,'msg':str(e)}),content_type="application/json")



@login_required
def repay_log(request):
    path = request.path.split('/')[1]
    if not request.user.has_perm('repay.can_view'):
        return render(request,'public/no_passing.html')
    return render(request,'repay/repay_log.html',{'user':request.user.username,
                                                   'path1':'repay',
                                                   'path2':path,
                                                   'page_name1':u'报销管理',
                                                   'page_name2':u'操作日志'},context_instance=RequestContext(request))



@login_required
def repay_log_data(request):
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    aaData = []
    sort = ['name','comment','apply_time','id']

    if  sSortDir_0 == 'asc':
        if sSearch == '':
            result_data = log.objects.all().order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = log.objects.all().count()
        else:
            result_data = log.objects.filter(Q(name__contains=sSearch) | \
                                                Q(comment__contains=sSearch) | \
                                               Q(id__contains=sSearch)) \
                                            .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = log.objects.filter(Q(name__contains=sSearch) | \
                                                Q(comment__contains=sSearch) | \
                                               Q(id__contains=sSearch)).count()
    else:
        if sSearch == '':
            result_data = log.objects.all().order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = log.objects.all().count()
        else:
            result_data = log.objects.filter(Q(name__contains=sSearch) | \
                                                Q(comment__contains=sSearch) | \
                                               Q(id__contains=sSearch)) \
                                            .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = log.objects.filter(Q(name__contains=sSearch) | \
                                                Q(comment__contains=sSearch) | \
                                               Q(id__contains=sSearch)).count()
    for i in  result_data:
        aaData.append({
                       '0':i.name,
                       '1':i.comment,
                       '2':str(i.apply_time),
                       '3':i.id
                      })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(json.dumps(result),content_type="application/json")




@login_required
def repay_apply_bank(request):
    path = request.path.split('/')[1]
    return render(request, 'repay/repay_apply_bank.html',{'user':'%s%s' % (request.user.last_name,request.user.first_name),
                                                       'path1':'repay',
                                                       'path2':path,
                                                       'page_name1':u'报销管理',
                                                       'page_name2':u'银行报销申请'},context_instance=RequestContext(request))



@login_required
def repay_apply_sub(request):
    path = request.path.split('/')[1]
    try:
        orm_user = user_table.objects.get(name=request.user.first_name)
        orm = budget.objects.filter(date=str(datetime.datetime.now().date())).filter(department=orm_user.department)
        if orm:
            budget_available = orm[0].budget_available
    except Exception:
        return render(request,'public/no_passing.html')
    return render(request, 'vacation/vacation_apply_sub.html',{'budget_available':budget_available},context_instance=RequestContext(request))




@login_required
def repay_apply_data(request):
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    aaData = []
    sort = ['name','apply_time','budget_class','budget_class_level2','department','description','amount','amount_words',
            'payment_class','beneficiary_name','beneficiary_account','beneficiary_bank','contract_uuid','final_payment_date',
            'status','approve_now']

    if  sSortDir_0 == 'asc':
        if sSearch == '':
            result_data = repay.objects.filter(name=request.user.first_name).order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = repay.objects.filter(name=request.user.first_name).count()
        else:
            result_data = repay.objects.filter(name=request.user.first_name).filter(Q(name__contains=sSearch) | \
                                                    Q(budget_class__contains=sSearch) | \
                                                    Q(budget_class_level2__contains=sSearch) | \
                                                    Q(department__contains=sSearch) | \
                                                    Q(description__contains=sSearch) | \
                                                    Q(payment_class__contains=sSearch) | \
                                                    Q(beneficiary_name__contains=sSearch) | \
                                                    Q(beneficiary_account__contains=sSearch) | \
                                                    Q(beneficiary_bank__contains=sSearch) | \
                                                    Q(contract_uuid__contains=sSearch)) \
                                                    .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = repay.objects.filter(name=request.user.first_name).filter(Q(name__contains=sSearch) | \
                                                    Q(budget_class__contains=sSearch) | \
                                                    Q(budget_class_level2__contains=sSearch) | \
                                                    Q(department__contains=sSearch) | \
                                                    Q(description__contains=sSearch) | \
                                                    Q(payment_class__contains=sSearch) | \
                                                    Q(beneficiary_name__contains=sSearch) | \
                                                    Q(beneficiary_account__contains=sSearch) | \
                                                    Q(beneficiary_bank__contains=sSearch) | \
                                                    Q(contract_uuid__contains=sSearch)).count()
    else:
        if sSearch == '':
            result_data = repay.objects.filter(name=request.user.first_name).order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = repay.objects.filter(name=request.user.first_name).count()
        else:
            result_data = repay.objects.filter(name=request.user.first_name).filter(Q(name__contains=sSearch) | \
                                                    Q(budget_class__contains=sSearch) | \
                                                    Q(budget_class_level2__contains=sSearch) | \
                                                    Q(department__contains=sSearch) | \
                                                    Q(description__contains=sSearch) | \
                                                    Q(payment_class__contains=sSearch) | \
                                                    Q(beneficiary_name__contains=sSearch) | \
                                                    Q(beneficiary_account__contains=sSearch) | \
                                                    Q(beneficiary_bank__contains=sSearch) | \
                                                    Q(contract_uuid__contains=sSearch)) \
                                                    .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = repay.objects.filter(name=request.user.first_name).filter(Q(name__contains=sSearch) | \
                                                    Q(budget_class__contains=sSearch) | \
                                                    Q(budget_class_level2__contains=sSearch) | \
                                                    Q(department__contains=sSearch) | \
                                                    Q(description__contains=sSearch) | \
                                                    Q(payment_class__contains=sSearch) | \
                                                    Q(beneficiary_name__contains=sSearch) | \
                                                    Q(beneficiary_account__contains=sSearch) | \
                                                    Q(beneficiary_bank__contains=sSearch) | \
                                                    Q(contract_uuid__contains=sSearch)).count()

    for i in  result_data:
        if i.apply_time.month != datetime.datetime.now().month and i.status not in (7,8,9):
            i.status = 9
            i.save()

        aaData.append({
                       '0':i.name,
                       '1':str(i.apply_time),
                       '2':i.budget_class,
                       '3':i.budget_class_level2,
                       '4':i.department,
                       '5':i.description,
                       '6':i.amount,
                       '7':i.amount_words,
                       '8':i.payment_class,
                       '9':i.beneficiary_name,
                       '10':i.beneficiary_account,
                       '11':i.beneficiary_bank,
                       '12':i.contract_uuid,
                       '13':str(i.payment_date),
                       '14':i.status,
                       '15':i.id,
                       '16':i.approve_now
                      })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(json.dumps(result),content_type="application/json")



@login_required
def repay_apply_save(request):
    name = request.POST.get('name')
    payment_type = request.POST.get('payment_type')
    invoice_type = request.POST.get('invoice_type')
    budget_class = request.POST.get('budget_class')
    budget_class_level2 = request.POST.get('budget_class_level2')
    department = request.POST.get('department')
    description = request.POST.get('description')
    amount = request.POST.get('amount')
    payment_class = request.POST.get('payment_class')
    beneficiary_name = request.POST.get('beneficiary_name')
    beneficiary_account = request.POST.get('beneficiary_account')
    beneficiary_bank = request.POST.get('beneficiary_bank')
    contract_uuid = request.POST.get('contract_uuid')
    payment_date = request.POST.get('payment_date')
    _id = request.POST.get('id')

    try:

        if budget_class_level2 == None:
            budget_class_level2 = ''

        today_date = datetime.datetime.now().date()
        day = str(today_date.month)
        if len(day) == 1:
            day = '0' + day
        year_month = str(today_date.year) + '-' + day

        budget_orm = budget.objects.filter(date=year_month).filter(department=department).filter(budget_class=budget_class)

        if not budget_orm:
            return HttpResponse(json.dumps({'code':1,'msg':u'您没有该项预算'}),content_type="application/json")
        elif budget_orm[0].budget_available <= 0 and budget_orm[0].budget_available < float(amount):
            return HttpResponse(json.dumps({'code':1,'msg':u'该项预算金额不足'}),content_type="application/json")
        else:
            if not _id:
                budget_orm[0].budget_used = budget_orm[0].budget_used + float(amount)
                budget_orm[0].budget_available = budget_orm[0].budget_summary - budget_orm[0].budget_used
                budget_orm[0].save()

            amount_words = Num2MoneyFormat(float(amount))

            user_orm = user_table.objects.get(name=name)

            approve_now = user_orm.supervisor

            if contract_uuid is None:
                contract_uuid = ''

            if _id:
                orm = repay.objects.get(id=_id)
                orm.name = name
                orm.budget_class = budget_class
                orm.budget_class_level2 = budget_class_level2
                orm.department = department
                orm.description = description
                orm.amount = amount
                orm.amount_words = amount_words
                orm.payment_class = payment_class
                orm.beneficiary_name = beneficiary_name
                orm.beneficiary_account = beneficiary_account
                orm.beneficiary_bank = beneficiary_bank
                orm.contract_uuid = contract_uuid
                orm.payment_date = payment_date
                orm.status = 1
                orm.payment_type = payment_type
                orm.invoice_type = invoice_type
                orm.approve_now = approve_now
            else:
                orm = repay(name=name,budget_class=budget_class,budget_class_level2=budget_class_level2,department=department,
                            description=description,amount=amount,amount_words=amount_words,payment_class=payment_class,
                            beneficiary_name=beneficiary_name,beneficiary_account=beneficiary_account,
                            beneficiary_bank=beneficiary_bank,contract_uuid=contract_uuid,payment_date=payment_date,status=1,
                            payment_type=payment_type,invoice_type=invoice_type,approve_now=approve_now)

            # log_info = '<b>%s</b> 申请了 <b>%s</b>，日期为 <b>%s</b>，当前状态为 <b>%s</b>' % (request.user.first_name,type,vacation_date,state_interface)
            # orm_log = operation_log(name=request.user.first_name,operation=log_info)

            # orm_alert = user_table.objects.get(name=approve_now)
            # orm_alert.has_approve += 1

            # orm_log.save()
            # orm_alert.save()
            orm.save()

            # Thread(target=thread_run).start()
            # Thread(target=send_mail,args=(supervisor_email,'请假审批提醒','<h3>有一个请假事件等待您的审批，请在OA系统中查看。</h3><br>OA链接：http://oa.xiaoquan.com:10000/vacation_approve/</br><br>此邮件为自动发送的提醒邮件，请勿回复。')).start()
            return HttpResponse(json.dumps({'code':0,'msg':u'申请成功'}),content_type="application/json")
    except UnicodeEncodeError:
        return HttpResponse(json.dumps({'code':1,'msg':'金额不能输入除数字以外的内容'}),content_type="application/json")
    except Exception,e:
        return HttpResponse(json.dumps({'code':1,'msg':str(e)}),content_type="application/json")



@login_required
def repay_apply_del(request):
    _id = request.POST.get('id')
    orm = repay.objects.get(id=_id)
    try:
        if orm.status in (7,8,0):
            return HttpResponse(json.dumps({'code':0,'msg':u'改流程已完成,无法撤回'}),content_type="application/json")
        else:
            apply_date = orm.apply_time.date()

            day = str(apply_date.month)
            if len(day) == 1:
                day = '0' + day
            year_month = str(apply_date.year) + '-' + day

            budget_orm = budget.objects.filter(date=year_month).filter(department=orm.department).filter(budget_class=orm.budget_class)
            if len(budget_orm) == 1:
                for i in budget_orm:
                    budget_used = i.budget_used - orm.amount
                    i.budget_used = budget_used
                    i.budget_available = i.budget_summary - i.budget_used
                    i.save()
            else:
                return HttpResponse(json.dumps({'code':1,'msg':u'匹配到多条预算项目'}),content_type="application/json")

            orm.delete()

            return HttpResponse(json.dumps({'code':0,'msg':u'撤回成功'}),content_type="application/json")
    except Exception,e:
        return HttpResponse(json.dumps({'code':1,'msg':str(e)}),content_type="application/json")





@login_required
def repay_apply_bank_detail(request):
    _id = request.GET.get('id')
    if _id is not None:
        orm = repay.objects.get(id=_id)
        status = orm.status
        budget_class = orm.budget_class
        amount = orm.amount
        payment_date = str(orm.payment_date)
        beneficiary_name = orm.beneficiary_name
        beneficiary_bank = orm.beneficiary_bank
        beneficiary_account = orm.beneficiary_account
        description = orm.description
        payment_type = orm.payment_type
        invoice_type = orm.invoice_type
    else:
        status = 0
        budget_class = ''
        amount = ''
        payment_date = ''
        beneficiary_name = ''
        beneficiary_bank = ''
        beneficiary_account = ''
        description = ''
        payment_type = ''
        invoice_type = ''
        _id = ''
    path = request.path.split('/')[1]

    user_orm = user_table.objects.get(name=request.user.first_name)

    return render(request, 'repay/repay_apply_bank_detail.html',{'user':'%s%s' % (request.user.last_name,request.user.first_name),
                                                       'path1':'repay',
                                                       'path2':path,
                                                       'page_name1':u'报销管理',
                                                       'page_name2':u'银行报销申请',
                                                       'status':status,
                                                       'name':user_orm.name,
                                                       'department':user_orm.department,
                                                       'budget_class':budget_class,
                                                       'amount':amount,
                                                       'payment_date':payment_date,
                                                       'beneficiary_name':beneficiary_name,
                                                       'beneficiary_bank':beneficiary_bank,
                                                       'beneficiary_account':beneficiary_account,
                                                       'description':description,
                                                       'payment_type':payment_type,
                                                       'invoice_type':invoice_type,
                                                       'id':_id},context_instance=RequestContext(request))




@login_required
def repay_approve(request):
    path = request.path.split('/')[1]
    return render(request, 'repay/repay_approve.html',{'user':'%s%s' % (request.user.last_name,request.user.first_name),
                                                       'path1':'repay',
                                                       'path2':path,
                                                       'page_name1':u'报销管理',
                                                       'page_name2':u'报销审批'},context_instance=RequestContext(request))






@login_required
def repay_approve_data(request):
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    aaData = []
    sort = ['name','apply_time','budget_class','budget_class_level2','department','description','amount','amount_words',
            'payment_class','beneficiary_name','beneficiary_account','beneficiary_bank','contract_uuid','final_payment_date',
            'status','approve_now']

    if  sSortDir_0 == 'asc':
        if sSearch == '':
            result_data = repay.objects.filter(approve_now=request.user.first_name).order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = repay.objects.filter(approve_now=request.user.first_name).count()
        else:
            result_data = repay.objects.filter(approve_now=request.user.first_name).filter(Q(name__contains=sSearch) | \
                                                    Q(budget_class__contains=sSearch) | \
                                                    Q(budget_class_level2__contains=sSearch) | \
                                                    Q(department__contains=sSearch) | \
                                                    Q(description__contains=sSearch) | \
                                                    Q(payment_class__contains=sSearch) | \
                                                    Q(beneficiary_name__contains=sSearch) | \
                                                    Q(beneficiary_account__contains=sSearch) | \
                                                    Q(beneficiary_bank__contains=sSearch) | \
                                                    Q(contract_uuid__contains=sSearch)) \
                                                    .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = repay.objects.filter(approve_now=request.user.first_name).filter(Q(name__contains=sSearch) | \
                                                    Q(budget_class__contains=sSearch) | \
                                                    Q(budget_class_level2__contains=sSearch) | \
                                                    Q(department__contains=sSearch) | \
                                                    Q(description__contains=sSearch) | \
                                                    Q(payment_class__contains=sSearch) | \
                                                    Q(beneficiary_name__contains=sSearch) | \
                                                    Q(beneficiary_account__contains=sSearch) | \
                                                    Q(beneficiary_bank__contains=sSearch) | \
                                                    Q(contract_uuid__contains=sSearch)).count()
    else:
        if sSearch == '':
            result_data = repay.objects.filter(approve_now=request.user.first_name).order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = repay.objects.filter(approve_now=request.user.first_name).count()
        else:
            result_data = repay.objects.filter(approve_now=request.user.first_name).filter(Q(name__contains=sSearch) | \
                                                    Q(budget_class__contains=sSearch) | \
                                                    Q(budget_class_level2__contains=sSearch) | \
                                                    Q(department__contains=sSearch) | \
                                                    Q(description__contains=sSearch) | \
                                                    Q(payment_class__contains=sSearch) | \
                                                    Q(beneficiary_name__contains=sSearch) | \
                                                    Q(beneficiary_account__contains=sSearch) | \
                                                    Q(beneficiary_bank__contains=sSearch) | \
                                                    Q(contract_uuid__contains=sSearch)) \
                                                    .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = repay.objects.filter(approve_now=request.user.first_name).filter(Q(name__contains=sSearch) | \
                                                    Q(budget_class__contains=sSearch) | \
                                                    Q(budget_class_level2__contains=sSearch) | \
                                                    Q(department__contains=sSearch) | \
                                                    Q(description__contains=sSearch) | \
                                                    Q(payment_class__contains=sSearch) | \
                                                    Q(beneficiary_name__contains=sSearch) | \
                                                    Q(beneficiary_account__contains=sSearch) | \
                                                    Q(beneficiary_bank__contains=sSearch) | \
                                                    Q(contract_uuid__contains=sSearch)).count()

    for i in  result_data:
        aaData.append({
                       '0':i.name,
                       '1':str(i.apply_time),
                       '2':i.budget_class,
                       '3':i.budget_class_level2,
                       '4':i.department,
                       '5':i.description,
                       '6':i.amount,
                       '7':i.amount_words,
                       '8':i.payment_class,
                       '9':i.beneficiary_name,
                       '10':i.beneficiary_account,
                       '11':i.beneficiary_bank,
                       '12':i.contract_uuid,
                       '13':str(i.payment_date),
                       '14':i.status,
                       '15':i.id,
                       '16':i.approve_now
                      })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(json.dumps(result),content_type="application/json")





@login_required
def repay_approve_process(request):
    flag = request.POST.get('flag')
    _id = request.POST.get('id')
    comment = request.POST.get('comment')
    add_process = request.POST.get('add_process')
    print add_process,_id

    orm = repay.objects.get(id=_id)
    orm2 = user_table.objects.get(name=request.user.first_name)

    if request.user.first_name != orm.approve_now:
        return HttpResponse(json.dumps({'code':1,'msg':u'您不是审批人'}),content_type="application/json")

    if flag == '1':
        if orm.status == 1:
            if orm2.principal == '曹津':
                orm.status = 3
                orm.approve_now = u'龚晓芸'
                Thread(target=send_mail,args=('gongxiaoyun@xiaohulu.com','报销审批提醒','<h3>有一个报销事件等待您的审批，请在OA系统中查看。</h3><br>OA链接：http://oa.xiaoquan.com:10000/repay_approve/</br><br>此邮件为自动发送的提醒邮件，请勿回复。')).start()
            else:
                orm.status = 2
                orm.approve_now = orm2.principal
                orm3 = user_table.objects.get(name=orm2.principal)
                email = orm3.email
                Thread(target=send_mail,args=(email,'报销审批提醒','<h3>有一个报销事件等待您的审批，请在OA系统中查看。</h3><br>OA链接：http://oa.xiaoquan.com:10000/repay_approve/</br><br>此邮件为自动发送的提醒邮件，请勿回复。')).start()
        elif orm.status == 2:
            orm.status = 3
            orm.approve_now = u'龚晓芸'
            Thread(target=send_mail,args=('gongxiaoyun@xiaohulu.com','报销审批提醒','<h3>有一个报销事件等待您的审批，请在OA系统中查看。</h3><br>OA链接：http://oa.xiaoquan.com:10000/repay_approve/</br><br>此邮件为自动发送的提醒邮件，请勿回复。')).start()
        elif orm.status == 3:
            if add_process:
                orm.status = 4
                orm.approve_now = add_process
                orm3 = user_table.objects.get(name=add_process)
                email = orm3.email
                Thread(target=send_mail,args=(email,'报销审批提醒','<h3>有一个报销事件等待您的审批，请在OA系统中查看。</h3><br>OA链接：http://oa.xiaoquan.com:10000/repay_approve/</br><br>此邮件为自动发送的提醒邮件，请勿回复。')).start()
            else:
                orm.status = 5
                orm.approve_now = u'高茹'
                Thread(target=send_mail,args=('gaoru@xiaohulu.com','报销审批提醒','<h3>有一个报销事件等待您的审批，请在OA系统中查看。</h3><br>OA链接：http://oa.xiaoquan.com:10000/repay_approve/</br><br>此邮件为自动发送的提醒邮件，请勿回复。')).start()
        elif orm.status == 4:
            orm.status = 5
            orm.approve_now = u'高茹'
            Thread(target=send_mail,args=('gaoru@xiaohulu.com','报销审批提醒','<h3>有一个报销事件等待您的审批，请在OA系统中查看。</h3><br>OA链接：http://oa.xiaoquan.com:10000/repay_approve/</br><br>此邮件为自动发送的提醒邮件，请勿回复。')).start()
        elif orm.status == 5:
            if orm.amount <= 10000:
                orm.status = 7
                orm.approve_now = ''
            else:
                orm.status = 6
                orm.approve_now = u'曹津'
                Thread(target=send_mail,args=('caojin@xiaohulu.com','报销审批提醒','<h3>有一个报销事件等待您的审批，请在OA系统中查看。</h3><br>OA链接：http://oa.xiaoquan.com:10000/repay_approve/</br><br>此邮件为自动发送的提醒邮件，请勿回复。')).start()
        elif orm.status == 6:
            orm.status = 7
            orm.approve_now = ''
    elif flag == '2':
        orm.status = 0
        orm.approve_now = orm.name
    else:
        orm.status = 8
        orm.approve_now = ''

        apply_date = orm.apply_time.date()

        day = str(apply_date.month)
        if len(day) == 1:
            day = '0' + day
        year_month = str(apply_date.year) + '-' + day

        budget_orm = budget.objects.filter(date=year_month).filter(department=orm.department).filter(budget_class=orm.budget_class)
        if len(budget_orm) == 1:
            for i in budget_orm:
                budget_used = i.budget_used - orm.amount
                i.budget_used = budget_used
                i.budget_available = i.budget_summary - i.budget_used
                i.save()
        else:
            return HttpResponse(json.dumps({'code':1,'msg':u'匹配到多条预算项目'}),content_type="application/json")

    orm.save()
    orm2 = detail(name=request.user.first_name,operation=flag,comment=comment,parent_id=_id)
    orm2.save()
    return HttpResponse(json.dumps({'code':0,'msg':u'提交成功'}),content_type="application/json")





@login_required
def repay_all(request):
    path = request.path.split('/')[1]
    return render(request, 'repay/repay_all.html',{'user':'%s%s' % (request.user.last_name,request.user.first_name),
                                                       'path1':'repay',
                                                       'path2':path,
                                                       'page_name1':u'报销管理',
                                                       'page_name2':u'报销审批'},context_instance=RequestContext(request))






@login_required
def repay_all_data(request):
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    aaData = []
    sort = ['name','apply_time','budget_class','budget_class_level2','department','description','amount','amount_words',
            'payment_class','beneficiary_name','beneficiary_account','beneficiary_bank','contract_uuid','final_payment_date',
            'status','approve_now']

    if  sSortDir_0 == 'asc':
        if sSearch == '':
            result_data = repay.objects.all().order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = repay.objects.all().count()
        else:
            result_data = repay.objects.all().filter(Q(name__contains=sSearch) | \
                                                    Q(budget_class__contains=sSearch) | \
                                                    Q(budget_class_level2__contains=sSearch) | \
                                                    Q(department__contains=sSearch) | \
                                                    Q(description__contains=sSearch) | \
                                                    Q(payment_class__contains=sSearch) | \
                                                    Q(beneficiary_name__contains=sSearch) | \
                                                    Q(beneficiary_account__contains=sSearch) | \
                                                    Q(beneficiary_bank__contains=sSearch) | \
                                                    Q(contract_uuid__contains=sSearch)) \
                                                    .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = repay.objects.all().filter(Q(name__contains=sSearch) | \
                                                    Q(budget_class__contains=sSearch) | \
                                                    Q(budget_class_level2__contains=sSearch) | \
                                                    Q(department__contains=sSearch) | \
                                                    Q(description__contains=sSearch) | \
                                                    Q(payment_class__contains=sSearch) | \
                                                    Q(beneficiary_name__contains=sSearch) | \
                                                    Q(beneficiary_account__contains=sSearch) | \
                                                    Q(beneficiary_bank__contains=sSearch) | \
                                                    Q(contract_uuid__contains=sSearch)).count()
    else:
        if sSearch == '':
            result_data = repay.objects.all().order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = repay.objects.all().count()
        else:
            result_data = repay.objects.all().filter(Q(name__contains=sSearch) | \
                                                    Q(budget_class__contains=sSearch) | \
                                                    Q(budget_class_level2__contains=sSearch) | \
                                                    Q(department__contains=sSearch) | \
                                                    Q(description__contains=sSearch) | \
                                                    Q(payment_class__contains=sSearch) | \
                                                    Q(beneficiary_name__contains=sSearch) | \
                                                    Q(beneficiary_account__contains=sSearch) | \
                                                    Q(beneficiary_bank__contains=sSearch) | \
                                                    Q(contract_uuid__contains=sSearch)) \
                                                    .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = repay.objects.all().filter(Q(name__contains=sSearch) | \
                                                    Q(budget_class__contains=sSearch) | \
                                                    Q(budget_class_level2__contains=sSearch) | \
                                                    Q(department__contains=sSearch) | \
                                                    Q(description__contains=sSearch) | \
                                                    Q(payment_class__contains=sSearch) | \
                                                    Q(beneficiary_name__contains=sSearch) | \
                                                    Q(beneficiary_account__contains=sSearch) | \
                                                    Q(beneficiary_bank__contains=sSearch) | \
                                                    Q(contract_uuid__contains=sSearch)).count()

    for i in  result_data:
        aaData.append({
                       '0':i.name,
                       '1':str(i.apply_time),
                       '2':i.budget_class,
                       '3':i.budget_class_level2,
                       '4':i.department,
                       '5':i.description,
                       '6':i.amount,
                       '7':i.amount_words,
                       '8':i.payment_class,
                       '9':i.beneficiary_name,
                       '10':i.beneficiary_account,
                       '11':i.beneficiary_bank,
                       '12':i.contract_uuid,
                       '13':str(i.payment_date),
                       '14':i.status,
                       '15':i.id,
                       '16':i.approve_now
                      })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(json.dumps(result),content_type="application/json")




@login_required
def repay_process_detail_data(request):
    parent_id = request.GET.get('parent_id')
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    aaData = []
    sort = ['apply_time','name','operation','comment','id']

    if not parent_id:
        parent_id = None

    if  sSortDir_0 == 'asc':
        if sSearch == '':
            result_data = detail.objects.filter(parent_id=parent_id).order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = detail.objects.filter(parent_id=parent_id).count()
        else:
            result_data = detail.objects.filter(parent_id=parent_id).filter(Q(name__contains=sSearch) | \
                                                                                          Q(comment__contains=sSearch) | \
                                                                                          Q(id__contains=sSearch)) \
                                            .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = detail.objects.filter(parent_id=parent_id).filter(Q(name__contains=sSearch) | \
                                                                                          Q(comment__contains=sSearch) | \
                                                                                          Q(id__contains=sSearch)).count()
    else:
        if sSearch == '':
            result_data = detail.objects.filter(parent_id=parent_id).order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = detail.objects.filter(parent_id=parent_id).count()
        else:
            result_data = detail.objects.filter(parent_id=parent_id).filter(Q(name__contains=sSearch) | \
                                                                                          Q(comment__contains=sSearch) | \
                                                                                          Q(id__contains=sSearch)) \
                                            .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = detail.objects.filter(parent_id=parent_id).filter(Q(name__contains=sSearch) | \
                                                                                          Q(comment__contains=sSearch) | \
                                                                                          Q(id__contains=sSearch)).count()

    for i in  result_data:
        aaData.append({
                       '0':str(i.apply_time),
                       '1':i.name,
                       '2':i.operation,
                       '3':i.comment.replace('\n','</br>'),
                       '4':i.id
                      })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(json.dumps(result),content_type="application/json")