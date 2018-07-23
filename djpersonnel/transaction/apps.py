# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class TransactionConfig(AppConfig):
    name = 'djpersonnel.transaction'
    verbose_name = "Personnel Transaction"

    def ready(self):
        import djpersonnel.transaction.signals
