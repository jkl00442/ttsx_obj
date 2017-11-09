from django.db import models

# Create your models here.
class UserInfo(models.Model):
    u_name = models.CharField(max_length=20)
    u_pwd = models.CharField(max_length=40)
    u_phone = models.CharField(max_length=11)


    u_get = models.CharField(max_length=20)
    u_address = models.CharField(max_length=100)
    u_zip = models.CharField(max_length=6)
    u_email = models.CharField(max_length=40)
    u_delete = models.BooleanField(default=False)

# class UserAddress(models.Model):
#     u_get = models.CharField(max_length=20)
#     u_address = models.CharField(max_length=100)
#     u_zip = models.CharField(max_length=6)
#     u_email = models.CharField(max_length=40)
#
#     u_info = models.ForeignKey(UserInfo)


class UserInfo_2(models.Model):

    u_name = models.CharField(max_length=20)
    u_pwd = models.CharField(max_length=40)
    u_phone = models.CharField(max_length=11)
    u_delete = models.BooleanField(default=False)

class UserAddress_2(models.Model):

    u_get = models.CharField(max_length=20)
    u_address = models.CharField(max_length=100)
    u_zip = models.CharField(max_length=6)
    u_email = models.CharField(max_length=40)

    u_info = models.ForeignKey(UserInfo_2)
