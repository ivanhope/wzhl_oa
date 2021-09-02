#coding:utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from vacation.models import user_table
from work_out.models import table
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from libs.sendmail import send_mail
from wzhl_oa.settings import HR,BASE_DIR
from models import *
import json
from threading import Thread
import datetime

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

@login_required
def work_out_apply(request):
    path = request.path.split('/')[1]
    try:
        orm = user_table.objects.get(name=request.user.first_name)
    except Exception:
        return render(request,'public/no_passing.html')
    return render(request, 'work_out/work_out_apply.html',{'user':'%s%s' % (request.user.last_name,request.user.first_name),
                                                       'path1':'work_out',
                                                       'path2':path,
                                                       'page_name1':u'公事外出',
                                                       'page_name2':u'公事外出申请'},context_instance=RequestContext(request))


@login_required
def work_out_apply_data(request):
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    aaData = []
    sort = ['name', 'reason', 'city', 'place', 'target', 'apply_time', 'vacation_date', 'days', 'state_interface']

    if  sSortDir_0 == 'asc':
        if sSearch == '':
            result_data = table.objects.filter(name=request.user.first_name).order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = table.objects.filter(name=request.user.first_name).count()
        else:
            result_data = table.objects.filter(name=request.user.first_name).filter(name__contains=sSearch) \
                                                    .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = table.objects.filter(name=request.user.first_name).filter(name__contains=sSearch).count()
    else:
        if sSearch == '':
            result_data = table.objects.filter(name=request.user.first_name).order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = table.objects.filter(name=request.user.first_name).count()
        else:
            result_data = table.objects.filter(name=request.user.first_name).filter(name__contains=sSearch) \
                                                    .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = table.objects.filter(name=request.user.first_name).filter(name__contains=sSearch).count()

    for i in  result_data:
        aaData.append({
                       '0':i.name,
                       '1':i.reason,
                       '2':i.city,
                       '3':i.place,
                       '4':i.target,
                       '5':str(i.apply_time).split('+')[0],
                       '6':i.vacation_date,
                       '7':i.days,
                       '8':i.handover_to,
                       '9':i.state,
                       '10':i.state_interface,
                       '11':i.id
                      })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(json.dumps(result),content_type="application/json")



@login_required
def work_out_apply_save(request):
    reason = request.POST.get('reason')
    city = request.POST.get('city')
    district = request.POST.get('district')
    place = request.POST.get('place')
    target = request.POST.get('target')
    begin = request.POST.get('begin')
    end = request.POST.get('end')
    half_day = request.POST.get('half_day')
    handover_to = request.POST.get('handover_to')

    if begin == end:
        days = 1
        vacation_date = begin
        if half_day:
            days = 0.5
            vacation_date = '%s %s' % (vacation_date,half_day)
    else:
        begin_list = begin.split('-')
        begin_datetime = datetime.date(int(begin_list[0]),int(begin_list[1]),int(begin_list[2]))
        end_list = end.split('-')
        end_datetime = datetime.date(int(end_list[0]),int(end_list[1]),int(end_list[2]))
        days = (end_datetime - begin_datetime).days + 1
        vacation_date = begin + '&nbsp->&nbsp' + end

    orm_fetch_supervisor = user_table.objects.get(name=request.user.first_name)

    if orm_fetch_supervisor.supervisor == '/':
        return HttpResponse(json.dumps({'code':0,'msg':u'您是中心负责人无需申请'}),content_type="application/json")

    if not reason:
        return HttpResponse(json.dumps({'code':1,'msg':u'公事外出的请假原由不能为空'}),content_type="application/json")

    approve_now = orm_fetch_supervisor.supervisor
    state_interface = u'等待 ' + orm_fetch_supervisor.supervisor + u' 审批'
    orm_supervisor = user_table.objects.get(name=approve_now)
    supervisor_email = orm_supervisor.email
    # Thread(target=send_mail,args=(supervisor_email,'请假审批提醒','<h3>有一个公事外出事件等待您的审批，请在OA系统中查看。</h3><br>OA链接：http://oa.xiaoquan.com:10000/vacation_approve/</br><br>此邮件为自动发送的提醒邮件，请勿回复。')).start()

    orm = table(name=request.user.first_name,reason=reason,city='{0} {1}'.format(city,district),place=place,target=target,
                vacation_date=vacation_date,days=days,handover_to=handover_to,state_interface=state_interface,state=1,
                approve_now=approve_now,real_days=0)

    # log_info = '<b>%s</b> 申请了 <b>%s</b>，日期为 <b>%s</b>，当前状态为 <b>%s</b>' % (request.user.first_name, type, vacation_date, state_interface)
    # orm_log = operation_log(name=request.user.first_name, operation=log_info)
    # orm_log.save()

    orm.save()
    return HttpResponse(json.dumps({'code':0,'msg':u'保存成功'}),content_type="application/json")




@login_required
def work_out_apply_del(request):
    try:
        _id = request.POST.get('id')
        orm = table.objects.get(id=_id)
        if orm.state_interface == '已批准' or orm.state_interface == '不批准' or orm.state_interface == '已过期':
            return HttpResponse(json.dumps({'code':1,'msg':u'已审批完成无法删除'}),content_type="application/json")

        orm.delete()
        return HttpResponse(json.dumps({'code':0,'msg':u'删除成功'}),content_type="application/json")
    except Exception,e:
        print e
        return HttpResponse(json.dumps({'code':1,'msg':str(e)}),content_type="application/json")



@login_required
def work_out_approve(request):
    path = request.path.split('/')[1]
    try:
        orm = user_table.objects.get(name=request.user.first_name)
    except Exception:
        return render(request,'public/no_passing.html')
    return render(request, 'work_out/work_out_approve.html',{'user':'%s%s' % (request.user.last_name,request.user.first_name),
                                                       'path1':'work_out',
                                                       'path2':path,
                                                       'page_name1':u'公事外出',
                                                       'page_name2':u'公事外出审批',},context_instance=RequestContext(request))

@login_required
def work_out_approve_data(request):
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    aaData = []
    sort = ['name','work_site','reason','city','place','target','apply_time','vacation_date','days','handover_to',None,'state_interface']


    if  sSortDir_0 == 'asc':
        if sSearch == '':
            result_data = table.objects.filter(approve_now=request.user.first_name).order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = table.objects.filter(approve_now=request.user.first_name).count()
        else:
            result_data = table.objects.filter(approve_now=request.user.first_name).filter(name__contains=sSearch) \
                                                    .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = table.objects.filter(approve_now=request.user.first_name).filter(name__contains=sSearch).count()
    else:
        if sSearch == '':
            result_data = table.objects.filter(approve_now=request.user.first_name).order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = table.objects.filter(approve_now=request.user.first_name).count()
        else:
            result_data = table.objects.filter(approve_now=request.user.first_name).filter(name__contains=sSearch) \
                                                    .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = table.objects.filter(approve_now=request.user.first_name).filter(name__contains=sSearch).count()


    for i in  result_data:
        try:
            work_site_orm = user_table.objects.get(name=i.name)
            work_site = work_site_orm.work_site
        except:
            work_site = ''
        aaData.append({
                       '0':i.name,
                       '1':work_site,
                       '2':i.reason,
                       '3':i.city,
                       '4':i.place,
                       '5':i.target,
                       '6':str(i.apply_time).split('+')[0],
                       '7':i.vacation_date,
                       '8':i.days,
                       '9':i.handover_to,
                       '10':i.state,
                       '11':i.state_interface,
                       '12':i.id
                      })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(json.dumps(result),content_type="application/json")


@login_required
def work_out_all(request):
    path = request.path.split('/')[1]
    try:
        orm = user_table.objects.get(name=request.user.first_name)
    except Exception:
        return render(request,'public/no_passing.html')
    return render(request, 'work_out/work_out_all.html',{'user':'%s%s' % (request.user.last_name,request.user.first_name),
                                                       'path1':'work_out',
                                                       'path2':path,
                                                       'page_name1':u'公事外出',
                                                       'page_name2':u'全部公事外出',},context_instance=RequestContext(request))

@login_required
def work_out_all_data(request):
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    aaData = []
    sort = ['name','work_site','reason','city','place','target','apply_time','vacation_date','days','handover_to',None,'state_interface']

    if request.user.has_perm('vacation.can_view_all'):
        if  sSortDir_0 == 'asc':
            if sSearch == '':
                result_data = table.objects.all().order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = table.objects.all().count()
            else:
                result_data = table.objects.filter(name__contains=sSearch) \
                                                        .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = table.objects.filter(name__contains=sSearch).count()
        else:
            if sSearch == '':
                result_data = table.objects.all().order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = table.objects.all().count()
            else:
                result_data = table.objects.filter(name__contains=sSearch) \
                                                        .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = table.objects.filter(name__contains=sSearch).count()

    else:
        subordinate = []
        subordinate_orm = user_table.objects.filter(Q(supervisor=request.user.first_name) | Q(principal=request.user.first_name))
        for i in subordinate_orm:
            subordinate.append(i.name)

        # orm_approved_id = user_table.objects.get(name=request.user.first_name)
        # approved_id_list = orm_approved_id.approved_id.split(',')
        # if approved_id_list != [u'']:
        #     approved_id_list = map(lambda x:int(x), approved_id_list)
        # else:
        #     approved_id_list = []
        #
        # if  orm_approved_id.subordinate:
        #     subordinate_list = orm_approved_id.subordinate.split(',')
        # else:
        #     subordinate_list = []

        if  sSortDir_0 == 'asc':
            if sSearch == '':
                result_data = table.objects.filter(Q(approve_now=request.user.first_name) | Q(name__in=subordinate)).order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = table.objects.filter(Q(approve_now=request.user.first_name) | Q(name__in=subordinate)).count()
            else:
                result_data = table.objects.filter(Q(approve_now=request.user.first_name) | Q(name__in=subordinate)).filter(name__contains=sSearch) \
                                                        .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = table.objects.filter(Q(approve_now=request.user.first_name) | Q(name__in=subordinate)).filter(name__contains=sSearch).count()
        else:
            if sSearch == '':
                result_data = table.objects.filter(Q(approve_now=request.user.first_name) | Q(name__in=subordinate)).order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = table.objects.filter(Q(approve_now=request.user.first_name) | Q(name__in=subordinate)).count()
            else:
                result_data = table.objects.filter(Q(approve_now=request.user.first_name) | Q(name__in=subordinate)).filter(name__contains=sSearch) \
                                                        .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = table.objects.filter(Q(approve_now=request.user.first_name) | Q(name__in=subordinate)).filter(name__contains=sSearch).count()

    for i in  result_data:
        try:
            work_site_orm = user_table.objects.get(name=i.name)
            work_site = work_site_orm.work_site
        except:
            work_site = ''
        aaData.append({
                       '0':i.name,
                       '1':work_site,
                       '2':i.reason,
                       '3':i.city,
                       '4':i.place,
                       '5':i.target,
                       '6':str(i.apply_time).split('+')[0],
                       '7':i.vacation_date,
                       '8':i.days,
                       '9':i.handover_to,
                       '10':i.state,
                       '11':i.state_interface,
                       '12':i.id
                      })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(json.dumps(result),content_type="application/json")


@login_required
def work_out_approve_process(request):
    flag = request.POST.get('flag')
    dst_id = request.POST.get('dst_id')
    disagree_reason = request.POST.get('disagree_reason')

    orm = table.objects.get(id=dst_id)

    if orm.approve_now != request.user.first_name:
        return HttpResponse(json.dumps({'code':1,'msg':u'这条申请的审批人不是您'}),content_type="application/json")

    if int(flag) == 1:
        if orm.state == 1:
            state_interface = u'等待 ' + HR['name'] + u' 审批'
            HR_email = HR['email']

            orm.state_interface = state_interface
            orm.approve_now = HR['name']
            orm.state = 3

            try:
                orm.save()
                # Thread(target=send_mail,args=(HR_email,'请假申请已批准','<h3>您的请假申请已被批准，请在OA系统中查看。</h3><br>OA链接：http://oa.xiaoquan.com:10000/vacation_approve/</br><br>此邮件为自动发送的提醒邮件，请勿回复。')).start()

                return HttpResponse(json.dumps({'code':0,'msg':u'审批成功'}),content_type="application/json")
            except Exception,e:
                print e
                return HttpResponse(json.dumps({'code':1,'msg':str(e)}),content_type="application/json")
        if orm.state == 3:
            orm.state_interface = '已批准'
            orm.state = 8
            orm.approve_now = ''

            orm_fetch_principal = user_table.objects.get(name=orm.name)
            apply_email = orm_fetch_principal.email
            try:
                orm.save()
                # Thread(target=send_mail,args=(apply_email,'请假申请已批准','<h3>您的请假申请已被批准，请在OA系统中查看。</h3><br>OA链接：http://oa.xiaoquan.com:10000/vacation_approve/</br><br>此邮件为自动发送的提醒邮件，请勿回复。')).start()

                return HttpResponse(json.dumps({'code':0,'msg':u'审批成功'}),content_type="application/json")
            except Exception,e:
                print e
                return HttpResponse(json.dumps({'code':1,'msg':str(e)}),content_type="application/json")
    if int(flag) == 0:
        try:
            orm.state_interface = '不批准'
            orm.state = 0
            orm.approve_now = ''

            fetch_email = user_table.objects.get(name=orm.name)
            email = fetch_email.email

            # Thread(target=send_mail,args=(email,'请假申请被拒绝','<h3>您的请假申请被拒绝，请在OA系统中查看。</h3><br>拒绝理由：<font color="red">%s</font><br>OA链接：http://oa.xiaoquan.com:10000/vacation_approve/</br><br>此邮件为自动发送的提醒邮件，请勿回复。' % disagree_reason)).start()

            orm.save()

            return HttpResponse(json.dumps({'code':0,'msg':u'审批成功'}),content_type="application/json")
        except Exception,e:
            print e
            return HttpResponse(json.dumps({'code':1,'msg':str(e)}),content_type="application/json")


@login_required
def work_out_approve_alert(request):
    orm = table.objects.filter(approve_now=request.user.first_name)
    if len(orm) > 0:
        msg = '有%s个公事外出事件等待您的审批' % len(orm)
        return HttpResponse(json.dumps({'code':0,'msg':msg}),content_type="application/json")
    else:
        return HttpResponse(json.dumps({'code':1}),content_type="application/json")