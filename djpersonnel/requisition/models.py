# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User
from djtools.fields import BINARY_CHOICES

SALARY_CHOICES = (
    ('Exempt', 'Exempt (Salary)'),
    ('Non-exempt', 'Non-exempt (Hourly)')
)

class Operation(models.Model):
    """
    Model: ...
    """
    created_by = models.ForeignKey(
        User,
        verbose_name="Created by",
        related_name='prf_operation_created_by',
        editable=False
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        related_name='prf_operation_updated_by',
        editable=False,
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
    # VP
    level3 = models.BooleanField(default=False)
    level3_date = models.DateField(
        "VP Signed Date",
        null=True, blank=True
    )
    # VP for Business (CFO)
    level2 = models.BooleanField(default=False)
    level2_date = models.DateField(
        "CFO Signed Date",
        null=True, blank=True
    )
    # HR
    level1 = models.BooleanField(default=False)
    level1_date = models.DateField(
        "HR Signed Date",
        null=True, blank=True
    )
    # anyone in the workflow can decline the operation
    decline = models.BooleanField(default=False)
    # set to True when levels are completed.
    # post_save signal sends email to Supervisor.
    email_approved = models.BooleanField(default=False)

    # form fields
    position_title = models.CharField(
        "Position Title",
        max_length=128,
    )
    department_name = models.CharField(
        "Department Name",
        max_length=128,
    )
    new_position = models.CharField(
        "Is this a new position?",
        max_length=4,
        choices=BINARY_CHOICES,
        null=True, blank=True
    )
    # NOTE: if 'No', provide the replacement name
    replacement_name = models.CharField(
        "If 'Replacement', please provide name",
        max_length=128,
        null=True, blank=True
    )
    salary_type = models.CharField(
        max_length=16,
        choices=SALARY_CHOICES,
    )
    budgeted_position = models.CharField(
        "Is this a new position?",
        max_length=4,
        choices=BINARY_CHOICES,
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
    post_position_by_date = models.DateField(
        "Human Resources to post this position by"
    )
    applicant_system = models.CharField(
        """
        Would you like any others to have access to the
        applications in the Applicant Pro system?
        """,
        max_length=4, default='No',
        choices=BINARY_CHOICES,
    )
    applicant_system_people = models.TextField(
        null=True, blank=True,
        help_text="""
            The following individuals need to have access to the applications
            in Applicant Pro system
        """
    )
    speciality_sites = models.CharField(
        """
        I would like to post to a speciality site that is not part
        of the base package.
        """,
        max_length=4, default='No',
        choices=BINARY_CHOICES,
    )
    speciality_sites_urls = models.TextField(
        "URLs",
        null=True, blank=True,
        help_text="""
            Please provide the URL(s) of the sites to which you would like
            to submit this job position
        """
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
