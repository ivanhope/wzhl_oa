# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.utils.log import logger
from django.contrib import auth
from vacation.models import user_table
import datetime
from wzhl_oa.settings import BossName,department_BossName

import simplejson
from django.contrib.auth.decorators import login_required


def login(request):
    return render_to_response('login/login.html')

def login_auth(request):
    user_auth = request.POST.get('username')
    passwd_auth = request.POST.get('password')
    authed = auth.authenticate(username=user_auth,password=passwd_auth)
    if authed and authed.is_active:
        auth.login(request,authed)

        for perm in ['vacation.can_view','assets.can_view','KPI.can_view','personal_information.can_view',
                     'contract.can_view_all','contract.can_view_anchor_contract','order_form.can_upload_menu',
                     'seal.can_view_all']:
            if request.user.has_perm(perm):
                request.session['_'.join(perm.split('.'))] = 1
            else:
                request.session['_'.join(perm.split('.'))] = 0

        # if globals().has_key('next_next') and not next_next == None:
        #     logger.info('<%s> login in sucess.' % user_auth)
        #     return HttpResponseRedirect(next_next)
        # else:
        #     logger.info('<%s> login in sucess.' % user_auth)
        #     return HttpResponseRedirect('/main/')
        next_page = request.session.get('next')
        if next_page:
            request.session.pop('next')
            return HttpResponseRedirect(next_page)
        else:
            _user_detail = user_table.objects.filter(name=request.user.first_name)
            user_name = ""
            department = ""
            join_date = ""
            other_str = ""
            d_sub = ""
            birthday_date_str = ""
            for i in _user_detail:
                user_name = i.name
                department = i.department
                join_date = i.join_date
                d_sub = i.department_sub
                birthday_date_str = i.birthday_date
                join_date = datetime.datetime.strftime(join_date, '%Y???%m???%d???')
            positive_day = (_user_detail[0].positive_date - datetime.datetime.now().date()).days

            name_str = u"?????????%s???" % user_name
            showlsit = []
            if positive_day == 0:
                showlsit.append(u"??????????????????????????????????????????????????????????????????")
            elif positive_day>0 and positive_day <= 15:
                showlsit.append(u"????????? %s ??????????????????????????????????????????????????????" % positive_day)
            elif positive_day == 100:
                showlsit.append(u"????????????100?????????????????????????????????????????????")
            join_day_str =_user_detail[0].join_date.strftime("%m-%d")
            torday_day_str =datetime.datetime.now().strftime("%m-%d")
            join_year = _user_detail[0].join_date.year
            torday_year = datetime.datetime.now().year
            if join_day_str == torday_day_str and torday_year-join_year > 0:
                showlsit.append(u"??????????????????%s????????????????????????????????????????????????????????????" % (torday_year-join_year))


            #??????
            if birthday_date_str:
                # mon = birthday_date_str.split('???')
                # birthday_mon = mon[0]
                # birthday_day = mon[1].split('???')[0]
                # torday_day = datetime.datetime.now().day
                # torday_mon = datetime.datetime.now().month
                # if int(birthday_mon) == torday_mon and int(birthday_day) == torday_day:
                birthday_date_str = u'%s???%s' % (datetime.datetime.now().year, birthday_date_str)
                birthday_date_d = datetime.datetime.strptime(birthday_date_str, '%Y???%m???%d???').date()
                torday_date_d = datetime.datetime.now().date()
                birthday_sp_day = (birthday_date_d - torday_date_d).days
                if birthday_sp_day == 0:
                    showlsit.append(u"?????????????????????????????????????????????")
                elif birthday_sp_day > 0 and birthday_sp_day < 4:
                    showlsit.append(u"%s????????????????????????????????????????????????" % birthday_sp_day)
            show_str = ""
            if showlsit:
                show_str = name_str + u'|'.join(showlsit)

            isBoss = 0
            if user_name in BossName:
                isBoss = 1
            isdepartment_BossName = 0
            if user_name in department_BossName:
                isdepartment_BossName = 1

            return render_to_response('login/login.html', {'code': 0, 'msg': u'????????????'
                , 'user_name': user_name, 'department': department, 'join_date': join_date,
                                                           'd_sub':d_sub, 'other_str': show_str,'isBoss': isBoss,'isdepartment_BossName':isdepartment_BossName})
            # HttpResponse(simplejson.dumps({'code': 0, 'msg': '????????????','data':user_dic}), content_type="application/json")
    else:
        logger.warn('<%s> login in fail.' % user_auth)
        return render_to_response('login/login.html', {'code': 1, 'msg':u'?????????????????????'})

def logout(request):
    auth.logout(request)
    return render_to_response('login/login.html')

def not_login(request):
    next_next = request.GET.get('next')
    # print next_next
    # global next_next
    request.session['next'] = next_next
    return render_to_response('login/login.html',{'msg':u'??????????????????'})

def test_notify(request):
    offline = request.POST.get('mod_offline_post')
    to = request.POST.get('to')
    test_from = request.POST.get('from')
    body = request.POST.get('body')
    access_token = request.POST.get('access_token')
    print offline,to,test_from,body,access_token
    return HttpResponse('ok')
