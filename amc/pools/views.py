# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,render_to_response
from django.template.context import RequestContext
from models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.db.models import Sum
from django.utils import timezone
import datetime
import math



# Create your views here.

#mkx-index
def index_n(req):
    if req.method == 'GET':
        return render(req, 'index_newyear.html', {})

def index(req):
    if req.method == 'GET':
        return render(req, 'index.html', {})

@csrf_exempt
def login(req):
    if req.method == 'GET':
        return render(req, 'login.html', {})
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
            today = datetime.date.today()
            daylist = []
            conutlist = []
            purchasepricelist = []
            paylist = []
            for i in range(0, 7):
                temp = 0
                temp2 = 0
                oneday = datetime.timedelta(days=i)
                yesterday = today - oneday
                year = yesterday.year
                month = yesterday.month
                day = yesterday.day
                purprice = Purchase_account.objects.filter(addTime__year=year, addTime__month=month,
                                                           addTime__day=day).aggregate(Sum('totalAccount'))
                pay = SaleAccount.objects.filter(addTime__year=year, addTime__month=month, addTime__day=day).aggregate(
                    Sum('totalAccount'))
                count = Order.objects.filter(orderTime__year=year, orderTime__month=month, orderTime__day=day).count()
                ayesterday = yesterday.strftime("%Y-%m-%d")
                conutlist.append(count)
                if purprice.values()[0] == None:
                    temp = 0
                else:
                    temp = purprice.values()[0]
                if pay.values()[0] == None:
                    temp2 = 0
                else:
                    temp2 = pay.values()[0]
                purchasepricelist.append(temp)
                paylist.append(temp2)
                daylist.append(ayesterday)
            daylist.reverse()
            conutlist.reverse()
            paylist.reverse()
            purchasepricelist.reverse()
            data['daylist'] = daylist
            data['countlist'] = conutlist
            data['paylist'] = paylist
            data['purchasepricelist'] = purchasepricelist
            if userRoleid == 1:
                return render(req, 'admin_base.html', data)
            elif userRoleid ==2:
                return render(req, 'sales_base.html', data)
            elif userRoleid == 3:
                return render(req, 'kucun_base.html', data)
            elif userRoleid == 4:
                return render(req, 'caiwu_base.html', data)
            elif userRoleid == 5:
                return render(req, 'caigou_base.html', data)
            elif userRoleid == 6:
                return render(req, 'customer_base.html', data)
            elif userRoleid == 7:
                return render(req, 'supplier_base.html', data)
            else:
                return render(req, 'login.html', {})
        else:
            return render(req, 'login.html', {} )

#用户管理
@csrf_exempt
def admin_employeemanage(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        employee = Employee.objects.all()
        employeelist = []
        for i in employee:
            userdetail={}
            userdetail['id']= i.user.id
            userdetail['username']= i.user.userName
            userdetail['realname']= i.employName
            userdetail['depart']=i.employDepart
            userdetail['password'] = i.user.userPassword
            userdetail['userrole']=i.user.userRole.roleName
            employeelist.append(userdetail)
        data['employeelist'] = employeelist
        data['username'] = username
        return render(req, 'admin_employeemanage.html', data)
    else:
        username = req.POST.get('username')
        password = req.POST.get('password')
        realname = req.POST.get('realname')
        userdepart = req.POST.get('userdepart')
        juese = req.POST.get('juese')
        user=User.objects.create(userName=username,userPassword=password,userRole_id=juese)
        Employee.objects.create(employName = realname,employDepart = userdepart,user = user)
        result = 'post_success'
        return HttpResponse(json.dumps(result), content_type='application/json')

@csrf_exempt
def admin_userdelete(req):
    if req.method == 'POST':
        user_id = req.POST.get('userid')
        user = User.objects.filter(id=user_id)
        Employee.objects.filter(user = user ).delete()
        user.delete()
        data = {}
        data['result'] = 'post_success'
        data['id'] = user_id
        return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def admin_modify(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        realname = req.POST.get('realname')
        userdepart = req.POST.get('userdepart')
        juese = req.POST.get('juese')
        user_id = req.POST.get('userid')
        User.objects.filter(id=user_id).update(userName=username, userPassword=password,
                                               userRole_id=juese)
        Employee.objects.filter(user_id = user_id).update(employName = realname,employDepart = userdepart)
        result = 'post_success'
        return HttpResponse(json.dumps(result), content_type='application/json')

# wtq add-销售管理
#销售管理--订单管理
@csrf_exempt
def sales_ordermanage(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        data['username']=username
        sales = Order.objects.all().order_by("-orderTime")
        saleslist = []
        for i in sales:
            salesdetail={}
            salesdetail['id']= i.id
            salesdetail['user']= i.user.userName
            salesdetail['customername'] = i.customer.customerName
            salesdetail['receaddress'] = i.receAddress
            salesdetail['ordertime']= i.orderTime
            salesdetail['status'] = i.status
            saleslist.append(salesdetail)
        data['saleslist'] = saleslist
        data['realname'] = username
        customerlist=[]
        customer = Customer.objects.all()
        for j in customer:
            customerlist.append(j.customerName)
        data['customerlist']= customerlist
        product = Product.objects.all()
        productlist=[]
        for k in product:
            productlist.append(k.productName)
        data['productlist']=productlist
        user = User.objects.get(userName=username)
        if user.userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'sales_base.html'
        data['base_template'] = base_template
        return render(req, 'sales_ordermanage.html', data)
    else:
        orderid=req.POST.get('orderid')
        status = req.POST.get('status')
        if status == "已审核" or status == "已打回":
            if Order.objects.get(id=orderid).status == "待审核":
                Order.objects.filter(id=orderid).update(status=status)
                result = "post_success"
            else:
                result = "0"
            return HttpResponse(json.dumps(result), content_type='application/json')
        elif status == "发货":
            order = Order.objects.filter(id=orderid)
            orderdetail = Order_detail.objects.filter(order=order)
            tag = 1
            tag2 = 0
            for i in orderdetail:
                kucun = i.product.stock
                shuliang = i.orderNum
                if kucun!=0:
                    tag2 = 1
                if (kucun-shuliang)<0:
                    tag = 0
            if tag2 == 0:
                tag = 2
            elif tag2==1 and tag == 0:
                tag = 0
            #tag =0,部分缺货；1,不缺货；2，完全缺货
            data={}
            data['result']=tag
            data['id']=orderid
            return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def customer_ordermanage(req):
    if req.method == 'GET':
        user_id = req.session['user_id']
        username = req.session['username']
        data = {}
        data['username'] = username
        user=User.objects.get(id =user_id)
        customer = Customer.objects.get(user=user)
        sales = Order.objects.filter(customer = customer).order_by("-orderTime")
        saleslist = []
        for i in sales:
            salesdetail = {}
            salesdetail['id'] = i.id
            salesdetail['user'] = i.user.userName
            salesdetail['customername'] = i.customer.customerName
            salesdetail['receaddress'] = i.receAddress
            salesdetail['ordertime'] = i.orderTime
            salesdetail['status'] = i.status
            saleslist.append(salesdetail)
        data['saleslist'] = saleslist
        product = Product.objects.all()
        productlist = []
        for k in product:
            productlist.append(k.productName)
        data['productlist'] = productlist
        base_template = 'customer_base.html'
        data['base_template'] = base_template
        return render(req, 'customer_ordermanage.html', data)
    else:
        orderid = req.POST.get('orderid')
        status = req.POST.get('status')
        if status == "已收货" or status == "已付款":
            Order.objects.filter(id=orderid).update(status=status)
            result = "post_success"
            return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def customer_delivermanage(req):
    if req.method == 'GET':
        user_id = req.session['user_id']
        username = req.session['username']
        data = {}
        data['username'] = username
        user = User.objects.get(id=user_id)
        customer = Customer.objects.get(user=user)
        deliver = []
        deliverlist = Deliver.objects.all().order_by("-addTime")
        for j in deliverlist:
            if j.order.customer ==customer:
                deliver.append(j)
        saleslist = []
        for i in deliver:
            salesdetail = {}
            salesdetail['id'] = i.id
            salesdetail['receiver'] = i.order.receiver
            salesdetail['receaddress'] = i.order.receAddress
            salesdetail['time'] = i.addTime
            salesdetail['status'] = i.status
            saleslist.append(salesdetail)
        data['saleslist'] = saleslist
        base_template = 'customer_base.html'
        data['base_template'] = base_template
        return render(req, 'customer_delivermanage.html', data)
    else:
        orderid = req.POST.get('orderid')
        status = req.POST.get('status')
        result = '0'
        if status =="已收货":
            if Deliver.objects.get(id = orderid).status == '已发货':
                deliver = Deliver.objects.get(id = orderid)
                Deliver.objects.filter(id=orderid).update(status=status)
                receivable = Receivable.objects.create(Deliver = deliver,addTime = timezone.now(),status = "待付款",totalAccount = 0)
                deliverDatail = DeliverDatail.objects.filter(deliver=deliver).all()
                tempnum = 0
                for i in deliverDatail:
                    product = i.product
                    num = i.deliverNum
                    total = product.saleprice*num
                    ReceivableDetail.objects.create(receivable = receivable,product = product,unitPrice = product.saleprice,salsAmount = num,totalsales = total)
                    tempnum += total
                Receivable.objects.filter(id = receivable.id).update(totalAccount = tempnum)
                result = "post_success"
        elif status == "已付款":
            if Deliver.objects.get(id=orderid).status == '已收货':
                deliver = Deliver.objects.get(id = orderid)
                Deliver.objects.filter(id=orderid).update(status=status)
                receivable = Receivable.objects.get(Deliver = deliver)
                SaleAccount.objects.create(receivable = receivable,addTime = timezone.now(),totalAccount = receivable.totalAccount)
                Receivable.objects.filter(Deliver=deliver).update(status = status)
                result = "post_success"
        return HttpResponse(json.dumps(result), content_type='application/json')


# 客户-增加订单
@csrf_exempt
def customer_addorder(req):
    if req.method == "POST":
        rows = req.POST.get('rows')
        user_id = req.session['user_id']
        user = User.objects.get(id=user_id)
        customer = Customer.objects.get(user = user)
        customeraddress = req.POST.get('customeraddress')
        shouhuoname = req.POST.get('shouhuoname')
        order = customer.order_set.create(receAddress=customeraddress, receiver=shouhuoname,
                                          orderTime=timezone.now(), status="待审核", user=user, sumprice=0)
        sumprice = 0
        for i in range(0, int(rows)):
            tempproname = 'productname' + str(i)
            temppronum = 'productnum' + str(i)
            productname = req.POST.get(tempproname)
            productnum = req.POST.get(temppronum)
            product = Product.objects.filter(productName=productname)[0]
            price = product.saleprice * int(productnum)
            sumprice = sumprice + price
            order.order_detail_set.create(product=product, orderNum=productnum)
        Order.objects.filter(id=order.id).update(sumprice=sumprice)
        result = 'post_success'
        return HttpResponse(json.dumps(result), content_type='application/json')


# 销售管理-成功发货
@csrf_exempt
def sales_successfahuo(req):
    if req.method == "POST":
        order_id = req.POST.get('id')
        userid = req.session['user_id']
        order = Order.objects.get(id=order_id)
        user = User.objects.get(id = userid)
        result = '0'
        if  Order.objects.get(id = order_id).status == "已审核":
            Order.objects.filter(id = order_id).update(status = "已发货")
            deliver=Deliver.objects.create(order = order,user = user,addTime = timezone.now(),status = "已发货")
            orderdetail = order.order_detail_set.all()
            for i in orderdetail:
                stock = i.product.stock-i.orderNum
                Product.objects.filter(id = i.product.id).update(stock = stock)
                DeliverDatail.objects.create(deliver = deliver,product = i.product,deliverNum = i.orderNum)
            result = 'post_success'
        data = {}
        data['result'] = result
        return HttpResponse(json.dumps(data), content_type='application/json')

# 销售管理-部分发货开缺货单
@csrf_exempt
def sales_unsuccessfahuo(req):
    if req.method == "POST":
        order_id = req.POST.get('id')
        userid = req.session['user_id']
        order = Order.objects.get(id=order_id)
        user = User.objects.get(id=userid)
        result = '0'
        if  Order.objects.get(id = order_id).status == "已审核":
            Order.objects.filter(id = order_id).update(status="部分发货")
            deliver = Deliver.objects.create(order=order, user=user, addTime=timezone.now(), status="已发货")
            outdemand = OutDemand.objects.create(order = order,user = user,addTime = timezone.now(),status ="缺货")
            orderdetail = order.order_detail_set.all()
            for i in orderdetail:
                stock = i.product.stock
                res = i.product.stock - i.orderNum
                if stock == 0:
                    OutdemandDetail.objects.create(outDemand = outdemand,product = i.product,outNum = (0-res))
                elif res >= 0:
                    Product.objects.filter(id=i.product.id).update(stock=res)
                    DeliverDatail.objects.create(deliver=deliver, product=i.product, deliverNum=i.orderNum)
                else:
                    DeliverDatail.objects.create(deliver=deliver, product=i.product, deliverNum=i.product.stock)
                    Product.objects.filter(id=i.product.id).update(stock=0)
                    OutdemandDetail.objects.create(outDemand = outdemand,product = i.product,outNum = (0-res))
            result = 'post_success'
        data = {}
        data['result'] = result
        return HttpResponse(json.dumps(data), content_type='application/json')

# 销售管理-完全缺货开缺货单
@csrf_exempt
def sales_wqquehuo(req):
    if req.method == "POST":
        order_id = req.POST.get('id')
        userid = req.session['user_id']
        order = Order.objects.get(id=order_id)
        user = User.objects.get(id=userid)
        result = '0'
        if Order.objects.get(id=order_id).status == "已审核":
            Order.objects.filter(id=order_id).update(status="缺货")
            outdemand = OutDemand.objects.create(order=order, user=user, addTime=timezone.now(), status="缺货")
            orderdetail = order.order_detail_set.all()
            for i in orderdetail:
                OutdemandDetail.objects.create(outDemand=outdemand, product=i.product, outNum=i.orderNum)
            result =  'post_success'
        data = {}
        data['result'] = result
        return HttpResponse(json.dumps(data), content_type='application/json')


# 销售管理-增加订单
@csrf_exempt
def sales_addorder(req):
    if req.method == "POST":
        rows = req.POST.get('rows')
        user_id = req.session['user_id']
        user = User.objects.get(id=user_id)
        customername = req.POST.get('customername')
        customeraddress = req.POST.get('customeraddress')
        shouhuoname = req.POST.get('shouhuoname')
        customer = Customer.objects.get(customerName=customername)
        order = customer.order_set.create(receAddress=customeraddress, receiver=shouhuoname,
                                          orderTime=timezone.now(), status="待审核", user=user,sumprice = 0)
        sumprice = 0
        for i in range(0, int(rows)):
            tempproname = 'productname' + str(i)
            temppronum = 'productnum' + str(i)
            productname = req.POST.get(tempproname)
            productnum = req.POST.get(temppronum)
            product = Product.objects.filter(productName=productname)[0]
            price = product.saleprice * int(productnum)
            sumprice = sumprice + price
            order.order_detail_set.create(product=product, orderNum=productnum)
        Order.objects.filter(id = order.id).update(sumprice = sumprice)
        result = 'post_success'
        return HttpResponse(json.dumps(result), content_type='application/json')

# 销售管理-删除订单
@csrf_exempt
def sales_delorder(req):
    if req.method == "POST":
        id = req.POST.get('id')
        order = Order.objects.get(id = id)
        result = '0'
        data = {}
        if order.status == '待审核':
            orderdetail = order.order_detail_set.all()
            for i in orderdetail:
                i.delete()
            order.delete()
            result = 'post_success'
        data['result'] = result
        data['id'] = id
        return HttpResponse(json.dumps(data), content_type='application/json')

# 销售管理-订单详情
@csrf_exempt
def sales_orderdetail(req):
    if req.method == "POST":
        data={}
        id = req.POST.get('id')
        order = Order.objects.get(id=id)
        orderdetail = order.order_detail_set.all()
        detail= []
        for i in orderdetail:
            orderxiangxi = {}
            orderxiangxi["id"] = i.id
            orderxiangxi["name"] = i.product.productName
            orderxiangxi["num"] = i.orderNum
            detail.append(orderxiangxi)
        data["detail"] = detail
        data['result'] = 'post_success'
        return HttpResponse(json.dumps(data), content_type='application/json')


#销售管理-客户管理
@csrf_exempt
def sales_customermanage(req):
    if req.method == 'GET':
        userid = req.session['user_id']
        username = req.session['username']
        data={}
        clist = Customer.objects.all()
        customerlist = []
        for i in clist:
            customerdetail={}
            customerdetail['username']=i.user.userName
            customerdetail['password']=i.user.userPassword
            customerdetail['id']= i.id
            customerdetail['customername'] = i.customerName
            customerdetail['customeraddress'] = i.address
            customerdetail['phone']= i.phone
            customerdetail['email'] = i.email
            customerdetail['credit'] = i.credit
            customerlist.append(customerdetail)
        data['customerlist'] = customerlist
        data['username'] = username
        user = User.objects.get(id=userid)
        if user.userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'sales_base.html'
        data['base_template'] = base_template
        return render(req, 'sales_customermanage.html', data)
    else:
        customerusername = req.POST.get('customerusername')
        customerpassword = req.POST.get('customerpassword')
        user = User.objects.create(userName = customerusername, userPassword = customerpassword,userRole_id = 6)
        customername = req.POST.get('customername')
        customeraddress = req.POST.get('customeraddress')
        phone = req.POST.get('phone')
        email = req.POST.get('email')
        Customer.objects.create(customerName=customername,address=customeraddress,phone=phone,email=email,credit=100,user = user)
        result = 'post_success'
        return HttpResponse(json.dumps(result), content_type='application/json')


#销售管理-客户信息修改
@csrf_exempt
def sales_customermodify(req):
    if req.method == 'POST':
        customername = req.POST.get('customername')
        customeraddress = req.POST.get('customeraddress')
        phone = req.POST.get('phone')
        email = req.POST.get('email')
        id = req.POST.get('id')
        Customer.objects.filter(id=id).update(customerName=customername, address=customeraddress, phone=phone,email=email)
        result = 'post_success'
        return HttpResponse(json.dumps(result), content_type='application/json')

#销售管理-客户删除
@csrf_exempt
def sales_customerdel(req):
    if req.method == 'POST':
        id = req.POST.get('id')
        user = Customer.objects.filter(id=id)[0].user
        Customer.objects.filter(id=id).delete()
        user.delete()
        data = {}
        data['result'] = 'post_success'
        data['id'] = id
        return HttpResponse(json.dumps(data), content_type='application/json')


#库存管理--产品管理
@csrf_exempt
def kucun_chanpinguanli(req):
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
            productdetail['salesprice'] = i.saleprice
            productlist.append(productdetail)
        data['productlist'] = productlist
        data['username'] = username
        user = User.objects.get(userName=username)
        if user.userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'kucun_base.html'
        data['base_template'] = base_template
        return render(req, 'kucun_chanpinguanli.html', data)

    else:
        productname = req.POST.get('productname')
        productsize = req.POST.get('productsize')
        stock = int(req.POST.get('stock'))
        safestock = int(req.POST.get('safestock'))
        purchaseprice = req.POST.get('purchaseprice')
        salesprice = req.POST.get('salesprice')
        supplierid = req.POST.get('supplierid')
        supplier = Supplier.objects.get(id=supplierid)

        Product.objects.create(productName=productname, productSize=productsize, stock=stock, safastock=safestock,
                               purchasePrice=purchaseprice, saleprice=salesprice, supplier=supplier, status = 1)
        result = 'post_success'
        return HttpResponse(json.dumps(result), content_type='application/json')


# 库存管理-产品信息修改
@csrf_exempt
def kucun_productmodify(req):
    if req.method == 'POST':
        productname = req.POST.get('productname')
        productsize = req.POST.get('productsize')
        stock = int(req.POST.get('stock'))
        safestock = int(req.POST.get('safestock'))
        salesprice = req.POST.get('salesprice')
        id = req.POST.get('id')
        Product.objects.filter(id=id).update(productName=productname, productSize=productsize, stock=stock, safastock=safestock,
                                saleprice=salesprice)
        result = 'post_success'
        return HttpResponse(json.dumps(result), content_type='application/json')


# 库存管理_产品删除
@csrf_exempt
def kucun_productdel(req):
    if req.method == 'POST':
        id = req.POST.get('id')
        Product.objects.filter(id=id)[0].delete()
        data = {}
        data['result'] = 'post_success'
        data['id'] = id
        return HttpResponse(json.dumps(data), content_type='application/json')

# 库存管理-再订货通知单管理
@csrf_exempt
def kucun_againpurchasenotice(req):
    if req.method == 'GET':
        username = req.session['username']
        data = {}
        againpurchasenotice = Againpurchasenotice.objects.all()
        noticelist = []

        for i in againpurchasenotice:
            detail = {}
            detail['id'] = i.id
            detail['productname'] =i.product.productName
            detail['productsize'] = i.product.productSize
            detail['num'] = i.num
            detail['time'] = i.addTime
            detail['status'] = i.status
            noticelist.append(detail)
        data['againnotice'] = noticelist
        data['username'] = username
        if User.objects.get(userName=username).userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'kucun_base.html'
        data['base_template'] = base_template
        return render(req, 'kucun_againpurchasenotice.html', data)
    else:
        id = req.POST.get('id')
        num = req.POST.get('num')
        user_id = req.session['user_id']
        user = User.objects.get(id = user_id)
        product = Product.objects.get(id = id)
        Againpurchasenotice.objects.create(user = user, product =product, num = num, status = "未处理")
        result = 'post_success'
        return HttpResponse(json.dumps(result), content_type='application/json')

# 采购管理-再订货单删除
@csrf_exempt
def caigou_zaidinghuodandel(req):
    if req.method == 'POST':
        id = req.POST.get('id')
        result = '0'
        if Againpurchase.objects.get(id=id).status == "待发货":
            againpurchasenoticeID = Againpurchase.againpurchasenotice.id
            Againpurchasenotice.objects.filter(id = againpurchasenoticeID).update(status = '未处理')
            Againpurchase.objects.filter(id=id).delete()
            result = 'post_success'
        data = {}
        data['result'] = result
        data['id'] = id
        return HttpResponse(json.dumps(data), content_type='application/json')

# 库存管理-再订货通知单删除
@csrf_exempt
def kucun_againnoticedel(req):
    if req.method == 'POST':
        id = req.POST.get('id')
        result = "0"
        if Againpurchasenotice.objects.get(id = id).status == "未处理":
            Againpurchasenotice.objects.filter(id = id).delete()
            result = 'post_success'
        data = {}
        data['result']=result
        data['id']=id
        return HttpResponse(json.dumps(data), content_type='application/json')

#库存管理-发货单管理
@csrf_exempt
def kucun_fahuodanguanli(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        fahuodan = Deliver.objects.all().order_by('-addTime')
        fahuodanlist = []

        for i in fahuodan:
            fahuodandetail={}
            fahuodandetail['id']= i.id
            fahuodandetail['time'] = i.addTime
            fahuodandetail['status'] = i.status
            fahuodandetail['customer'] = i.order.customer.customerName
            fahuodanlist.append(fahuodandetail)
        data['fahuodanlist'] = fahuodanlist
        data['username'] = username
        if User.objects.get(userName=username).userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'kucun_base.html'
        data['base_template'] = base_template
        return render(req, 'kucun_fahuodanguanli.html', data)
    else:
        id = req.POST.get('id')
        fahuo = Deliver.objects.get(id = id)
        data={}
        data['customer'] = fahuo.order.customer.customerName
        data['receiver'] = fahuo.order.receiver
        data['address'] = fahuo.order.receAddress
        detail = DeliverDatail.objects.filter(deliver = fahuo)
        fahuodetail =[]
        for i in detail:
            prodetail = {}
            prodetail['product'] = i.product.productName
            prodetail['num'] = i.deliverNum
            fahuodetail.append(prodetail)
        data['fahuodetail'] =fahuodetail
        data['result'] = 'post_success'
        return HttpResponse(json.dumps(data), content_type='application/json')


# 库存管理-再订货单管理
@csrf_exempt
def kucun_zaidinghuodanguanli(req):
    if req.method == 'GET':
        username = req.session['username']
        data = {}
        zaidinghuodan = Againpurchase.objects.all().order_by('-addTime')
        zaidinghuodanlist = []
        for i in zaidinghuodan:
            product = i.againpurchasenotice.product
            supplier = i.supplier
            detail = {}
            detail['id'] = i.id
            detail['user'] = i.user.userName
            detail['num'] = i.againpurchasenotice.num
            detail['product'] = product.productName
            detail['supplier'] = supplier.supplierName
            detail['price'] = ProducttoSupplier.objects.filter(product=product, supplier=supplier)[0].price
            detail['status'] = i.status
            detail['time'] = i.addTime
            zaidinghuodanlist.append(detail)
        data['zaidinghuodanlist'] = zaidinghuodanlist
        data['username'] = username
        if User.objects.get(userName=username).userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'kucun_base.html'
        data['base_template'] = base_template
        return render(req, 'kucun_zaidinghuodanguanli.html', data)
    else:
        id = req.POST.get('id')
        status = req.POST.get('status')
        if status == "已收货":
            againpurchase  = Againpurchase.objects.get(id=id)
            result = '0'
            if againpurchase.status == "已发货":
                payable = Payable.objects.create(againpurchase = againpurchase, totalAccount = 0,invoiceStatus='未开', addTime =timezone.now(),status = '待付款')
                product = againpurchase.againpurchasenotice.product
                num =againpurchase.againpurchasenotice.num
                supplier = againpurchase.supplier
                unitprice = ProducttoSupplier.objects.filter(product=product,supplier = supplier)[0].price
                total = num*unitprice
                PayableDetail.objects.create(payable = payable, product = product,unitPrice = unitprice, salsAmount = num,totalsales = total)
                Againpurchase.objects.filter(id=id).update(status=status)
                Payable.objects.filter(id = payable.id).update(totalAccount = total)
                result = "post_success"
            return HttpResponse(json.dumps(result), content_type='application/json')

#采购管理-再订货通知单管理
@csrf_exempt
def caigou_againpurchasenotice(req):
    if req.method == 'GET':
        username = req.session['username']
        data = {}
        againpurchasenotice = Againpurchasenotice.objects.all().order_by("-addTime")
        noticelist = []

        for i in againpurchasenotice:
            detail = {}
            detail['id'] = i.id
            detail['productname'] = i.product.productName
            detail['productsize'] = i.product.productSize
            detail['num'] = i.num
            detail['time'] = i.addTime
            detail['status'] = i.status
            noticelist.append(detail)
        data['againnotice'] = noticelist
        data['username'] = username
        if User.objects.get(userName=username).userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'caigou_base.html'
        data['base_template'] = base_template
        return render(req, 'caigou_againpurchasenotice.html', data)
    else:
        id = req.POST.get('id')
        data = {}
        againnotice = Againpurchasenotice.objects.get(id =id)
        product = againnotice.product
        data['productname'] = product.productName
        data['productsize'] = product.productSize
        data['againnoticeid'] = id
        baojia = ProducttoSupplier.objects.filter(product = product)
        baojialist=[]
        for i in baojia:
            detail = {}
            detail['supplierid'] = i.supplier.id
            detail['supplier'] = i.supplier.supplierName
            detail['credit'] = i.supplier.credit
            detail['price'] = i.price
            baojialist.append(detail)
        data['baojialist']=baojialist
        data['result'] = 'post_success'
        return HttpResponse(json.dumps(data), content_type='application/json')

# 采购管理-再订货单管理
@csrf_exempt
def caigou_againpurchase(req):
    if req.method == 'GET':
        username = req.session['username']
        data = {}
        againpurchasenotice = Againpurchasenotice.objects.all().order_by("-addTime")
        noticelist = []

        for i in againpurchasenotice:
            detail = {}
            detail['id'] = i.id
            detail['productname'] = i.product.productName
            detail['productsize'] = i.product.productSize
            detail['num'] = i.num
            detail['time'] = i.addTime
            detail['status'] = i.status
            noticelist.append(detail)
        data['againnotice'] = noticelist
        data['username'] = username
        if User.objects.get(userName=username).userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'caigou_base.html'
        data['base_template'] = base_template
        return render(req, 'caigou_againpurchasenotice.html', data)
    else:
        user_id = req.session['user_id']
        user = User.objects.get(id = user_id)
        supplierid = req.POST.get('supplierid')
        againnoticeid = req.POST.get('againnoticeid')
        supplier = Supplier.objects.get(id = supplierid)
        againnotice = Againpurchasenotice.objects.get(id = againnoticeid)
        result = '0'
        if againnotice.status == "未处理":
            Againpurchase.objects.create(user = user, supplier = supplier, againpurchasenotice = againnotice, addTime = timezone.now(),status = "待发货")
            result = 'post_success'
            Againpurchasenotice.objects.filter(id=againnoticeid).update(status = "已处理")
        data = {}
        data['result'] = result
        return HttpResponse(json.dumps(data), content_type='application/json')


#mkx-缺货单
#采购管理-缺货单管理
@csrf_exempt
def kucun_quehuodanguanli(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        quehuodan = OutDemand.objects.all().order_by('-addTime')
        quehuodanlist = []
        for i in quehuodan:
            quehuodandetail={}
            quehuodandetail['id']= i.id
            quehuodandetail['user']= i.user.userName
            quehuodandetail['time'] =  i.addTime
            quehuodandetail['status'] = i.status
            quehuodandetail['customer'] = i.order.customer.customerName
            quehuodanlist.append(quehuodandetail)
        data['quehuodanlist'] = quehuodanlist
        data['username'] = username
        if User.objects.get(userName=username).userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'kucun_base.html'
        data['base_template'] = base_template
        return render(req, 'kucun_quehuodanguanli.html', data)
    else:
        data = {}
        id = req.POST.get('id')
        outDemand = OutDemand.objects.get(id = id)
        outdemanddetail = OutdemandDetail.objects.filter(outDemand = outDemand).all()
        outdetail = []
        for i in outdemanddetail:
            detail = {}
            detail['productname'] = i.product.productName
            detail['productsize'] = i.product.productSize
            detail['num'] = i.outNum
            outdetail.append(detail)
        data['outdetail'] = outdetail
        data['result'] = 'post_success'
        return HttpResponse(json.dumps(data), content_type='application/json')

#缺货单校验
@csrf_exempt
def kucun_quehuodancheck(req):
    if req.method == 'POST':
        id = req.POST.get('id')
        outDemand = OutDemand.objects.get(id=id)
        outdemandDetail = OutdemandDetail.objects.filter(outDemand=outDemand).all()
        tag = 1
        for i in outdemandDetail:
            kucun = i.product.stock
            shuliang = i.outNum
            if (kucun - shuliang) < 0:
                tag = 0
                break
        data = {}
        data['result'] = tag
        data['id'] = id
        return HttpResponse(json.dumps(data), content_type='application/json')

# 缺货单发货
@csrf_exempt
def kucun_quehuodanfahuo(req):
    if req.method == 'POST':
        id = req.POST.get('id')
        outDemand = OutDemand.objects.get(id=id)
        userid = req.session['user_id']
        order = outDemand.order
        result = '0'
        if outDemand.status == "缺货":
            Order.objects.filter(id=order.id).update(status="已发货")
            deliver = Deliver.objects.create(order=order, user=user, addTime=timezone.now(), status="已发货")
            outdemandDetail = OutdemandDetail.objects.filter(outDemand=outDemand).all()
            for i in outdemandDetail:
                stock = i.product.stock - i.outNum
                Product.objects.filter(id=i.product.id).update(stock=stock)
                DeliverDatail.objects.create(deliver=deliver, product=i.product, deliverNum=i.outNum)
            OutDemand.objects.filter(id=outDemand.id).update(status = "已处理")
            result = 'post_success'
        data = {}
        data['result'] = result
        return HttpResponse(json.dumps(data), content_type='application/json')

#mkx-再订货单
#采购管理-再订货单管理
def caigou_zaidinghuodanguanli(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        zaidinghuodan = Againpurchase.objects.all().order_by('-addTime')
        zaidinghuodanlist = []
        for i in zaidinghuodan:
            product = i.againpurchasenotice.product
            supplier = i.supplier
            detail={}
            detail['id']= i.id
            detail['user'] = i.user.userName
            detail['num'] = i.againpurchasenotice.num
            detail['product'] = product.productName
            detail['supplier'] = supplier.supplierName
            detail['price'] = ProducttoSupplier.objects.filter(product = product,supplier = supplier)[0].price
            detail['status'] = i.status
            detail['time'] = i.addTime
            zaidinghuodanlist.append(detail)
        data['zaidinghuodanlist'] = zaidinghuodanlist
        data['username'] = username
        if User.objects.get(userName=username).userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'caigou_base.html'
        data['base_template'] = base_template
        return render(req, 'caigou_zaidinghuodanguanli.html', data)
    else:
        id = req.POST.get('id')
        Againpurchase.objects.filter(id = id).delete()
        data={}
        data['result'] ="post_success"
        data['id'] = id
        return HttpResponse(json.dumps(data), content_type='application/json')

#采购管理-供应商管理
@csrf_exempt
def caigou_gongyingshangguanli(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        supplier = Supplier.objects.all()
        supplierlist = []
        for i in supplier:
            supplierdetail={}
            supplierdetail['id']= i.id
            supplierdetail['username'] = i.user.userName
            supplierdetail['suppliercompany']= i.supplierName
            supplierdetail['linkman'] = i.linkMan
            supplierdetail['phone']= i.phone
            supplierdetail['productscope'] = i.productScope
            supplierlist.append(supplierdetail)
        data['supplierlist'] = supplierlist
        data['username'] = username
        if User.objects.get(userName=username).userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'caigou_base.html'
        data['base_template'] = base_template
        return render(req, 'caigou_gongyingshangguanli.html', data)
    else:
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = User.objects.create(userName = username, userPassword=password, userRole_id = 7)
        suppliercompany = req.POST.get('suppliercompany')
        linkman = req.POST.get('linkman')
        address = req.POST.get('address')
        phone = req.POST.get('phone')
        email = req.POST.get('email')
        productscope = req.POST.get('productscope')
        Supplier.objects.create(supplierName=suppliercompany, credit =100, linkMan=linkman, address=address, phone=phone, email=email, productScope=productscope,user = user)
        result = 'post_success'
        return HttpResponse(json.dumps(result), content_type='application/json')


# 采购管理-供应商信息修改
@csrf_exempt
def caigou_suppliermodify(req):
    if req.method == 'POST':
        suppliercompany = req.POST.get('suppliercompany')
        linkman = req.POST.get('linkman')
        address = req.POST.get('address')
        phone = req.POST.get('phone')
        email = req.POST.get('email')
        productscope = req.POST.get('productscope')
        credit = req.POST.get('credit')

        id = req.POST.get('id')
        Supplier.objects.filter(id=id).update(supplierName=suppliercompany, linkMan=linkman, address=address, phone=phone, email=email, productScope=productscope,credit = credit)
        result = 'post_success'
        return HttpResponse(json.dumps(result), content_type='application/json')

# 采购管理-供应商信息详情
@csrf_exempt
def caigou_supplierdetail(req):
    if req.method == 'POST':
        id = req.POST.get('id')
        supplier = Supplier.objects.get(id=id)
        data = {}
        data['id'] = supplier.id
        data['supplierName'] = supplier.supplierName
        data['linkMan'] = supplier.linkMan
        data['address'] = supplier.address
        data['phone'] = supplier.phone
        data['email'] = supplier.email
        data['productScope'] = supplier.productScope
        data['credit'] = supplier.credit
        data['result'] = 'post_success'
        return HttpResponse(json.dumps(data), content_type='application/json')

# 采购管理-供应商 再订货单
@csrf_exempt
def supplier_zaidinghuo(req):
    if req.method == 'GET':
        user_id = req.session['user_id']
        username = req.session['username']
        user = User.objects.get(id = user_id)
        supplier = Supplier.objects.filter(user = user)[0]
        data = {}
        againpurchase = Againpurchase.objects.filter(supplier = supplier).all().order_by('-addTime')
        againlist = []
        for i in againpurchase:
            detail ={}
            product = i.againpurchasenotice.product
            supplier = i.supplier
            detail['id'] = i.id
            detail['user'] = i.user.userName
            detail['num'] = i.againpurchasenotice.num
            detail['product'] = product.productName
            detail['supplier'] = supplier.supplierName
            detail['price'] = ProducttoSupplier.objects.filter(product=product, supplier=supplier)[0].price
            detail['status'] = i.status
            detail['time'] = i.addTime
            againlist.append(detail)
        data['zaidinghuodanlist'] = againlist
        data['username'] = username
        data['base_template'] = 'supplier_base.html'
        return  render(req, 'supplier_zaidinghuodanguanli.html', data)
    else:
        id = req.POST.get('id')
        result = '1'
        if Againpurchase.objects.get(id = id).status =="待发货":
            Againpurchase.objects.filter(id = id).update(status = "已发货")
            result = "post_success"
        return HttpResponse(json.dumps(result), content_type='application/json')

# 供应商报价 详情
@csrf_exempt
def bjmanage(req):
    if req.method == 'GET':
        data = {}
        id = req.session['user_id']
        username = req.session['username']
        user = User.objects.get(id=id)
        if user.userRole.id ==7:
            supplier = Supplier.objects.get(user = user)
        else:
            supplier_id = req.GET.get("id")
            supplier = Supplier.objects.get(id = supplier_id)

        protopri=ProducttoSupplier.objects.filter(supplier=supplier)
        suptoprodetail = []
        for i in protopri:
            detail = {}
            detail['id'] = i.id
            detail['productname'] = i.product.productName
            detail['productsize'] = i.product.productSize
            detail['price'] = i.price
            suptoprodetail.append(detail)
        product = Product.objects.all()
        productlist = []

        for k in product:
            productlist.append(k.productName)
        data['productlist'] = productlist
        if user.userRole_id == 1:
            base_template = 'admin_base.html'
        elif user.userRole_id == 5:
            base_template = 'caigou_base.html'
        else:
            base_template = 'supplier_base.html'
        data['base_template'] = base_template
        data['protosup'] = suptoprodetail
        data['user_id']=supplier.id
        data['username'] = username
        return  render(req, 'supplier_bj.html', data)
    else:
        id = req.POST.get('id')
        supplier = Supplier.objects.get(id = id)
        productname = req.POST.get('product')
        price = float(req.POST.get('price'))
        product = Product.objects.filter(productName=productname)[0]
        ProducttoSupplier.objects.create(supplier = supplier,product=product, price=price)
        result = 'post_success'
        return HttpResponse(json.dumps(result), content_type='application/json')

# 销售管理-删除订单
@csrf_exempt
def bjdel(req):
    if req.method == "POST":
        id = req.POST.get('id')
        ProducttoSupplier.objects.get(id=id).delete()
        data={}
        data['result'] = 'post_success'
        data['id'] = id
        return HttpResponse(json.dumps(data), content_type='application/json')

# 销售管理-删除订单
@csrf_exempt
def bjmod(req):
    if req.method == "POST":
        id = req.POST.get('id')
        price=req.POST.get('price')
        ProducttoSupplier.objects.filter(id=id).update(price = price)
        data = {}
        data['result'] = 'post_success'
        return HttpResponse(json.dumps(data), content_type='application/json')

# 采购管理_供应商删除
@csrf_exempt
def caigou_supplierdel(req):
    if req.method == 'POST':
        id = req.POST.get('id')
        user = Supplier.objects.get(id=id).user
        Supplier.objects.get(id=id).delete()
        user.delete()
        data = {}
        data['result'] = 'post_success'
        data['id'] = id
        return HttpResponse(json.dumps(data), content_type='application/json')


#财务-应付账款管理
@csrf_exempt
def caiwu_yingfuzhangfuanli(req):
    if req.method == 'GET':
        username = req.session['username']
        user_id = req.session['user_id']
        data={}
        yingfuzhang = Payable.objects.all().order_by('-addTime')
        yingfuzhanglist = []
        for i in yingfuzhang:
            yingfuzhangdetail={}
            yingfuzhangdetail['id']= i.id
            yingfuzhangdetail['time'] = i.addTime
            yingfuzhangdetail['status']= i.status
            yingfuzhangdetail['supplier'] = i.againpurchase.supplier.supplierName
            yingfuzhangdetail['total'] = i.totalAccount
            yingfuzhanglist.append(yingfuzhangdetail)
        data['yingfuzhanglist'] = yingfuzhanglist
        data['username'] = username
        if User.objects.get(id = user_id).userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'caiwu_base.html'
        data['base_template'] = base_template
        return render(req, 'caiwu_yingfuzhangfuanli.html', data)
    else:
        id = req.POST.get('id')
        data = {}
        paylist = []
        pay = Payable.objects.get(id = id)
        paydetail = PayableDetail.objects.filter(payable = pay)
        for i in paydetail:
            detail = {}
            detail['product'] = i.product.productName
            detail['unitprice'] = i.unitPrice
            detail['salsAmount'] = i.salsAmount
            detail['totalsales'] = i.totalsales
            paylist.append(detail)
        data['paylist'] = paylist
        data['result'] = 'post_success'
        return HttpResponse(json.dumps(data), content_type='application/json')

#应付账款-支付
@csrf_exempt
def caiwu_zhifu(req):
    if req.method == 'POST':
        id = req.POST.get('id')
        data = {}
        paylist = []
        pay = Payable.objects.get(id=id)
        result = '0'
        if pay.status== "待付款":
            Payable.objects.filter(id = id).update(status = '已支付')
            Purchase_account.objects.create(payable = pay,addTime = timezone.now(), totalAccount = pay.totalAccount)
            result = 'post_success'
        data['result'] = result
        data['id'] = id
        return HttpResponse(json.dumps(data), content_type='application/json')


#mkx-应收帐
#财务管理-应收账款管理
@csrf_exempt
def caiwu_yingshouzhangguanli(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        yingshouzhang = Receivable.objects.all().order_by('-addTime')
        yingshouzhanglist = []
        for i in yingshouzhang:
            yingshouzhangdetail={}
            yingshouzhangdetail['id']= i.id
            yingshouzhangdetail['customer']= i.Deliver.order.customer.customerName
            yingshouzhangdetail['sum']= i.totalAccount
            yingshouzhangdetail['time'] = i.addTime
            yingshouzhangdetail['status'] = i.status
            yingshouzhanglist.append(yingshouzhangdetail)
        data['yingshouzhanglist'] = yingshouzhanglist
        data['username'] = username
        if User.objects.get(userName=username).userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'caiwu_base.html'
        data['base_template'] = base_template
        return render(req, 'caiwu_yingshouzhangguanli.html', data)
    else:
        id = req.POST.get('id')
        data = {}
        paylist = []
        pay = Receivable.objects.get(id = id)
        paydetail = ReceivableDetail.objects.filter(receivable = pay)
        for i in paydetail:
            detail = {}
            detail['product'] = i.product.productName
            detail['unitprice'] = i.unitPrice
            detail['salsAmount'] = i.salsAmount
            detail['totalsales'] = i.totalsales
            paylist.append(detail)
        data['paylist'] = paylist
        data['result'] = 'post_success'
        return HttpResponse(json.dumps(data), content_type='application/json')



#mkx-销售帐
#财务管理-销售账款管理
def caiwu_xiaoshouzhangguanli(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        xiaoshouzhang = SaleAccount.objects.all().order_by('-addTime')

        xiaoshouzhanglist = []
        for i in xiaoshouzhang:
            xiaoshouzhangdetail={}
            xiaoshouzhangdetail['id']= i.id
            xiaoshouzhangdetail['customer']= i.receivable.Deliver.order.customer.customerName
            xiaoshouzhangdetail['time'] = i.addTime
            xiaoshouzhangdetail['total'] = i.totalAccount
            xiaoshouzhanglist.append(xiaoshouzhangdetail)
        data['xiaoshouzhanglist'] = xiaoshouzhanglist
        data['username'] = username
        if User.objects.get(userName=username).userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'caiwu_base.html'
        data['base_template'] = base_template
        return render(req, 'caiwu_xiaoshouzhangguanli.html', data)

#mkx-采购帐
#财务管理-采购帐管理
def caiwu_caigouzhangguanli(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        caigouzhang = Purchase_account.objects.all()
        caigouzhanglist = []

        for i in caigouzhang:
            caigouzhangdetail={}
            caigouzhangdetail['id']= i.id
            caigouzhangdetail['supplier'] = i.payable.againpurchase.supplier.supplierName
            caigouzhangdetail['time'] = i.addTime
            caigouzhangdetail['total'] = i.totalAccount
            caigouzhanglist.append(caigouzhangdetail)
        data['caigouzhanglist'] = caigouzhanglist
        data['username'] = username
        if User.objects.get(userName=username).userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'caiwu_base.html'
        data['base_template'] = base_template
        return render(req, 'caiwu_caigouzhangguanli.html', data)

#退出锁屏
def lockscreen(req):
    data={}
    username = req.session['username']
    data['username']=username
    return render(req, 'lockscreen.html', data)

#主页
def zhuye(req):
    data = {}
    username = req.session['username']
    user_id = req.session['user_id']
    user = User.objects.get(id =user_id)
    data['username'] = username
    userRoleid = user.userRole.id
    today = datetime.date.today()
    daylist = []
    conutlist = []
    purchasepricelist = []
    paylist = []
    for i in range(0, 7):
        temp = 0
        temp2 = 0
        oneday = datetime.timedelta(days=i)
        yesterday = today - oneday
        year = yesterday.year
        month = yesterday.month
        day = yesterday.day
        purprice = Purchase_account.objects.filter(addTime__year=year, addTime__month=month,
                                                   addTime__day=day).aggregate(Sum('totalAccount'))
        pay = SaleAccount.objects.filter(addTime__year=year, addTime__month=month, addTime__day=day).aggregate(
            Sum('totalAccount'))
        count = Order.objects.filter(orderTime__year=year, orderTime__month=month, orderTime__day=day).count()
        ayesterday = yesterday.strftime("%Y-%m-%d")
        conutlist.append(count)
        if purprice.values()[0] == None:
            temp = 0
        else:
            temp = purprice.values()[0]
        if pay.values()[0] == None:
            temp2 = 0
        else:
            temp2 = pay.values()[0]
        purchasepricelist.append(temp)
        paylist.append(temp2)
        daylist.append(ayesterday)
    daylist.reverse()
    conutlist.reverse()
    paylist.reverse()
    purchasepricelist.reverse()
    data['daylist'] = daylist
    data['countlist'] = conutlist
    data['paylist'] = paylist
    data['purchasepricelist'] = purchasepricelist

    if userRoleid == 1:
        return render(req, 'admin_base.html', data)
    elif userRoleid ==2:
        return render(req, 'sales_base.html', data)
    elif userRoleid == 3:
        return render(req, 'kucun_base.html', data)
    elif userRoleid == 4:
        return render(req, 'caiwu_base.html', data)
    elif userRoleid == 5:
        return render(req, 'caigou_base.html', data)
    elif userRoleid == 6:
        return render(req, 'customer_base.html', data)
    elif userRoleid == 7:
        return render(req, 'supplier_base.html', data)
    else:
        return render(req, 'login.html', {})

#注册
def signup(req):
    if req.method == 'GET':
        return  render(req,'signup.html',{})

#eoq
@csrf_exempt
def eoq(req):
    if req.method == 'GET':
        data = {}
        username = req.session['username']
        product = Product.objects.all()
        productlist = []
        for k in product:
            productlist.append(k.productName)
        data['productlist'] = productlist
        data['username'] = username
        user = User.objects.get(userName=username)
        if user.userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'kucun_base.html'
        data['base_template'] = base_template
        return  render(req,'kucun_eoq.html',data)
    else:
        data ={}
        productname = req.POST.get('product')
        product = Product.objects.filter(productName = productname)[0]
        cost = float(req.POST.get('cost'))
        yearprice = float(req.POST.get('yearprice'))
        today = datetime.datetime.now()
        oneday = datetime.timedelta(days=30)
        yesterday = today - oneday
        order_detail = Order_detail.objects.filter(product = product)
        asum = 0
        for i in order_detail:
            if i.order.orderTime >yesterday:
                asum += i.orderNum
        sum = int((asum/30)*365)
        aeoq = math.sqrt(2*sum*cost/yearprice)
        eoq = int(aeoq)
        data['eoq'] = eoq
        data['result'] = 'post_success'
        return HttpResponse(json.dumps(data), content_type='application/json')



