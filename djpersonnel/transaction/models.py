# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User


class Operation(models.Model):
    """
    Model: ...
    """
    created_by = models.ForeignKey(
        User,
        verbose_name="Created by",
        related_name='paf_operation_created_by',
        #editable=False
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        related_name='paf_operation_updated_by',
        #editable=False,
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "Date Updated", auto_now=True
    )

    # supervisor/chair has submitted the form and
    # the following are status levels for various approvers

    # VP of Area or Provost
    level3 = models.BooleanField(default=False)
    level3_date = models.DateField(
        "VP or Area or Provost signed date",
        null=True, blank=True
    )
    # Vice President of Finance and Administration (VPFA)
    level2 = models.BooleanField(default=False)
    level2_date = models.DateField(
        "VPFA signed date",
        null=True, blank=True
    )
    # HR
    level1 = models.BooleanField(default=False)
    level1_date = models.DateField(
        "HR Signed Date",
        null=True, blank=True
    )
    # anyone in the workflow can decline the operation
    declined = models.BooleanField(default=False)
    # set to True when levels are completed.
    # post_save signal sends email to Supervisor.
    email_approved = models.BooleanField(default=False)

    # form fields
    start_date = models.DateField("Position start date")
    title = models.CharField(
        max_length=128
    )
    comments = models.TextField(
        null=True, blank=True,
        help_text="Provide any additional comments if need be"
    )

    class Meta:
        ordering  = ['-created_at']
        get_latest_by = 'created_at'

    def __unicode__(self):
        """
        Default data for display
        """
        return "{}: submitted by {}, {}".format(
            self.title, self.created_by.last_name,self.created_by.first_name
        )

    @models.permalink
    def get_absolute_url(self):
        return ('transaction_detail', [str(self.id)])
