# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
#用户角色表
class Userrole(models.Model):
    roleName = models.CharField(max_length=30)
    roleDes = models.CharField(max_length=100)
#用户表
class User(models.Model):
    userName = models.CharField(max_length=30)
    realName = models.CharField(max_length=30)
    userPassword = models.CharField(max_length=20, blank=True)
    userRole = models.ForeignKey(Userrole, on_delete=models.CASCADE)
    userDepart = models.CharField(max_length=30)
#供应商表
class Supplier(models.Model):
    supplierName = models.CharField(max_length=50)
    linkMan = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    productScope = models.CharField(max_length=30)
#顾客表
class Customer(models.Model):
    customerName = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
#订单表
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orderTime = models.DateTimeField(auto_now=True)
    receiver = models.CharField(max_length=30)
    receAddress = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    outDemandTimes = models.IntegerField()
# 产品表
class Product(models.Model):
    productName = models.CharField(max_length=50)
    productSize = models.CharField(max_length=20)
    stock = models.IntegerField()
    safastock = models.IntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    purchasePrice = models.FloatField()
    saleprice = models.FloatField()
#订单明细表
class Order_detail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    orderNum = models.IntegerField()

#再订货单表
class Againpurchase(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    addTime = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20)
#再订货单明细
class AgainpurchaseDetail(models.Model):
    againpurchase = models.ForeignKey(Againpurchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchaseNum = models.IntegerField()
#备货通知单
class Stocknotice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    addTime = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20)
#备货通知单明细
class StocknoticeDetail(models.Model):
    stocknotice = models.ForeignKey(Stocknotice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stocknoticeNum = models.IntegerField()
#进货通知单
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    addTime = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20)
# 进货通知单明细
class PurchaseDatail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchaseNum = models.IntegerField()
# 应付账款表
class Payable(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    totalAccount = models.FloatField()
    invoiceStatus = models.CharField(max_length=20)
    addTime = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20)
# 应付账款明细表
class PayableDetail(models.Model):
    payable = models.ForeignKey(Payable, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    productName = models.CharField(max_length=50)
    unitPrice = models.FloatField()
    salsAmount = models.IntegerField()
    totalsales = models.FloatField()
# 应收账款表
class Receivable(models.Model):
    stocknotice = models.ForeignKey(Stocknotice, on_delete=models.CASCADE)
    totalAccount = models.FloatField()
    addTime = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20)
# 应收账款明细表
class ReceivableDetail(models.Model):
    receivable = models.ForeignKey(Receivable, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    productName = models.CharField(max_length=50)
    unitPrice = models.FloatField()
    salsAmount = models.IntegerField()
    totalsales = models.FloatField()
# 缺货通知单表
class OutDemand(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    addTime = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20)
# 缺货通知单明细表
class OutdemandDetail(models.Model):
    outDemand = models.ForeignKey(OutDemand, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    outNum = models.IntegerField()
# 采购业务帐
class Purchase_account(models.Model):
    payable = models.ForeignKey(Payable, on_delete=models.CASCADE)
    addTime = models.DateTimeField(auto_now=True)
    totalAccount = models.FloatField()
# 销售业务帐
class SaleAccount(models.Model):
    receivable = models.ForeignKey(Receivable, on_delete=models.CASCADE)
    addTime = models.DateTimeField(auto_now=True)
    totalAccount = models.FloatField()







