# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User
from djtools.fields import STATE_CHOICES
from djzbar.utils.hr import departments_all_choices

POSITION_CHOICES = (
    ('Full-Time', 'Full-Time'),
    ('Part-Time', 'Part-Time')
)


class Operation(models.Model):
    """
    Model: ...
    """
    created_by = models.ForeignKey(
        User,
        verbose_name="Created by",
        related_name='paf_operation_created_by',
        editable=False
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        related_name='paf_operation_updated_by',
        editable=False,
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
    employee_id_number = models.CharField(
        verbose_name='Employee Number',
        max_length=15
    )
    last_name = models.CharField(
        verbose_name='Last Name',
        max_length=100
    )
    first_name = models.CharField(
        verbose_name='First Name',
        max_length=75
    )
    middle_name = models.CharField(
        verbose_name='Middle Name',
        max_length=50,
        null=True, blank=True
    )
    position_start_date = models.DateField(
        verbose_name='Position start date'
    )
    position_end_date = models.DateField(
        verbose_name='Position end date',
        null=True, blank=True
    )
    home_address = models.CharField(
        verbose_name='Home address',
        max_length=128
    )
    city = models.CharField(
        verbose_name='City',
        max_length=50
    )
    state = models.CharField(
        verbose_name='State',
        max_length=2,
        choices=STATE_CHOICES
    )
    postal_code = models.CharField(
        max_length=10,
        verbose_name='Zip Code'
    )
    phone = models.CharField(
        max_length=12,
        verbose_name='Phone Number',
        help_text="Format: XXX-XXX-XXXX"
    )
    email = models.CharField(
        max_length=128,
        verbose_name='Email Address'
    )
    effective_date = models.DateField(
        verbose_name='Effective date'
    )
    newhire_rehire = models.BooleanField(
        verbose_name='New Hire or Rehire',
        default=False
    )
    onetime_payment = models.BooleanField(
        verbose_name='Request for one-time payment',
        default=False
    )
    voluntary_termination = models.BooleanField(
        verbose_name='Termination voluntary',
        default=False
    )
    # NOTE: if 'Voluntary Termination checked', provide the unused pto payout
    voluntary_unused_pto_payout = models.DecimalField(
        verbose_name='Unused paid time off payout',
        decimal_places=2,
        max_digits=16,
        null=True, blank=True
    )
    involuntary_termination = models.BooleanField(
        verbose_name='Termination involuntary',
        default=False
    )
    # NOTE: if 'Involuntary Termination checked', provide the unused pto payout
    involuntary_unused_pto_payout = models.DecimalField(
        verbose_name='Unused paid time off payout',
        decimal_places=2,
        max_digits=16,
        null=True, blank=True
    )
    position_change = models.BooleanField(
        verbose_name='Position change',
        default=False
    )
    department_change = models.BooleanField(
        verbose_name='Department change',
        default=False
    )
    compensation_change = models.BooleanField(
        verbose_name='Compensation change',
        default=False
    )
    leave_of_absence = models.BooleanField(
        verbose_name='Leave of absence',
        default=False
    )
    position_title = models.CharField(
        verbose_name='Position Title',
        max_length=128,
        null=True, blank=True
    )
    department_name = models.CharField(
        max_length=128,
        choices=departments_all_choices(),
        null=True, blank=True,
    )
    compensation = models.DecimalField(
        verbose_name='Pay Rate/Salary/One-time Payment',
        decimal_places=2,
        max_digits=16,
        null=True, blank=True
    )
    office_extension = models.CharField(
        verbose_name='Office #/Extension',
        max_length=12,
        null=True, blank=True
    )
    position_type = models.CharField(
        verbose_name='Status',
        max_length=16,
        choices=POSITION_CHOICES,
        null=True, blank=True
    )
    supervisor_name = models.CharField(
        verbose_name='Supervisor Name',
        max_length=128,
        null=True, blank=True
    )
    budget_account = models.CharField(
        verbose_name='Budget Account',
        max_length=30,
        null=True, blank=True
    )
    benefit_change_effective_date = models.DateField(
        verbose_name='Benefit change effective date',
        null=True, blank=True
    )
    supplement_life_policy_amount = models.DecimalField(
        verbose_name='Supplement Life Policy Amount',
        decimal_places=2,
        max_digits=16,
        null=True, blank=True
    )
    supplement_life_ppp_contribution = models.DecimalField(
        verbose_name='Supplement Life PPP Contribution',
        decimal_places=2,
        max_digits=16,
        null=True, blank=True
    )
    health_insurance_plan_tier = models.CharField(
        verbose_name='Health Insurance Plan and Tier',
        max_length=30,
        null=True, blank=True
    )
    cc_health_insurance_compensation_contribution = models.DecimalField(
        verbose_name='Carthage Health Insurance Compensation Contribution',
        decimal_places=2,
        max_digits=16,
        null=True, blank=True
    )
    hsa_annual_ppp_contribution = models.DecimalField(
        verbose_name='HSA Annual PPP Contribution',
        decimal_places=2,
        max_digits=16,
        null=True, blank=True
    )
    hsa_carthage_contribution = models.DecimalField(
        verbose_name='HSA Carthage Contribution',
        decimal_places=2,
        max_digits=16,
        null=True, blank=True
    )
    fsa_medical_annual_ppp_contribution = models.DecimalField(
        verbose_name='FSA Medical Annual PPP Contribution',
        decimal_places=2,
        max_digits=16,
        null=True, blank=True
    )
    fsa_dependent_care_annual_ppp_contribution = models.DecimalField(
        verbose_name='FSA Dependent Care Annual PPP Contribution',
        decimal_places=2,
        max_digits=16,
        null=True, blank=True
    )
    comments = models.TextField(
        null=True, blank=True,
        help_text='Provide any additional comments if need be'
    )

    class Meta:
        ordering  = ['-created_at']
        get_latest_by = 'created_at'

    def __unicode__(self):
        """
        Default data for display
        """
        return "{}: submitted by {}, {}".format(
            self.position_title, self.created_by.last_name,
            self.created_by.first_name
        )

    @models.permalink
    def get_absolute_url(self):
        return ('transaction_display', [str(self.id)])
