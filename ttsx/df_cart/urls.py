from django.conf.urls import url
import views

urlpatterns = [
    # url(r'^list/$', views.list),
    # url(r'^detail/$', views.detail),
    url(r'^add_cart/$', views.add_cart),
    url(r'^show_count/$', views.show_count),
    url(r'^$', views.index),
    url(r'^edit/$', views.edit),
    url(r'^delete_cart/$', views.delete_cart),
    url(r'^order/$', views.order),
]
