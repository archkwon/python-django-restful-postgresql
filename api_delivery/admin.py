from django.contrib import admin
from django.utils.safestring import mark_safe
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django.utils.html import format_html
from api_delivery.models import DeliveryMasterModel

# Register your models here.
@admin.register(DeliveryMasterModel)
class DeliveryMasterAdmin(admin.ModelAdmin):
    list_display = ['master_seq', 'memo_code', 'order_code', 'cust_code', 'cust_name','driver_name',
                    'part_count', 'delivery_date', 'complete_date', 'delivery_state_code']

    list_display_links = ['master_seq', 'cust_name']
    list_per_page = 15
    list_filter = ['driver_name',
                   'delivery_state_code',
                   ('delivery_date', DateRangeFilter),
                   ('complete_date', DateRangeFilter) ]

    search_fields = ['memo_code','order_code','cust_code','cust_name','driver_name','delivery_date','complete_date',]
    ordering = ['-complete_date',]
    readonly_fields = ('_thumbnail',)

    def _thumbnail(self, obj):
        return format_html(u'<img src="{}"/>', obj.image_file_url)
    _thumbnail.allow_tags = True

