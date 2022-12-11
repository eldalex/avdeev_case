from django.contrib import admin
from .models import StatusCard, OperationCard, CardBaseTable, CardHistoryUse

# Register your models here.

class HistoryCard(admin.StackedInline):
    model = CardHistoryUse
    fields = ('card_id','card_operation','card_operation_detail',)
    readonly_fields = ('card_id','card_operation','card_operation_detail',)
    extra = 0

class CardBaseTableAdmin(admin.ModelAdmin):
    list_display=('card_series','card_number','card_create_date','card_end_date','card_last_use','card_amount','card_status',)
    list_display_links = ('card_series', 'card_number',)
    list_filter = ('card_status',)
    inlines = [HistoryCard, ]

class CardHistoryUseAdmin(admin.ModelAdmin):
    list_display = ('card_id', 'card_operation', 'card_operation_detail',)
    list_display_links = ('card_id', 'card_operation', 'card_operation_detail',)
    readonly_fields = ('card_id', 'card_operation', 'card_operation_detail',)
    list_filter = ('card_operation',)

admin.site.register(StatusCard)
admin.site.register(OperationCard)
admin.site.register(CardBaseTable,CardBaseTableAdmin)
admin.site.register(CardHistoryUse,CardHistoryUseAdmin)
