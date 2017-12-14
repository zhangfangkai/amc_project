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
                return render(req, 'sales_base.html', data)
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


@csrf_exempt
def admin_usermanage(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        user = User.objects.all()
        userlist = []
        for i in user:
            userdetail={}
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
        return HttpResponse(json.dumps(data), content_type='application/json')

def admin_salesmanage(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        sales = Order.objects.all()
        saleslist = []
        for i in sales:
            salesdetail={}
            salesdetail['id']= i.id
            salesdetail['user']= i.user.realName
            salesdetail['customername'] = i.customer.customerName
            salesdetail['receaddress'] = i.receAddress
            salesdetail['ordertime']= i.orderTime
            salesdetail['status'] = i.status
            saleslist.append(salesdetail)
        data['saleslist'] = saleslist
        data['realname'] = username
        return render(req, 'admin_salesmanage.html', data)

def admin_customermanage(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        clist = Customer.objects.all()
        customerlist = []
        for i in clist:
            customerdetail={}
            customerdetail['id']= i.id
            customerdetail['customername'] = i.customerName
            customerdetail['customeraddress'] = i.address
            customerdetail['phone']= i.phone
            customerdetail['email'] = i.email
            customerdetail['credit'] = i.credit
            customerlist.append(customerdetail)
        data['customerlist'] = customerlist
        #data['realname'] = username
        return render(req, 'admin_customermanage.html', data)

def admin_chanpinguanli(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        product = Product.objects.all()
        productlist = []
        for i in product:
            productdetail={}
            productdetail['id']= i.id
            productdetail['productname']= i.productName
            productdetail['productsize'] = i.productSize
            productdetail['stock'] = i.stock
            productdetail['safestock']= i.safastock
            productdetail['purchaseprice'] = i.purchasePrice
            productdetail['salesprice'] = i.saleprice
            productdetail['supplierid'] = i.supplier

            productlist.append(productdetail)
        data['productlist'] = productlist
        data['realname'] = username
        return render(req, 'admin_chanpinguanli.html', data)


def admin_beihuodanmanage(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        beihuodan = StocknoticeDetail.objects.all()
        beihuodanlist = []

        for i in beihuodan:
            beihuodandetail={}
            beihuodandetail['id']= i.id
            beihuodandetail['pid']= Product.objects.get(id=i.product_id).id
            beihuodandetail['productname'] = Product.objects.get(id=i.product_id).productName
            beihuodandetail['number'] = i.stocknoticeNum
            beihuodandetail['oid']= Stocknotice.objects.get(id=i.stocknotice_id).id
            beihuodandetail['time'] = Stocknotice.objects.get(id=i.stocknotice_id).addTime
            beihuodandetail['state'] = Stocknotice.objects.get(id=i.stocknotice_id).status
            beihuodanlist.append(beihuodandetail)
        data['beihuodanlist'] = beihuodanlist
        data['realname'] = username
        return render(req, 'admin_beihuodanmanage.html', data)


def admin_jinhuodanguanli(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        jinhuodan = PurchaseDatail.objects.all()
        jinhuodanlist = []

        for i in jinhuodan:
            jinhuodandetail={}
            jinhuodandetail['id']= i.id
            jinhuodandetail['pid']= Product.objects.get(id=i.product_id).id
            jinhuodandetail['productname'] = Product.objects.get(id=i.product_id).productName
            jinhuodandetail['number'] = i.purchaseNum
            jinhuodandetail['time'] = Purchase.objects.get(id=i.purchase_id).addTime
            jinhuodandetail['state'] = Purchase.objects.get(id=i.purchase_id).status
            jinhuodanlist.append(jinhuodandetail)
        data['jinhuodanlist'] = jinhuodanlist
        data['realname'] = username
        return render(req, 'admin_jinhuodanguanli.html', data)


def admin_fahuodanguanli(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        fahuodan = DeliverDatail.objects.all()
        fahuodanlist = []

        for i in fahuodan:
            fahuodandetail={}
            fahuodandetail['id']= i.id
            fahuodandetail['oid'] = Order.objects.get(id=i.deliver_id).id
            fahuodandetail['pid']= Product.objects.get(id=i.product_id).id
            fahuodandetail['productname'] = Product.objects.get(id=i.product_id).productName
            fahuodandetail['number'] = i.deliverNum
            fahuodandetail['time'] = Deliver.objects.get(id=i.deliver_id).addTime
            fahuodandetail['state'] = Deliver.objects.get(id=i.deliver_id).status
            fahuodanlist.append(fahuodandetail)
        data['fahuodanlist'] = fahuodanlist
        data['realname'] = username
        return render(req, 'admin_fahuodanguanli.html', data)


def admin_quehuodanguanli(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        quehuodan = OutdemandDetail.objects.all()
        quehuodanlist = []

        for i in quehuodan:
            quehuodandetail={}
            quehuodandetail['id']= i.id
            quehuodandetail['pid']= Product.objects.get(id=i.product_id).id
            quehuodandetail['pname'] = Product.objects.get(id=i.product_id).productName
            quehuodandetail['qnum'] = i.outNum
            quehuodandetail['oid'] = OutDemand.objects.get(id=i.outDemand_id).order_id
            quehuodandetail['time'] = OutDemand.objects.get(id=i.outDemand_id).addTime
            quehuodandetail['user'] = OutDemand.objects.get(id=i.outDemand_id).user
            quehuodandetail['state'] = OutDemand.objects.get(id=i.outDemand_id).status
            quehuodanlist.append(quehuodandetail)
        data['quehuodanlist'] = quehuodanlist
        data['realname'] = username
        return render(req, 'admin_quehuodanguanli.html', data)

def admin_gongyingshangguanli(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        supplier = Supplier.objects.all()
        supplierlist = []
        for i in supplier:
            supplierdetail={}
            supplierdetail['id']= i.id
            supplierdetail['suppliercompany']= i.supplierName
            supplierdetail['linkman'] = i.linkMan
            supplierdetail['address'] = i.address
            supplierdetail['phone']= i.phone
            supplierdetail['email'] = i.email
            supplierlist.append(supplierdetail)
        data['supplierlist'] = supplierlist
        data['realname'] = username
        return render(req, 'admin_gongyingshangguanli.html', data)

def admin_yingfuzhangfuanli(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        yingfuzhang = Payable.objects.all()
        yingfuzhanglist = []

        for i in yingfuzhang:
            yingfuzhangdetail={}
            yingfuzhangdetail['id']= i.id
            yingfuzhangdetail['cgid'] = Purchase.objects.get(id=i.purchase_id).id
            yingfuzhangdetail['time'] = i.addTime
            yingfuzhangdetail['paystatus']= i.status
            yingfuzhangdetail['invoicestatus'] = i.invoiceStatus
            yingfuzhangdetail['total'] = i.totalAccount
            yingfuzhanglist.append(yingfuzhangdetail)
        data['yingfuzhanglist'] = yingfuzhanglist
        data['realname'] = username
        return render(req, 'admin_yingfuzhangfuanli.html', data)


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

#wtq add-销售管理
def sales_ordermanage(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        sales = Order.objects.all()
        saleslist = []
        for i in sales:
            salesdetail={}
            salesdetail['id']= i.id
            salesdetail['user']= i.user.realName
            salesdetail['customername'] = i.customer.customerName
            salesdetail['receaddress'] = i.receAddress
            salesdetail['ordertime']= i.orderTime
            salesdetail['status'] = i.status
            saleslist.append(salesdetail)
        data['saleslist'] = saleslist
        data['realname'] = username
        return render(req, 'sales_ordermanage.html', data)

@csrf_exempt
def sales_orderzhifu(req):
    if req.method == 'POST':
        print "keyi shanchu"
        order_id = req.POST.get('orderid')
        Order.objects.filter(id=order_id).update(status='已支付')
        data = {}
        data['result'] = 'post_success';
        return HttpResponse(json.dumps(data), content_type='application/json')

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


