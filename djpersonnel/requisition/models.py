# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djpersonnel.core.utils import LEVEL2

from djtools.utils.users import in_group
from djtools.fields.helpers import upload_to_path
from djtools.fields import BINARY_CHOICES
from djzbar.utils.hr import departments_all_choices

SALARY_CHOICES = (
    ('Exempt', 'Exempt (salary)'),
    ('Non-exempt', 'Non-exempt (hourly)')
)


class Operation(models.Model):
    """
    Model: ...
    """
    created_by = models.ForeignKey(
        User,
        verbose_name="Created by",
        related_name='prf_operation_created_by',
        editable=settings.DEBUG
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        related_name='prf_operation_updated_by',
        editable=settings.DEBUG,
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
    level3_approver = models.ForeignKey(
        User,
        verbose_name="Level 3 Approver",
        related_name='prf_operation_approver',
        editable=settings.DEBUG,
        null=True, blank=True
    )
    level3_date = models.DateField(
        "Level 3 signed date",
        null=True, blank=True
    )
    # Vice President of Finance and Administration (VPFA)
    level2 = models.BooleanField(default=False)
    level2_date = models.DateField(
        "Level 2 signed date",
        null=True, blank=True
    )
    # HR
    level1 = models.BooleanField(default=False)
    level1_date = models.DateField(
        "Level 1 Signed Date",
        null=True, blank=True
    )
    # anyone in the workflow can decline the operation
    declined = models.BooleanField(default=False)
    # set to True when all levels are completed.
    # post_save signal sends email to...whom?
    email_approved = models.BooleanField(default=False)

    # form fields
    position_title = models.CharField(
        "Position Title",
        max_length=128,
    )
    department_name = models.CharField(
        "Department Name",
        max_length=128,
        choices=departments_all_choices()
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
    budgeted_position = models.CharField(
        "Is this a budgeted position?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    # NOTE: if 'Yes', provide the account number to charge
    account_number = models.CharField(
        "Account number",
        max_length=30,
        null=True, blank=True
    )
    salary_type = models.CharField(
        "This position is",
        max_length=16,
        choices=SALARY_CHOICES,
    )
    # NOTE: if 'Non Exempt (hourly)', provide the hours per week
    # this position will work
    hours_per_week = models.CharField(
        "How many hours per week will this position work?",
        max_length=25,
        null=True, blank=True
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
        "Open/available Date"
    )
    expected_start_date = models.DateField(
        "Expected Start Date"
    )
    publication_date = models.DateField(
        help_text=("Human Resources should publish this position "
            "by the following date")
    )
    applicant_system = models.CharField(
        """
        Would you like any others to have access to the
        applications in the Applicant Pro system?
        """,
        max_length=4,
        choices=BINARY_CHOICES,
    )
    applicant_system_people = models.TextField(
        null=True, blank=True,
        help_text="Enter each individual's name, one per line"
    )
    speciality_sites = models.CharField(
        """
        Would you like to post to a speciality site that is not part
        of the base package?
        """,
        max_length=4,
        choices=BINARY_CHOICES,
    )
    speciality_sites_urls = models.TextField(
        "URLs",
        null=True, blank=True,
        help_text=("Please provide the URL(s) of the sites to which "
            "you would like to submit this job position")
    )
    job_description = models.FileField(
        "Job Description",
        upload_to=upload_to_path,
        max_length=768,
        help_text="PDF or Word format",
        null=True, blank=True
    )

    class Meta:
        ordering  = ['-created_at']
        get_latest_by = 'created_at'

    def get_slug(self):
        return 'files/requisition/'

    def __unicode__(self):
        """
        Default data for display
        """
        return "{}: submitted by {}, {}".format(
            self.position_title, self.created_by.last_name,
            self.created_by.first_name
        )

    def permissions(self, user):
        perms = {
            'view':False,'approver':False,
            'level3': False, 'level2': False, 'level1': False
        }

        # in_group includes an exception for superusers
        group = in_group(user, settings.HR_GROUP)
        if group:
            perms['view'] = True
            perms['approver'] = True
            perms['level1'] = True
        elif user.id == LEVEL2.id:
            perms['view'] = True
            perms['approver'] = True
            perms['level2'] = True
        elif self.level3_approver == user:
            perms['view'] = True
            perms['approver'] = True
            perms['level3'] = True
        elif self.created_by == user:
            perms['view'] = True

        return perms

    @models.permalink
    def get_absolute_url(self):
        return ('requisition_display', [str(self.id)])

