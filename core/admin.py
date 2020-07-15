from django.contrib import admin

from .models import (
    Item,
    OrderItem,
    Order,
    Payment,
    Coupon,
    Refund,
    Address,
    UserProfile,
    Slotitem,
    Checktime,
    History
)


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'stripe_charge_id',
                    'braintree_charge_id',
                    'amount',
                    'timestamp',
                    ]

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'user',
                    'get_cleared_hot',
                    'ordered',
                    'ordered_date',
                    'status',
                    'get_purchased_items',
                    'billing_address',
                    'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'status',
                   'ordered_date',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'id',
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]

    def get_cleared_hot(self, obj):
        return obj.user.cleared_hot
    get_cleared_hot.boolean = True
    get_cleared_hot.short_description = 'Cleared Hot'
    get_cleared_hot.admin_order_field = 'user__cleared_hot'

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'get_title',
                    'quantity',
                    'kind',
                    'ordered',
                    'username',
                    'launch_code',
                    'order_id',
                    'ordered_date'
                    ]
    
    list_filter = ['ordered']

    def get_email(self, obj):
        return obj.user.email
    
    def order_id(self, obj):
        return obj.orders.all()[0].id
    
    def ordered_date(self, obj):
        return obj.orders.all()[0].ordered_date
    
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']

class HistoryAdmin(admin.ModelAdmin):
    list_display = [
        'start_date',
        'user',
        'user_id',
        'action',
        'reason',
        'order_str',
        'item_str',
    ]
    list_display_links = [
        'user',
    ]
    list_filter = ['user']
    search_fields = ['order_str']

    def user_id(self, obj):
        if obj.user:
            return obj.user.id
        else:
            return 0

admin.site.register(Item)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
admin.site.register(Slotitem)
admin.site.register(Checktime)
