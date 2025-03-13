from django.contrib import admin

from .models import Prodact, LastCategiry, MainCategiry



class ProdactAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    list_filter = ('category',) 
    search_fields = ('name',)

class LastCategiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_main_cat')
    list_filter = ('main_categiry',) 
    search_fields = ('name',)

    def get_main_cat(self, obj):
        return obj.main_categiry.name
    get_main_cat.short_description = 'Главная категория'

class MainCategiryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Prodact, ProdactAdmin)
admin.site.register(LastCategiry, LastCategiryAdmin)
admin.site.register(MainCategiry, MainCategiryAdmin)
