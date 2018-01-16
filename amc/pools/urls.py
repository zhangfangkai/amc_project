# -*- coding: utf-8 -*-
from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', index_n),
    url(r'^index_n', index_n),
    url(r'^index', index),
    url(r'^login', login),
#用户管理
    url(r'^admin_employeemanage', admin_employeemanage),
    url(r'^admin_userdelete', admin_userdelete),
    url(r'^admin_modify', admin_modify),
#销售管理
    url(r'^sales_customermanage', sales_customermanage),
    url(r'^sales_ordermanage', sales_ordermanage),
    url(r'^sales_customerdel',sales_customerdel),
    url(r'^sales_customermodify', sales_customermodify),
    url(r'^sales_successfahuo', sales_successfahuo),
    url(r'^sales_unsuccessfahuo', sales_unsuccessfahuo),
    url(r'^sales_wqquehuo', sales_wqquehuo),

    url(r'^sales_addorder', sales_addorder),
    url(r'^sales_delorder', sales_delorder),
    url(r'^sales_orderdetail', sales_orderdetail),

    #库存管理
    url(r'^kucun_chanpinguanli', kucun_chanpinguanli),
    url(r'^kucun_fahuodanguanli', kucun_fahuodanguanli),
    url(r'^kucun_productdel', kucun_productdel),
    url(r'^kucun_productmodify', kucun_productmodify),
    url(r'^kucun_againpurchasenotice', kucun_againpurchasenotice),
    url(r'^kucun_againnoticedel', kucun_againnoticedel),
    url(r'^kucun_zaidinghuodanguanli', kucun_zaidinghuodanguanli),
    url(r'^kucun_quehuodanguanli', kucun_quehuodanguanli),
    url(r'^kucun_quehuodancheck', kucun_quehuodancheck),
    url(r'^kucun_quehuodanfahuo', kucun_quehuodanfahuo),

    #采购管理
    url(r'^caigou_gongyingshangguanli', caigou_gongyingshangguanli),
    url(r'^caigou_zaidinghuodanguanli', caigou_zaidinghuodanguanli),
    url(r'^caigou_zaidinghuodandel', caigou_zaidinghuodandel),

    url(r'^caigou_suppliermodify', caigou_suppliermodify),
    url(r'^caigou_supplierdel', caigou_supplierdel),
    url(r'^caigou_supplierdetail', caigou_supplierdetail),
    url(r'^caigou_againpurchasenotice', caigou_againpurchasenotice),
    url(r'^caigou_againpurchase', caigou_againpurchase),


    #供应商
    url(r'^supplier_zaidinghuo', supplier_zaidinghuo),
    url(r'^bjmanage', bjmanage),
    url(r'^bjdel', bjdel),
    url(r'^bjmod', bjmod),
    #客户
    url(r'^customer_ordermanage', customer_ordermanage),
    url(r'^customer_addorder', customer_addorder),
    url(r'^customer_delivermanage', customer_delivermanage),

    #财务管理
    url(r'^caiwu_yingshouzhangguanli', caiwu_yingshouzhangguanli),
    url(r'^caiwu_yingfuzhangfuanli', caiwu_yingfuzhangfuanli),
    url(r'^caiwu_xiaoshouzhangguanli', caiwu_xiaoshouzhangguanli),
    url(r'^caiwu_caigouzhangguanli', caiwu_caigouzhangguanli),
    url(r'^caiwu_zhifu', caiwu_zhifu),

    #锁屏
    url(r'^lockscreen', lockscreen),
    url(r'^zhuye', zhuye),
    url(r'^signup', signup),
    url(r'^eoq', eoq),

]