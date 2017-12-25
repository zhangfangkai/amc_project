# -*- coding: utf-8 -*-
from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$',  index),
    url(r'^login', login),
#用户管理
    url(r'^admin_usermanage', admin_usermanage),
#销售管理
    url(r'^sales_customermanage', sales_customermanage),
    url(r'^sales_ordermanage', sales_ordermanage),
#库存管理
    url(r'^kucun_beihuodanmanage', kucun_beihuodanmanage),
    url(r'^kucun_chanpinguanli', kucun_chanpinguanli),
    url(r'^kucun_fahuodanguanli', kucun_fahuodanguanli),
    url(r'^kucun_jinhuodanguanli', kucun_jinhuodanguanli),
#采购管理
    url(r'^caigou_gongyingshangguanli', caigou_gongyingshangguanli),
    url(r'^caigou_quehuodanguanli', caigou_quehuodanguanli),
    url(r'^caigou_zaidinghuodanguanli', caigou_zaidinghuodanguanli),
    # url(r'^caigou_caigoudingdanguanli', caigou_caigoudingdanguanli),
#财务管理
    url(r'^caiwu_yingshouzhangguanli', caiwu_yingshouzhangguanli),
    url(r'^caiwu_yingfuzhangfuanli', caiwu_yingfuzhangfuanli),
    url(r'^caiwu_xiaoshouzhangguanli', caiwu_xiaoshouzhangguanli),
    url(r'^caiwu_caigouzhangguanli', caiwu_caigouzhangguanli),


    url(r'^lockscreen', lockscreen),
    url(r'^sales_orderzhifu', sales_orderzhifu),
    url(r'^admin_userdelete', admin_userdelete),
    url(r'^admin_modify', admin_modify),
]