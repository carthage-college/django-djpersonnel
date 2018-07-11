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
        related_name='operation_created_by',
        editable=False
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        related_name='operation_updated_by',
        editable=False, null=True, blank=True
    )
    created_at = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "Date Updated", auto_now=True
    )

    # status

    # supervisor/chair has submitted the form for approval
    save_submit = models.BooleanField(default=False)
    # Division Dean or VP of Area
    level4 = models.BooleanField(default=False)
    # VP for Business (CFO)
    level3 = models.BooleanField(default=False)
    # HR
    level2 = models.BooleanField(default=False)
    # Payroll
    level1 = models.BooleanField(default=False)
    # anyone in the workflow can decline the operation
    decline = models.BooleanField(default=False)
    # set to True when levels are completed.
    # post_save signal sends email to Supervisor.
    email_approved = models.BooleanField(default=False)
    # no longer active but might be used later
    closed = models.BooleanField(default=False)
    # signifies that it has been reopened
    opened = models.BooleanField(default=False)

    # form fields
    start_date = models.DateField("Position tart date")
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
        return self.created_by.username

    @models.permalink
    def get_absolute_url(self):
        return ('operation_detail', [str(self.id)])
