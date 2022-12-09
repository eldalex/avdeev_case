from django.contrib import admin
from .models import StatusCard, OperationCard, CardBaseTable, CardHistoryUse

# Register your models here.

admin.site.register(StatusCard)
admin.site.register(OperationCard)
admin.site.register(CardBaseTable)
admin.site.register(CardHistoryUse)
