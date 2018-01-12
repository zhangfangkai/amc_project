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
from django.utils import timezone



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
        print "keyi shanchu"
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
        print "keyixiugai"
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
            Order.objects.filter(id=orderid).update(status=status)
            result = "post_success"
            return HttpResponse(json.dumps(result), content_type='application/json')
        elif status == "发货":
            order = Order.objects.filter(id=orderid)
            orderdetail = Order_detail.objects.filter(order=order)
            tag = 1
            for i in orderdetail:
                kucun = i.product.stock
                shuliang = i.orderNum
                if (kucun-shuliang)<0:
                    tag = 0
                    break
            if tag == 1:
                result = 1
            else:
                result = 2
            data={}
            data['result']=result
            data['id']=orderid
            return HttpResponse(json.dumps(data), content_type='application/json')

# 销售管理-成功发货
@csrf_exempt
def sales_successfahuo(req):
    if req.method == "POST":
        order_id = req.POST.get('id')
        userid = req.session['user_id']
        order = Order.objects.get(id=order_id)
        user = User.objects.get(id = userid)
        order.update(status = "已发货",)
        deliver=Deliver.objects.create(order = order,user = user,addTime = timezone.now(),status = "已发货")
        orderdetail = order.order_detail_set.all()
        for i in orderdetail:
            stock = i.product.stock-i.orderNum
            i.product.update(stock = stock)
            DeliverDatail.objects.create(deliver = deliver,product = i.product,deliverNum = i.orderNum)
        data = {}
        data['result'] = 'post_success'
        return HttpResponse(json.dumps(data), content_type='application/json')

# 销售管理-部分发货开缺货单单
@csrf_exempt
def sales_unsuccessfahuo(req):
    if req.method == "POST":
        order_id = req.POST.get('id')
        userid = req.session['user_id']
        order = Order.objects.get(id=order_id)
        user = User.objects.get(id=userid)
        Order.objects.filter(id = order_id).update(status="部分发货")
        deliver = Deliver.objects.create(order=order, user=user, addTime=timezone.now(), status="部分发货")
        outdemand = OutDemand.objects.create(order = order,user = user,addTime = timezone.now(),status ="缺货")
        orderdetail = order.order_detail_set.all()
        for i in orderdetail:
            stock = i.product.stock - i.orderNum
            if stock>=0:
                Product.objects.filter(id=i.product.id).update(stock=stock)
                DeliverDatail.objects.create(deliver=deliver, product=i.product, deliverNum=i.orderNum)
            else:
                DeliverDatail.objects.create(deliver=deliver, product=i.product, deliverNum=i.product.stock)
                Product.objects.filter(id=i.product.id).update(stock=0)
                OutdemandDetail.objects.create(outDemand = outdemand,product = i.product,outNum = (0-stock))
        data = {}
        data['result'] = 'post_success'
        print "nihao"
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
            print i, productname, productnum
            print type(product.saleprice)
            price = product.saleprice * int(productnum)
            sumprice = sumprice + price
            order.order_detail_set.create(product=product, orderNum=productnum)
            print "keyi"
        Order.objects.filter(id = order.id).update(sumprice = sumprice)
        result = 'post_success'
        return HttpResponse(json.dumps(result), content_type='application/json')

# 销售管理-删除订单
@csrf_exempt
def sales_delorder(req):
    if req.method == "POST":
        id = req.POST.get('id')
        order = Order.objects.get(id = id)
        orderdetail = order.order_detail_set.all()
        for i in orderdetail:
            i.delete()
        order.delete()
        data = {}
        data['result'] = 'post_success'
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
        user = User.objects.get(userName=username)
        if user.userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'sales_base.html'
        data['base_template'] = base_template
        return render(req, 'sales_customermanage.html', data)
    else:
        print "111"
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
        print "keyixiugai"
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
        print "keyi shanchu"
        id = req.POST.get('id')
        user = Customer.objects.filter(id=id).user
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
        purchaseprice = req.POST.get('purchaseprice')
        salesprice = req.POST.get('salesprice')
        supplierid = req.POST.get('supplierid')
        supplier = Supplier.objects.get(id=supplierid)
        id = req.POST.get('id')
        Product.objects.filter(id=id).update(productName=productname, productSize=productsize, stock=stock, safastock=safestock,
                               purchasePrice=purchaseprice, saleprice=salesprice, supplier=supplier)
        result = 'post_success'
        return HttpResponse(json.dumps(result), content_type='application/json')


# 库存管理_产品删除
@csrf_exempt
def kucun_productdel(req):
    if req.method == 'POST':
        print "keyi shanchu"
        id = req.POST.get('id')
        Product.objects.filter(id=id)[0].delete()
        data = {}
        data['result'] = 'post_success'
        data['id'] = id
        return HttpResponse(json.dumps(data), content_type='application/json')


#库存管理-备货单管理
def kucun_beihuodanmanage(req):
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
        user = User.objects.get(userName=username)
        if user.userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'kucun_base.html'
        data['base_template'] = base_template
        return render(req, 'kucun_beihuodanmanage.html', data)

#库存管理-进货单管理
def kucun_jinhuodanguanli(req):
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
        if User.objects.get(userName=username).userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'kucun_base.html'
        data['base_template'] = base_template
        return render(req, 'kucun_jinhuodanguanli.html', data)

#库存管理-发货单管理
def kucun_fahuodanguanli(req):
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
        if User.objects.get(userName=username).userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'kucun_base.html'
        data['base_template'] = base_template
        return render(req, 'kucun_fahuodanguanli.html', data)

#mkx-缺货单
#采购管理-缺货单管理
def caigou_quehuodanguanli(req):
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
        if User.objects.get(userName=username).userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'caigou_base.html'
        data['base_template'] = base_template
        return render(req, 'caigou_quehuodanguanli.html', data)

#mkx-再订货单
#采购管理-再订货单管理
def caigou_zaidinghuodanguanli(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        zaidinghuodan = AgainpurchaseDetail.objects.all()
        zaidinghuodanlist = []

        for i in zaidinghuodan:
            zaidinghuodandetail={}
            zaidinghuodandetail['id']= i.id
            zaidinghuodandetail['pid']= Product.objects.get(id=i.product_id).id
            zaidinghuodandetail['pname'] = Product.objects.get(id=i.product_id).productName
            zaidinghuodandetail['pnum'] = i.purchaseNum
            zaidinghuodandetail['apid'] = i.againpurchase_id #通知单编号
            zaidinghuodandetail['time'] = Againpurchase.objects.get(id=i.againpurchase_id).addTime
            zaidinghuodandetail['user'] = Againpurchase.objects.get(id=i.againpurchase_id).user
            zaidinghuodandetail['state'] = Againpurchase.objects.get(id=i.againpurchase_id).status
            zaidinghuodanlist.append(zaidinghuodandetail)
        data['zaidinghuodanlist'] = zaidinghuodanlist
        data['realname'] = username
        if User.objects.get(userName=username).userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'caigou_base.html'
        data['base_template'] = base_template
        return render(req, 'caigou_zaidinghuodanguanli.html', data)

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
        Supplier.objects.create(supplierName=suppliercompany, linkMan=linkman, address=address, phone=phone, email=email, productScope=productscope,user = user)
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
        id = req.POST.get('id')
        Supplier.objects.filter(id=id).update(supplierName=suppliercompany, linkMan=linkman, address=address, phone=phone, email=email, productScope=productscope)
        result = 'post_success'
        return HttpResponse(json.dumps(result), content_type='application/json')

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
def caiwu_yingfuzhangfuanli(req):
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
        if User.objects.get(userName=username).userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'caiwu_base.html'
        data['base_template'] = base_template
        return render(req, 'caiwu_yingfuzhangfuanli.html', data)

#mkx-应收帐
#财务管理-应收账款管理
def caiwu_yingshouzhangguanli(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        yingshouzhang = Receivable.objects.all()
        yingshouzhanglist = []

        for i in yingshouzhang:
            yingshouzhangdetail={}
            yingshouzhangdetail['id']= i.id
            yingshouzhangdetail['bhid'] = Stocknotice.objects.get(id=i.stocknotice_id).id
            yingshouzhangdetail['time'] = i.addTime
            yingshouzhangdetail['status'] = i.status
            yingshouzhangdetail['total'] = i.totalAccount
            yingshouzhanglist.append(yingshouzhangdetail)
        data['yingshouzhanglist'] = yingshouzhanglist
        data['realname'] = username
        if User.objects.get(userName=username).userRole_id == 1:
            base_template = 'admin_base.html'
        else:
            base_template = 'caiwu_base.html'
        data['base_template'] = base_template
        return render(req, 'caiwu_yingshouzhangguanli.html', data)

#mkx-销售帐
#财务管理-销售账款管理
def caiwu_xiaoshouzhangguanli(req):
    if req.method == 'GET':
        username = req.session['username']
        data={}
        xiaoshouzhang = SaleAccount.objects.all()
        xiaoshouzhanglist = []

        for i in xiaoshouzhang:
            xiaoshouzhangdetail={}
            xiaoshouzhangdetail['id']= i.id
            xiaoshouzhangdetail['rcid'] = Receivable.objects.get(id=i.receivable_id).id
            xiaoshouzhangdetail['time'] = i.addTime
            xiaoshouzhangdetail['total'] = i.totalAccount
            xiaoshouzhanglist.append(xiaoshouzhangdetail)
        data['xiaoshouzhanglist'] = xiaoshouzhanglist
        data['realname'] = username
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
            caigouzhangdetail['pbid'] = Payable.objects.get(id=i.payable_id).id
            caigouzhangdetail['time'] = i.addTime
            caigouzhangdetail['total'] = i.totalAccount
            caigouzhanglist.append(caigouzhangdetail)
        data['caigouzhanglist'] = caigouzhanglist
        data['realname'] = username
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
