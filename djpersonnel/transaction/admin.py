from django.contrib import admin

from djpersonnel.transaction.models import Operation


class TransactionOperationAdmin(admin.ModelAdmin):
    raw_id_fields = ('created_by','updated_by','level3_approver')


admin.site.register(Operation, TransactionOperationAdmin)
