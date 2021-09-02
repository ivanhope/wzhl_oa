# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import os
from wzhl_oa.settings import BASE_DIR


@login_required
def used_form(request):
    print(BASE_DIR , '++++++++++++')
    hr_forms_bd = os.listdir(BASE_DIR + '/media/used_form/hr/bd')
    hr_forms_zd = os.listdir(BASE_DIR + '/media/used_form/hr/zd')
    fn_forms_bd = os.listdir(BASE_DIR + '/media/used_form/fn/bd')
    fn_forms_zd = os.listdir(BASE_DIR + '/media/used_form/fn/zd')
    path = request.path.split('/')[1]
    return render(request, 'used_form/used_form.html',{'user':'%s%s' % (request.user.last_name,request.user.first_name),
                                                 'path1':'form',
                                                 'path2':path,
                                                 'page_name1':u'常用表单',
                                                 'page_name2':u'常用表单',
                                                 'hr_forms_bd':hr_forms_bd,
                                                 'hr_forms_zd':hr_forms_zd,
                                                 'fn_forms_bd':fn_forms_bd,
                                                 'fn_forms_zd':fn_forms_zd},
                                                context_instance=RequestContext(request))