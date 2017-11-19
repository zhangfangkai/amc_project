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

@csrf_exempt
def login(req):
    if req.method == 'GET':
        return render(req, 'signin.html', {})
    else:
        username = req.POST.get('name')
        password = req.POST.get('password')
        if User.objects.filter(userName=username, userPassword=password).count() > 0:
            user = User.objects.get(userName=username)
            user_id = user.id
            userRoleid = user.userRole_id
            req.session['user_id'] = user_id
            req.session['username'] = username
            data = {}
            data['username'] = username
            if userRoleid == 1:
                return render(req, 'admin_base.html', data)
            elif userRoleid ==2:
                return render(req, 'xiaoshou_base.html', data)
            elif userRoleid == 3:
                return render(req, 'cangchu_base.html', data)
            elif userRoleid == 4:
                return render(req, 'caiwu_base.html', data)
            elif userRoleid == 5:
                return render(req, 'caigou_base.html', data)
            else:
                return render(req, 'signin.html', {})
        else:
            return render(req, 'signin.html', {} )

<<<<<<< HEAD
def salesmanage(req):
    print"aaaaaaaaaaaaaaaa"
    user_id = req.session['user_id']
    username = req.session['realname']
    data={}
    sales = Order.objects.all()
    saleslist = []
    print"bbbbbbbbbbbbbbb"
    for i in sales:
        salesdetail={}
        sales_id = i.id
        salesdetail['id']= i.id#订单编号
        salesdetail['user']= i.user#添加人员
        salesdetail['customername'] = Customer.objects.get(id=i.Customer_id).customerName#顾客姓名
        salesdetail['receaddress'] = i.receAddress  #收货地址
        salesdetail['ordertime']= i.orderTime#下单时间
        salesdetail['status'] = i.status  #订单状态
        #userrole = Userrole.objects.get(id=i.userRole_id).roleName
        #userdetail['userrole']=userrole
        saleslist.append(salesdetail)
    data['saleslist'] = saleslist
    data['realname'] = username
    print"ccccccccccccc"
    return render(req, 'salesmanage.html', data)
    print"ddddddddddddd"
=======
@csrf_exempt
def admin_usermanage(req):
    if req.method == 'GET':
        user_id = req.session['user_id']
        username = req.session['username']
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
            userdetail['password'] = i.userPassword
            userrole = Userrole.objects.get(id=i.userRole_id).roleName
            userdetail['userrole']=userrole
            userlist.append(userdetail)
        data['userlist'] = userlist
        data['username'] = username
        return render(req, 'admin_usermanage.html', data)
    else:
        print "keyile"
        username = req.POST.get('username')
        password = req.POST.get('password')
        realname = req.POST.get('realname')
        userdepart = req.POST.get('userdepart')
        juese = req.POST.get('juese')
        User.objects.create(userName=username,userPassword=password,realName=realname,userDepart=userdepart,userRole_id=juese)
        print "keyile2"
        data ={}
        data['id'] = User.objects.get(userName = username).id
        data['username'] = username;
        data['realname'] = realname;
        data['userdepart'] = userdepart;
        data['juese'] = juese;
        data['result'] = 'post_success';
        # username = req.POST.get('')
        return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def admin_userdelete(req):
    if req.method == 'POST':
        print "keyi shanchu"
        user_id = req.POST.get('userid')
        User.objects.filter(id=user_id).delete()
        data = {}
        data['result'] = 'post_success';
        data['id'] = user_id
        return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def admin_modify(req):
    if req.method == 'POST':
        print "keyixiugai"
        username = req.POST.get('username')
        password = req.POST.get('password')
        realname = req.POST.get('realname')
        userdepart = req.POST.get('userdepart')
        juese = req.POST.get('juese')
        user_id = req.POST.get('userid')
        User.objects.filter(id=user_id).update(userName=username,userPassword=password,realName=realname,userDepart=userdepart,userRole_id=juese)
        data = {}
        data['result'] = 'post_success';
        return HttpResponse(json.dumps(data), content_type='application/json')

def lockscreen(req):
    data={}
    username = req.session['username']
    data['username']=username
    return render(req, 'lockscreen.html', data)
>>>>>>> e1dda9a1e066c13d3b0a98492db9533f35421f70


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


