from django.db.models import Count
from django.contrib import admin, messages
from django.urls import reverse

from tags.models import TaggedItem
from . models import Customer, Collection, Product, Promotion, Order, OrderItem
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html, urlencode
from django.contrib.contenttypes.admin import GenericTabularInline
# Register your models here.
class CustomerAdmin(ImportExportModelAdmin):
    list_display = ["first_name", "last_name", "membership", "order_count"]
    list_per_page = 10
    list_editable = ['membership']
    ordering = ["first_name", "last_name"]
    search_fields = ['first_name__startswith', "last_name__startswith"]

    @admin.display(ordering='order_count')
    def order_count(self, Customer):
        url = (reverse('admin:store_order_changelist') + '?' + urlencode({
            'customer__id': str(Customer.id)
        }))
        return format_html('<a href="{}">{}</a>', url ,Customer.order_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_count = Count('order')
        )



class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lte=10)


class TagInline(GenericTabularInline):
    model = TaggedItem

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    autocomplete_fields = ['Collection']
    prepopulated_fields = {'slug': ('title', ) }
    actions = ['clear_inventory']
    # inlines = [TagInline]
    list_display = ['title', 'unit_price', 'Collection', 'inventory_status']
    list_editable = ['unit_price']
    search_fields = ['title']
    list_per_page = 10
    list_filter = ['Collection', "last_update", InventoryFilter]

    @admin.display(ordering='inventory')
    def inventory_status(self, Product):
        if Product.inventory < 10:
            return 'LOW'
        return 'OK'
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} Products were successfully updated.',
            messages.ERROR
        )

@admin.register(Collection)
class CollectionAdmin(ImportExportModelAdmin):
    list_display = ['title', 'products_count']
    search_fields =['title']
    
    @admin.display(ordering='products_count')
    def products_count(self, Collection):
        url = (reverse('admin:store_product_changelist') + '?' + urlencode({
            'Collection__id': str(Collection.id)
        }))
        return format_html('<a href="{}">{}</a>', url ,Collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count = Count('products')
        )

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 10
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['customer']
    
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Promotion)
   