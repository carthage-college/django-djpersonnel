# -*- coding: utf-8 -*-

from django.contrib import admin
from djpersonnel.transaction.models import Operation


class TransactionOperationAdmin(admin.ModelAdmin):
    """Admin model for the PAF data model."""

    raw_id_fields = ('created_by', 'updated_by', 'level3_approver')
    list_display = ('last_name', 'first_name', 'created_by')
    list_max_show_all = 500
    list_per_page = 500
    search_fields = ['last_name']

admin.site.register(Operation, TransactionOperationAdmin)
