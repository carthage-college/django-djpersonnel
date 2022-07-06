# -*- coding: utf-8 -*-

from django.contrib import admin
from djpersonnel.finance.budget.models import Account
from djpersonnel.finance.budget.models import Budget
from djpersonnel.finance.budget.models import CostCenter


class AccountAdmin(admin.ModelAdmin):
    """Admin model for the ledger account data model."""


class BudgetAdmin(admin.ModelAdmin):
    """Admin model for the budget data model."""

    raw_id_fields = ('created_by', 'updated_by')


class CostCenterAdmin(admin.ModelAdmin):
    """Admin model for the cost center data model."""

    raw_id_fields = ('officer',)


admin.site.register(Account, AccountAdmin)
admin.site.register(Budget, BudgetAdmin)
admin.site.register(CostCenter, CostCenterAdmin)
