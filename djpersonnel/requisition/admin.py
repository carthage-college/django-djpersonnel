from django.contrib import admin

from djpersonnel.requisition.models import Operation


class RequisitionOperationAdmin(admin.ModelAdmin):
    raw_id_fields = ('created_by','updated_by','approver')

admin.site.register(Operation, RequisitionOperationAdmin)
