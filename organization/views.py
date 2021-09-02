# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import os
from wzhl_oa.settings import BASE_DIR


@login_required
def organization_main(request):
    path = request.path.split('/')[1]
    return render(request, 'organization/organization_main.html',{'user':'%s%s' % (request.user.last_name,request.user.first_name),
                                                 'path1':'organization',
                                                 'path2':path,
                                                 'page_name1':u'组织架构',
                                                 'page_name2':u'组织架构图'},
                                                context_instance=RequestContext(request))



@login_required
def organization_sub1(request):
    path = request.path.split('/')[1]
    return render(request, 'organization/organization_sub1.html',{'user':'%s%s' % (request.user.last_name,request.user.first_name),
                                                 'path1':'organization',
                                                 'path2':path,
                                                 'page_name1':u'组织架构',
                                                 'page_name2':u'基础技术中心'},
                                                context_instance=RequestContext(request))