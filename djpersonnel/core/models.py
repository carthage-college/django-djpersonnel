# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from djpersonnel.requisition.models import Operation as Requisition
from djpersonnel.transaction.models import Operation as Transaction


class Approver(models.Model):
    """
    Folks who approve a personnel requisition or action form
    """
    user = models.ForeignKey(
        User,
        related_name='approver_user'
    )
    requisition = models.ForeignKey(
        Requisition,
        related_name='requisition_approver',
        null=True,blank=True
    )
    transaction = models.ForeignKey(
        Transaction,
        related_name='transaction_approver',
        null=True,blank=True
    )

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

    def title(self):
        if self.requisition:
            title = self.requisition.position_title
        elif self.transaction:
            title = self.transacttion.position_title
        else:
            title = None
        return title
