# -*- coding: utf-8 -*-
from django.conf import settings
from django.urls import reverse
from django.db import models, connection
from django.contrib.auth.models import User

from djpersonnel.core.utils import get_deans, get_permissions

from djtools.fields.helpers import upload_to_path
from djtools.fields import BINARY_CHOICES
#from djtools.fields.validators import MimetypeValidator
from djimix.people.departments import department, departments_all_choices

SALARY_CHOICES = (
    ('Exempt', 'Exempt (salary)'),
    ('Non-exempt', 'Non-exempt (hourly)')
)


class Operation(models.Model):
    """
    Data model for the personnel requisition form
    """
    created_by = models.ForeignKey(
        User,
        verbose_name="Created by",
        related_name='prf_operation_created_by',
        on_delete=models.CASCADE, editable=settings.DEBUG
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        related_name='prf_operation_updated_by',
        on_delete=models.CASCADE, editable=settings.DEBUG,
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

    # VP of Area or Dean
    level3 = models.BooleanField(default=False)
    level3_approver = models.ForeignKey(
        User,
        verbose_name="Level 3 Approver",
        related_name='prf_operation_approver',
        on_delete=models.CASCADE, null=True, blank=True
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
        choices=departments_all_choices(),
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
    position_grant_funded = models.CharField(
        "Is this position grant funded?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    # NOTE: if 'Yes' to grant funded, then grant amount
    grant_fund_amount = models.TextField(
        null=True, blank=True,
        help_text='Please specify grant(s) and dollar or percentage amounts'
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
        help_text="Format: 00000.00 with no comma or $ sign"
    )
    mid_salary_range = models.DecimalField(
        "Midpoint Salary Range",
        decimal_places=2,
        max_digits=16,
        help_text="Format: 00000.00 with no comma or $ sign"
    )
    max_salary_range = models.DecimalField(
        "Maximum Salary Range",
        decimal_places=2,
        max_digits=16,
        help_text="Format: 00000.00 with no comma or $ sign"
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
        Would you like to post to a specialty site that is not part
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
        #validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="""
            All submission must be accompanied by a job description.
            (PDF or Word format)
        """, null=True, blank=True
    )
    ad_copy = models.FileField(
        "Ad Copy",
        upload_to=upload_to_path,
        #validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF or Word format",
        null=True, blank=True
    )
    plan_timeline = models.TextField(
        "Recruitment Plan and Timeline",
        help_text='Please specify grant(s) and dollar or percentage amounts'
    )

    class Meta:
        ordering  = ['-created_at']
        get_latest_by = 'created_at'
        verbose_name = "Requisition"
        verbose_name_plural = "Requisitions"

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

        return get_permissions(self, user)

    def get_absolute_url(self):
        return 'https://{}{}'.format(
            settings.SERVER_URL, reverse('requisition_detail', args=(self.id,))
        )

    def notify_level2(self):
        """
        Level 2 should be notified for all PRF for now
        """
        return True

    def notify_provost(self):
        """
        Provost must be notified about submissions that are approved by a
        division dean at level 3
        """
        if self.level3_approver.id in get_deans():
            return True
        else:
            return False

    def approved(self):
        """
        is the PRF approved?
        """
        status = False
        if self.level3 and self.level2 and self.level1:
            status = True
        return status

    def department(self):
        """
        Returns the full department name based on 3 or 4 letter code
        """
        name = self.department_name
        dept = department(name)
        if dept:
            name = dept[0]
        return name
