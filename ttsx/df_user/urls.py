from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.user),
    url(r'^order/$', views.order),
    url(r'^site/$', views.site),
    url(r'^recv_info/$', views.recv_info),

    url(r'^register/$', views.register),
    url(r'^register_handle/$', views.register_handle),

    url(r'^check_name_2/$', views.check_name_2),
    url(r'^test/$', views.test),

    url(r'^login/$', views.login),
    url(r'^login_handle/$', views.login_handle),
    url(r'^logout/$', views.logout),
    url(r'^is_login/$', views.is_login),
]
