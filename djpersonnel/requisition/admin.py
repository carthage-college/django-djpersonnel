from django.contrib import admin

from djpersonnel.requisition.models import Operation


class RequisitionOperationAdmin(admin.ModelAdmin):
    raw_id_fields = ('created_by','updated_by','level3_approver')
    list_display = ('position_title', 'department_name')
    list_max_show_all = 500
    list_per_page = 500
    search_fields = ['department_name']
    save_on_top = True


admin.site.register(Operation, RequisitionOperationAdmin)
