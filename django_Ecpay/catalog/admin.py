from django.contrib import admin

# Register your models here.

from .models import Item

#admin.site.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'item_id', 'item_price', 'item_amount')

admin.site.register(Item,ItemAdmin)