from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$',  login),
    url(r'^login', login),
<<<<<<< HEAD
    url(r'^usermanage', usermanage),
    url(r'^salesmanage', salesmanage),
=======
    url(r'^admin_usermanage', admin_usermanage),
    url(r'^admin_userdelete', admin_userdelete),
    url(r'^admin_modify', admin_modify),
    url(r'^lockscreen', lockscreen),
>>>>>>> e1dda9a1e066c13d3b0a98492db9533f35421f70
]