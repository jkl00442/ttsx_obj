from django.contrib import admin
from models import *

# Register your models here.
class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_delete']

class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['id', 'g_name', 'g_price', 'g_click', 'g_title', 'g_has', 'g_pic', 'g_unit', 'is_delete', 'g_type']

admin.site.register(TypeInfo, TypeInfoAdmin)
admin.site.register(GoodsInfo, GoodsInfoAdmin)
