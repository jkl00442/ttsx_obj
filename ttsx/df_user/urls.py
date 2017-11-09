from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register/$', views.register),
    url(r'^register.html/$', views.register),
    url(r'^register_handle/$', views.register_handle),

    url(r'^check_name_2/$', views.check_name_2),
    url(r'^test/$', views.test),

    url(r'^login/$', views.login),
    url(r'^login_handle/$', views.login_handle),


    # url(r'^user_center_info/$', views.user_center_info),
    # url(r'^user_center_order/$', views.user_center_order),
    # url(r'^user_center_site/$', views.user_center_site),
]
