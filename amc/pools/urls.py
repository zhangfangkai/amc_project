# -*- coding: utf-8 -*-
from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$',  login),
    url(r'^login', login),
    # url(r'^usermanage', usermanage),
    url(r'^sales_ordermanage', sales_ordermanage),
    url(r'^admin_usermanage', admin_usermanage),
    url(r'^admin_salesmanage', admin_salesmanage),
    url(r'^admin_customermanage', admin_customermanage),
    url(r'^admin_chanpinguanli', admin_chanpinguanli),
    url(r'^admin_gongyingshangguanli', admin_gongyingshangguanli),
    url(r'^admin_beihuodanmanage', admin_beihuodanmanage),
    url(r'^admin_jinhuodanguanli', admin_jinhuodanguanli),
    url(r'^admin_fahuodanguanli', admin_fahuodanguanli),
    #采购管理
    url(r'^admin_quehuodanguanli', admin_quehuodanguanli),
    url(r'^admin_zaidinghuodanguanli', admin_zaidinghuodanguanli),
 #   url(r'^admin_caigoudingdanguanli', admin_caigoudingdanguanli),
    url(r'^admin_userdelete', admin_userdelete),
    url(r'^admin_modify', admin_modify),
    #财务管理
    url(r'^admin_yingshouzhangguanli', admin_yingshouzhangguanli),
    url(r'^admin_yingfuzhangfuanli', admin_yingfuzhangfuanli),
    url(r'^admin_xiaoshouzhangguanli', admin_xiaoshouzhangguanli),
    url(r'^admin_caigouzhangguanli', admin_caigouzhangguanli),

    url(r'^lockscreen', lockscreen),

    url(r'^sales_orderzhifu', sales_orderzhifu),


]