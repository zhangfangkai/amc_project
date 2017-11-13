# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,render_to_response
from django.template.context import RequestContext
from models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json


# Create your views here.
def usermanage(req):
    user_id = req.session['user_id']
    username = req.session['realname']
    data={}
    user = User.objects.all()
    userlist = []
    for i in user:
        userdetail={}
        user_id = i.id
        userdetail['id']= i.id
        userdetail['username']= i.userName
        userdetail['realname']= i.realName
        userdetail['depart']=i.userDepart
        userrole = Userrole.objects.get(id=i.userRole_id).roleName
        userdetail['userrole']=userrole
        userlist.append(userdetail)
    data['userlist'] = userlist
    data['realname'] = username
    return render(req, 'usermanage.html', data)

@csrf_exempt
def login(req):
    if req.method == 'GET':
        return render(req, 'signin.html', {})
    else:
        username = req.POST.get('name')
        password = req.POST.get('password')
        if User.objects.filter(userName=username, userPassword=password).count() > 0:
            user_id = User.objects.get(userName=username).id
            realname = User.objects.get(id=user_id).realName
            req.session['user_id'] = user_id
            req.session['realname'] = realname
            data = {}
            try:
                data['realname'] = realname
            except Exception, e:
                print e
            return render(req, 'index.html', data)
        else:
            return render(req, 'signin.html', {} )

#----一般的request和response写法
# def mainpage(req):
#     data = {}
#     try:
#         user_id = req.session['user_id']
#         user = User.objects.get(pk=user_id)
#         data['user_name'] = user.user_name
#         wenjuanlist = []
#         for i in Wenjuan.objects.filter(user_id=user_id).all():
#             wj={}
#             wj['id']=i.id
#             wjcishu=Record.objects.filter(wenjuan_id=i.id).all()
#             wj['wjtime']=i.wj_date
#             wj['count']=wjcishu.count()
#             wj['name']=i.wj_name
#             wenjuanlist.append(wj)
#         data['wenjuanlist'] = wenjuanlist
#     except Exception, e:
#         print e
#     return render_to_response('mainpage1.html', data, RequestContext(req))
#----request和response写法示例完毕


