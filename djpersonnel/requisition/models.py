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
        related_name='prf_operation_created_by',
        #editable=False
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        related_name='prf_operation_updated_by',
        #editable=False,
        null=True, blank=True
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
    position_title = models.CharField(
        "Position Title",
        max_length=128
    )
    department_name = models.CharField(
        "Department Name",
        max_length=128
    )
    account_number = models.CharField(
        "Account Number",
        max_length=30
    )
    replacement_for = models.BooleanField(
        default=False
    )
    replacement_name = models.CharField(
        "If 'Replacement', please provide name",
        max_length=128,
        null=True, blank=True
    )
    new_position = models.BooleanField(
        default=False
    )
    budgeted_position = models.BooleanField(
        default=False
    )
    min_salary_range = models.DecimalField(
        "Minimum Salary Range",
        decimal_places=2,
        max_digits=16,
        help_text="List the minimum salary range for this position"
    )
    mid_salary_range = models.DecimalField(
        "Midpoint Salary Range",
        decimal_places=2,
        max_digits=16,
        help_text="List the midpoint salary range for this position"
    )
    max_salary_range = models.DecimalField(
        "Maximum Salary Range",
        decimal_places=2,
        max_digits=16,
        help_text="List the maximum salary range for this position"
    )
    position_open_date = models.DateField(
        "Position Open Date"
    )
    expected_start_date = models.DateField(
        "Expected Start Date"
    )
    hours_per_week = models.CharField(
        "Hours per Week",
        max_length=25
    )
    weekly_schedule = models.CharField(
        "Weekly Schedule for hourly positions",
        max_length=50
    )
    hiring_mgr_name = models.CharField(
        "Hiring Manager Name",
        max_length=128
    )
    hiring_mgr_date = models.DateField(
        "Hiring Manager Signed Date"
    )
    vp_provost_name = models.CharField(
        "VP/Provost Name",
        max_length=128
    )
    vp_provost_date = models.DateField(
        "VP/Provost Signed Date"
    )
    cfo_name = models.CharField(
        "CFO Name",
        max_length=128
    )
    cfo_date = models.DateField(
        "CFO Signed Date"
    )
    hr_name = models.CharField(
        "HR Name",
        max_length=128
    )
    hr_date = models.DateField(
        "HR Signed Date"
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
