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
    url(r'^admin_userdelete', admin_userdelete),
    url(r'^admin_modify', admin_modify),
    url(r'^lockscreen', lockscreen),
    url(r'^sales_orderzhifu', sales_orderzhifu),
]