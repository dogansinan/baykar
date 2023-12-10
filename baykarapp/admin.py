from django.contrib import admin
from .models import *

class KategoriAdmin(admin.ModelAdmin):
    list_display = ( 'isim' ,'slug',)
    readonly_fields = ('slug',)

class Ihadmin(admin.ModelAdmin):
    list_display = ( 'isim' ,'slug',)
    readonly_fields = ('slug',)


admin.site.register(Kategori,KategoriAdmin)
admin.site.register(Iha,Ihadmin)
admin.site.register(Profil)
admin.site.register(Kiralama)
