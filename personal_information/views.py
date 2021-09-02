# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from personal_information.models import table, interview
from wzhl_oa.settings import BASE_DIR
import json
import datetime
import os

@login_required
def personal_information_table(request):
    path = request.path.split('/')[1]
    return render(request, 'personal_information/personal_information_table.html',{'user':'%s%s' % (request.user.last_name,request.user.first_name),
                                                 'path1':'personal_information',
                                                 'path2':path,
                                                 'page_name1':u'人员信息',
                                                 'page_name2':u'人员基本信息表',},
                                                context_instance=RequestContext(request))

@login_required
def personal_information_table_data(request):
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    aaData = []
    sort = ['name','phone','email','keywords']

    if  sSortDir_0 == 'asc':
        if sSearch == '':
            result_data = table.objects.all().order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = table.objects.all().count()
        else:
            result_data = table.objects.all()
            sSearch_list = sSearch.split()
            for i in range(len(sSearch_list)):
                result_data = result_data.filter(Q(name__contains=sSearch_list[i]) | \
                                                        Q(phone__contains=sSearch_list[i]) | \
                                                        Q(email__contains=sSearch_list[i]) | \
                                                        Q(keywords__contains=sSearch_list[i]))

                iTotalRecords = result_data.filter(Q(name__contains=sSearch_list[i]) | \
                                                        Q(phone__contains=sSearch_list[i]) | \
                                                        Q(email__contains=sSearch_list[i]) | \
                                                        Q(keywords__contains=sSearch_list[i])).count()
            result_data = result_data.order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
    else:
        if sSearch == '':
            result_data = table.objects.all().order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = table.objects.all().count()
        else:
            result_data = table.objects.all()
            sSearch_list = sSearch.split()
            for i in range(len(sSearch_list)):
                result_data = result_data.filter(Q(name__contains=sSearch_list[i]) | \
                                                        Q(phone__contains=sSearch_list[i]) | \
                                                        Q(email__contains=sSearch_list[i]) | \
                                                        Q(keywords__contains=sSearch_list[i]))

                iTotalRecords = result_data.filter(Q(name__contains=sSearch_list[i]) | \
                                                        Q(phone__contains=sSearch_list[i]) | \
                                                        Q(email__contains=sSearch_list[i]) | \
                                                        Q(keywords__contains=sSearch_list[i])).count()
            result_data = result_data.order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]


    for i in  result_data:
        aaData.append({
                       '0':i.name,
                       '1':i.phone,
                       '2':i.email,
                       '3':i.keywords,
                       '4':i.id
                      })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(json.dumps(result),content_type="application/json")

@login_required
def personal_information_table_detail(request):
    path = request.path.split('/')[1]
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    keywords = request.POST.get('keywords')
    sex = request.POST.get('sex')
    graduate_date = request.POST.get('graduate_date')
    first_education = request.POST.get('first_education')
    education = request.POST.get('education')
    specialty = request.POST.get('specialty')
    graduate_school = request.POST.get('graduate_school')
    last_company = request.POST.get('last_company')
    channel = request.POST.get('channel')
    referrer = request.POST.get('referrer')
    salary = request.POST.get('salary')
    job_level = request.POST.get('job_level')
    job_title = request.POST.get('job_title')
    job_type = request.POST.get('job_type')
    resumes = request.FILES.get('resumes')
    direction = request.POST.get('direction')
    resource_state = request.POST.get('resource_state')
    comment = request.POST.get('comment')
    executor = request.POST.get('executor')
    _id = request.POST.get('id')

    try:
        request.session.pop('personal_information')
    except KeyError:
        pass
    if graduate_date:
        graduate_date_list = graduate_date.split('-')
        graduate_date_datetime = datetime.date(int(graduate_date_list[0]),int(graduate_date_list[1]),int(graduate_date_list[2]))
        today_datetime = datetime.datetime.now().date()
        graduate_year = (today_datetime - graduate_date_datetime).days // 365

    if _id:
        orm = table.objects.get(id=_id)
        if orm.resource_state != resource_state:
            orm.state_change_time = datetime.datetime.now()
        orm.name = name
        orm.email = email
        orm.phone = phone
        orm.keywords = keywords
        orm.sex = sex
        orm.graduate_year = graduate_year
        orm.graduate_date = graduate_date
        orm.first_education = first_education
        orm.education = education
        orm.specialty = specialty
        orm.graduate_school = graduate_school
        orm.last_company = last_company
        orm.channel = channel
        orm.referrer = referrer
        orm.salary = salary
        orm.job_level = job_level
        orm.job_title = job_title
        orm.job_type = job_type
        orm.resumes = resumes
        orm.direction = direction
        orm.resource_state = resource_state
        orm.comment = comment
        orm.executor = executor

        try:
            orm.save()
            request.session['personal_information'] = u'保存成功'
        except Exception,e:
            print e
            request.session['personal_information'] = e
    else:
        if name:
            orm = table(name=name,email=email,phone=phone,keywords=keywords,sex=sex,graduate_year=graduate_year,graduate_date=graduate_date,
                        first_education=first_education,education=education,specialty=specialty,graduate_school=graduate_school,
                        last_company=last_company,channel=channel,referrer=referrer,salary=salary,job_level=job_level,
                        job_title=job_title,job_type=job_type,resumes=resumes,direction=direction,resource_state=resource_state,
                        comment=comment,executor=executor,state_change_time=datetime.datetime.now())
            try:
                orm.save()
                request.session['personal_information'] = u'保存成功'
            except Exception,e:
                print e
                request.session['personal_information'] = e

    personal_information_id = request.session.get('personal_information_id')
    if personal_information_id:
        orm = table.objects.get(id=personal_information_id)
        return render(request, 'personal_information/personal_information_table_detail.html'
                      ,{'user':'%s%s' % (request.user.last_name,request.user.first_name),
                        'path1':'personal_information',
                        'path2':path,
                        'page_name1':u'人员信息',
                        'page_name2':u'人员基本信息表',
                        'name':orm.name,
                        'phone':orm.phone,
                        'email':orm.email,
                        'keywords':orm.keywords,
                        'sex':orm.sex,
                        'date_of_entry':str(orm.date_of_entry).split('+')[0],
                        'graduate_year':orm.graduate_year,
                        'graduate_date':str(orm.graduate_date).split('+')[0],
                        'first_education':orm.first_education,
                        'education':orm.education,
                        'specialty':orm.specialty,
                        'graduate_school':orm.graduate_school,
                        'last_company':orm.last_company,
                        'channel':orm.channel,
                        'referrer':orm.referrer,
                        'salary':orm.salary,
                        'job_level':orm.job_level,
                        'job_title':orm.job_title,
                        'job_type':orm.job_type,
                        'resumes':os.path.basename(str(orm.resumes)),
                        'resumes_path':str(orm.resumes),
                        'direction':orm.direction,
                        'resource_state':orm.resource_state,
                        'comment':orm.comment,
                        'state_change_time':str(orm.state_change_time).split('+')[0],
                        'executor':orm.executor,
                        'update_time':str(orm.update_time).split('+')[0],
                        'id':orm.id},
                      context_instance=RequestContext(request))
    return render(request, 'personal_information/personal_information_table_detail.html',{'user':'%s%s' % (request.user.last_name,request.user.first_name),
                                                 'path1':'personal_information',
                                                 'path2':path,
                                                 'page_name1':u'人员信息',
                                                 'page_name2':u'人员基本信息表',},
                                                context_instance=RequestContext(request))

@login_required
def personal_information_set_session(request):
    _id = request.POST.get('id')
    if _id == '0':
        try:
            request.session.pop('personal_information_id')
        except KeyError:
            pass
    elif _id:
        request.session['personal_information_id'] = int(_id)
    return HttpResponse(json.dumps('OK'),content_type="application/json")

@login_required
def personal_information_interview_data(request):
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    _id = request.session.get('personal_information_id')
    if _id:
        orm = table.objects.get(id=int(_id))
        name = orm.name
    else:
        name = ''

    aaData = []
    sort = ['name','interview_times','id']

    if  sSortDir_0 == 'asc':
        if sSearch == '':
            result_data = interview.objects.filter(name=name).order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = interview.objects.filter(name=name).count()
        else:
            result_data = interview.objects.filter(name=name).filter(Q(name__contains=sSearch) | \
                                                    Q(interview_times__contains=sSearch)) \
                                                    .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = interview.objects.filter(name=name).filter(Q(name__contains=sSearch) | \
                                                    Q(interview_times__contains=sSearch)).count()
    else:
        if sSearch == '':
            result_data = interview.objects.filter(name=name).order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = interview.objects.filter(name=name).count()
        else:
            result_data = interview.objects.filter(name=name).filter(Q(name__contains=sSearch) | \
                                                    Q(interview_times__contains=sSearch)) \
                                                    .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = interview.objects.filter(name=name).filter(Q(name__contains=sSearch) | \
                                                    Q(interview_times__contains=sSearch)).count()


    for i in  result_data:
        aaData.append({
                       '0':i.name,
                       '1':i.interview_times,
                       '2':i.id
                      })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(json.dumps(result),content_type="application/json")

@login_required
def personal_information_interview_set_session(request):
    _id = request.POST.get('id')
    if _id == '0':
        try:
            request.session.pop('personal_information_interview_id')
        except KeyError:
            pass
    elif _id:
        request.session['personal_information_interview_id'] = int(_id)
    return HttpResponse(json.dumps('OK'),content_type="application/json")

@login_required
def personal_information_interview_detail(request):
    path = request.path.split('/')[1]
    # name = request.POST.get('name')
    # channel = request.POST.get('channel')
    # education = request.POST.get('education')
    # interview_times = request.POST.get('interview_times')
    interview_date = request.POST.get('interview_date')
    reply_date = request.POST.get('reply_date')
    interview_mode = request.POST.get('interview_mode')
    # job_title = request.POST.get('job_title')
    # job_type = request.POST.get('job_type')
    # direction = request.POST.get('direction')
    invitation_success = request.POST.get('invitation_success')
    invitation_condition = request.POST.get('invitation_condition')
    interview_department = request.POST.get('interview_department')
    interviewer = request.POST.get('interviewer')
    interview_result = request.POST.get('interview_result')
    salary_now = request.POST.get('salary_now')
    except_salary = request.POST.get('except_salary')
    executor = request.POST.get('executor')
    comment = request.POST.get('comment')
    _id = request.POST.get('id')

    table_id =  request.session.get('personal_information_id')
    if table_id:
        orm = table.objects.get(id=table_id)
        name = orm.name
        channel = orm.channel
        education = orm.education
        job_title = orm.job_title
        job_type = orm.job_type
        direction = orm.direction
        all_entry_orm = interview.objects.filter(name=name)
        interview_times = len(all_entry_orm) + 1
    else:
        request.session['personal_information_interview'] = 'session失效，无法获取信息，请返回重新添加'
        return render(request, 'personal_information/personal_information_interview_detail.html',{'user':'%s%s' % (request.user.last_name,request.user.first_name),
                                                 'path1':'personal_information',
                                                 'path2':path,
                                                 'page_name1':u'人员信息',
                                                 'page_name2':u'人员基本信息表',},
                                                context_instance=RequestContext(request))

    try:
        request.session.pop('personal_information_interview')
    except KeyError:
        pass

    if _id:
        orm = interview.objects.get(id=_id)
        orm.name = name
        orm.channel = channel
        orm.education = education
        all_entry_orm = interview.objects.filter(name=name)
        orm.interview_times = len(all_entry_orm) + 1
        orm.interview_date = interview_date
        orm.reply_date = reply_date
        orm.interview_mode = interview_mode
        orm.job_title = job_title
        orm.job_type = job_type
        orm.direction = direction
        orm.invitation_success = invitation_success
        orm.invitation_condition = invitation_condition
        orm.interview_department = interview_department
        orm.interviewer = interviewer
        orm.interview_result = interview_result
        orm.salary_now = salary_now
        orm.except_salary = except_salary
        orm.executor = executor
        orm.comment = comment

        try:
            orm.save()
            request.session['personal_information_interview'] = u'保存成功'
        except Exception,e:
            print e
            request.session['personal_information_interview'] = e
    else:
        if interview_date:
            orm = interview(name=name,channel=channel,education=education,interview_times=interview_times,
                            interview_date=interview_date,reply_date=reply_date,interview_mode=interview_mode,
                            job_title=job_title,job_type=job_type,direction=direction,
                            invitation_success=invitation_success,invitation_condition=invitation_condition,
                            interview_department=interview_department,interviewer=interviewer,
                            interview_result=interview_result,salary_now=salary_now,except_salary=except_salary,
                            executor=executor,comment=comment)
            try:
                orm.save()
                request.session['personal_information_interview'] = u'保存成功'
            except Exception,e:
                print e
                request.session['personal_information_interview'] = e

    personal_information_interview_id = request.session.get('personal_information_interview_id')
    if personal_information_interview_id:
        orm = interview.objects.get(id=personal_information_interview_id)
        return render(request, 'personal_information/personal_information_interview_detail.html'
                      ,{'user':'%s%s' % (request.user.last_name,request.user.first_name),
                        'path1':'personal_information',
                        'path2':path,
                        'page_name1':u'人员信息',
                        'page_name2':u'人员基本信息表',
                        'name':orm.name,
                        'channel':orm.channel,
                        'education':orm.education,
                        'interview_times':orm.interview_times,
                        'interview_date':str(orm.interview_date).split('+')[0],
                        'reply_date':str(orm.reply_date).split('+')[0],
                        'interview_mode':orm.interview_mode,
                        'job_title':orm.job_title,
                        'job_type':orm.job_type,
                        'direction':orm.direction,
                        'invitation_success':orm.invitation_success,
                        'invitation_condition':orm.invitation_condition,
                        'interview_department':orm.interview_department,
                        'interviewer':orm.interviewer,
                        'interview_result':orm.interview_result,
                        'salary_now':orm.salary_now,
                        'except_salary':orm.except_salary,
                        'executor':orm.executor,
                        'comment':orm.comment,
                        'id':orm.id},
                      context_instance=RequestContext(request))
    return render(request, 'personal_information/personal_information_interview_detail.html',{'user':'%s%s' % (request.user.last_name,request.user.first_name),
                                                 'path1':'personal_information',
                                                 'path2':path,
                                                 'page_name1':u'人员信息',
                                                 'page_name2':u'人员基本信息表',
                                                 'name':name,
                                                 'channel':channel,
                                                 'education':education,
                                                 'job_title':job_title,
                                                 'job_type':job_type,
                                                 'direction':direction,
                                                 'interview_times':interview_times},
                                                context_instance=RequestContext(request))

