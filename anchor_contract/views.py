# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import requests
import json



# server_name = 'http://voting-test1.hub520.com'
server_name = 'http://contract.xiaohulu.com'

@login_required
def anchor_contract_table(request):
    # flag = check_permission(u'nagios',request.user.username)
    # if flag < 1:
    #     return render(request,'public/no_passing.html')
    path = request.path.split('/')[1]
    return render(request, 'anchor_contract/anchor_contract_table.html', {'user':request.user.username,
                                                                         'path1':'anchor_contract',
                                                                         'path2':path,
                                                                         'page_name1':u'艺人合同',
                                                                         'page_name2':u'艺人合同管理'})



@login_required
def anchor_contract_data(request):
    data = json.loads(request.body)
    _type = data.get('type')
    data = {
        'client_id': 'admin',
        'type': 2,
        'pagesize': 1000000000
    }
    res = requests.post(server_name + '/contractsList', data=data)
    res = json.loads(res.text)

    if res.get('code') == '0':
        tableData_all = res['data']['list']
    else:
        return HttpResponse(json.dumps({'code': 1, 'msg': res['msg']}), content_type="application/json")

    tableData = []
    for i in tableData_all:
        if i['party_a'] == int(_type):
            tableData.append(i)

    for i in tableData:
        if i['party_a'] == 1:
            i['status'] = '未签署'
        elif i['party_a'] == 2:
            i['status'] = '已签署'
        else:
            i['status'] = ''
    return HttpResponse(json.dumps({'code':-1,'tableData':tableData}),content_type="application/json")



@login_required
def anchor_contract_view(request):
    data = json.loads(request.body)
    contract_id = data.get('contract_id')
    data = {
        'client_id': 'admin',
        'contractId': contract_id
    }
    res = requests.post(server_name + '/contractsInfo', data=data)
    res = json.loads(res.text)
    if res.get('code') == '0':
        pdf_url = res['data']['PDFUrl']
        return HttpResponse(json.dumps({'code': -2, 'pdf_url': pdf_url}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'code': 1, 'msg': '获取url失败'}), content_type="application/json")



@login_required
def anchor_contract_sign(request):
    data = json.loads(request.body)
    contract_id = data.get('contract_id')
    data = {
        'client_id': 'admin',
        'contractId': contract_id
    }
    res = requests.post(server_name + '/contractsSign', data=data)
    res = json.loads(res.text)

    if res.get('code') == '0':
        return HttpResponse(json.dumps({'code': 0, 'msg': '签署成功'}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'code': 1, 'msg': res['msg']}), content_type="application/json")