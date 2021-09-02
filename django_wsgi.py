#!/usr/bin/python

import os,sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'wzhl_oa.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
