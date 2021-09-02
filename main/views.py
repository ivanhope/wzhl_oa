# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils.log import logger
from django.contrib import auth
from django.contrib.auth.decorators import login_required

@login_required
def main(request):
    print request.session.get('vacation_can_view')
    print request.session.get('vacation_can_view_all')
    path = request.path.split('/')[1]
    return render(request,'public/index.html',{'user':'%s%s' % (request.user.last_name,request.user.first_name),
                                                   'path1':path,
                                                   'page_name1':u'主页'},context_instance=RequestContext(request))
