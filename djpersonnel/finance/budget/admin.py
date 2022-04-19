# -*- coding: utf-8 -*-

from django.contrib import admin
from djpersonnel.finance.budget.models import Budget


class BudgetAdmin(admin.ModelAdmin):
    """Admin model for the budget data model."""

    raw_id_fields = ('created_by', 'updated_by', 'approver')


admin.site.register(Budget, BudgetAdmin)
