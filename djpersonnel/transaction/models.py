# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djpersonnel.core.utils import get_permissions

from djtools.fields import STATE_CHOICES
from djtools.fields import BINARY_CHOICES
from djzbar.utils.hr import departments_all_choices

STATUS_CHOICES = (
    ('Full-Time', 'Full-Time'),
    ('Part-Time', 'Part-Time')
)
HIRE_CHOICES = (
    ('New Hire', 'New Hire'),
    ('Rehire', 'Rehire')
)
PAY_RATE_CHOICES = (
    ('Hourly Rate', 'Hourly Rate'),
    ('Annual Salary', 'Annual Salary')
)
SHIFT_CHOICES = (
    ('1st Shift', '1st Shift'),
    ('2nd Shift', '2nd Shift'),
    ('3rd Shift', '3rd Shift')
)
EMPLOYMENT_TYPE_CHOICES = (
    ('Adjunct', 'Adjunct'),
    ('Contract-ongoing', 'Contract-ongoing'),
    ('Contract-terminal', 'Contract-terminal'),
    ('Graduate Assistant', 'Graduate Assistant'),
    ('Limited term', 'Limited term'),
    ('TLE', 'TLE'),
    ('Tenure', 'Tenure'),
    ('Tenure-track', 'Tenure-track')
)
PROGRAM_CHOICES = (
    ('Graduate Program', 'Graduate Program'),
    ('Semester Program', 'Semester Program'),
    ('7 Week Program', '7 Week Program'),
    ('Enrichment Program', 'Enrichment Program')
)
LEAVING_REASONS_CHOICES = (
    ('Alternate opportunity elsewhere', 'Alternate opportunity elsewhere'),
    ('Job dissatisfaction', 'Job dissatisfaction'),
    ('Contract expired', 'Contract expired'),
    ('Deceased', 'Deceased'),
    ('Gross misconduct', 'Gross misconduct'),
    ('Non-renewed', 'Non-renewed'),
    ('Perusing other opportunity', 'Perusing other opportunity'),
    ('Relocation', 'Relocation'),
    ('Retirement', 'Retirement'),
    ('Other', 'Other')
)
SABBATICAL_TERM_CHOICES = (
    ('Fall', 'Fall'),
    ('Spring', 'Spring'),
    ('Fall and Spring', 'Fall and Spring')
)


class Operation(models.Model):
    """
    Data model for the personnel action form
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
    level3_approver = models.ForeignKey(
        User,
        verbose_name="Level 3 Approver",
        related_name='paf_operation_approver',
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
    # set to True when levels are completed.
    # post_save signal sends email to Supervisor.
    email_approved = models.BooleanField(default=False)

    # form fields
    # required fields in the first part of the form
    last_name = models.CharField(
        verbose_name='Last Name (Legal Name)',
        max_length=100
    )
    first_name = models.CharField(
        verbose_name='First Name (Legal Name)',
        max_length=75
    )
    middle_name = models.CharField(
        verbose_name='Middle Name',
        max_length=50,
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
        verbose_name='Email Address',
        max_length=128
    )
    supervisor_name = models.CharField(
        verbose_name='Supervisor Name',
        max_length=128
    )
    employee_type = models.CharField(
        "Employee Type",
        max_length=16,
        choices=BINARY_CHOICES,
    )
    # NOTE: the choices will bring up a set of fields to filled out
    # based on which is checked
    newhire_rehire = models.BooleanField(
        verbose_name='New Hire/Rehire',
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
    onetime_payment = models.BooleanField(
        verbose_name='Request for one-time payment',
        default=False
    )
    supervisor_change = models.BooleanField(
        verbose_name='Supervisor change',
        default=False
    )
    voluntary_termination = models.BooleanField(
        verbose_name='Termination voluntary',
        default=False
    )
    involuntary_termination = models.BooleanField(
        verbose_name='Termination involuntary',
        default=False
    )
    status_change = models.BooleanField(
        verbose_name='Status change (Full-Time/Part-Time)',
        default=False
    )
    position_change = models.BooleanField(
        verbose_name='Position/Title change',
        default=False
    )
    leave_of_absence = models.BooleanField(
        verbose_name='Leave of absence',
        default=False
    )
    sabbatical = models.BooleanField(
        verbose_name='Sabbatical',
        default=False
    )
    # NOTE: the fields that will bring up based on which is checked
    position_title = models.CharField(
        verbose_name='Position Title',
        max_length=128,
        null=True, blank=True
    )
    status_type = models.CharField(
        verbose_name='Status (Full-Time/Part-Time)',
        max_length=16,
        choices=STATUS_CHOICES,
        null=True, blank=True
    )
    hire_type = models.CharField(
        verbose_name='New Hire/Rehire',
        max_length=16,
        choices=HIRE_CHOICES,
        null=True, blank=True
    )
    pay_type = models.CharField(
        "Exempt/Non-exempt",
        max_length=16,
        choices=BINARY_CHOICES,
    )
    # NOTE: if 'Non Exempt (hourly)', provide the hours per week this position
    # will work
    hours_per_week = models.CharField(
        "Hours worked per week",
        max_length=25,
        null=True, blank=True
    )
    pay_rate = models.CharField(
        verbose_name='Pay rate/annual salary',
        max_length=16,
        choices=PAY_RATE_CHOICES,
        null=True, blank=True
    )
    expected_start_date = models.DateField(
        verbose_name='Expected Start Date'
    )
    budget_account = models.CharField(
        verbose_name='Budget Account',
        max_length=30,
        null=True, blank=True
    )
    department_name = models.CharField(
        max_length=128,
        choices=departments_all_choices(),
        null=True, blank=True,
    )
    supervise_others = models.CharField(
        "Does this position supervise others?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    standard_vacation_package = models.CharField(
        "Standard vacation package",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    # NOTE: if 'No', then how many days
    vacation_days = models.CharField(
        "How many vacation days?",
        max_length=5,
        null=True, blank=True
    )
    position_grant_funded = models.CharField(
        "Is this position grant funded?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    # NOTE: if 'Yes' to grant funded, then grant number
    grant_number = models.CharField(
        "What is the grant fund number?",
        max_length=25,
        null=True, blank=True
    )
    # NOTE: if 'Yes', to grant funded, then grant amount
    grant_amount = models.CharField(
        "What is the grant fund percentage or amount?",
        max_length=25,
        null=True, blank=True
    )
    moving_expenses = models.CharField(
        "Moving expenses (up to $3,000)?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    # NOTE: if 'Yes', how much for moving expenses
    moving_expenses_amount = models.CharField(
        "What amount for the moving expenses?",
        max_length=25,
        null=True, blank=True
    )
    startup_expenses = models.CharField(
        "Startup expenses?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    # NOTE: if 'Yes', how much for moving expenses
    startup_expenses_amount = models.CharField(
        "What amount for the startup expenses?",
        max_length=25,
        null=True, blank=True
    )
    # NOTE: if department = 'EVD', what shift
    shift = models.CharField(
        verbose_name='What shift?',
        max_length=16,
        choices=SHIFT_CHOICES,
        null=True, blank=True
    )
    other_arrangements = models.TextField(
        null=True, blank=True,
        help_text='Other special arrangements'
    )
    employment_types = models.CharField(
        "Employment Types",
        max_length=255,
        choices=EMPLOYMENT_TYPE_CHOICES,
    )
    # NOTE: if 'Contract-ongoing or Contract-terminal',
    # need the number of years in the contract
    contract_years = models.CharField(
        "Number of years",
        max_length=25,
        null=True, blank=True
    )
    # NOTE: if 'Adjunct', then they fill out the following
    music = models.CharField(
        "Music",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    # NOTE: if Music is 'Yes', then
    courses_teaching = models.TextField(
        null=True, blank=True,
        help_text='What courses are you teaching?'
    )
    number_of_credits = models.CharField(
        "What is the number of credits you are teaching?",
        max_length=25,
        null=True, blank=True
    )
    leave_of_absence_date = models.DateField(
        verbose_name='Leave of Absence date'
    )
    expected_return_date = models.DateField(
        verbose_name='Expected return date'
    )
    leave_of_absence_reason = models.CharField(
        "Reason for the leave of absence?",
        max_length=25,
        null=True, blank=True
    )
    old_department = models.CharField(
        verbose_name='Old Department',
        max_length=55,
        null=True, blank=True
    )
    new_department = models.CharField(
        verbose_name='New Department',
        max_length=55,
        null=True, blank=True
    )
    old_supervisor = models.CharField(
        verbose_name='Old Supervisor',
        max_length=100,
        null=True, blank=True
    )
    new_supervisor = models.CharField(
        verbose_name='New Supervisor',
        max_length=100,
        null=True, blank=True
    )
    last_day_date = models.DateField(
        verbose_name='Last day'
    )
    # NOTE: if 'Voluntary Termination checked', provide the unused pto payout
    voluntary_unused_pto_payout = models.CharField(
        verbose_name='Unused paid time off payout',
        max_length=5,
        null=True, blank=True
    )
    # NOTE: if 'Involuntary Termination checked', provide the unused pto payout
    involuntary_unused_pto_payout = models.CharField(
        verbose_name='Unused paid time off payout',
        max_length=5,
        null=True, blank=True
    )
    returned_property = models.CharField(
        verbose_name='Property to be returned',
        max_length=255,
        null=True, blank=True
    )
    eligible_rehire = models.CharField(
        "Eligible for rehire",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    current_compensation = models.DecimalField(
        verbose_name='Current annual salary/rate of pay',
        decimal_places=2,
        max_digits=16,
        null=True, blank=True
    )
    new_compensation = models.DecimalField(
        verbose_name='New annual salary/rate of pay',
        decimal_places=2,
        max_digits=16,
        null=True, blank=True
    )
    salary_change_reason = models.CharField(
        verbose_name='Reason for the change',
        max_length=255,
        null=True, blank=True
    )
    effective_date = models.DateField(
        verbose_name='Effective date'
    )
    temporary_interim_pay = models.CharField(
        "Temporary interim pay",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    # NOTE: if temporary_interim_pay 'Yes', provide the end date
    end_date = models.DateField(
        verbose_name='End date',
        null=True, blank=True
    )
    amount = models.DecimalField(
        verbose_name='Amount',
        decimal_places=2,
        max_digits=16,
        null=True, blank=True
    )
    amount_reason = models.CharField(
        verbose_name='Reason for the amount',
        max_length=255,
        null=True, blank=True
    )
    pay_after_date = models.DateField(
        verbose_name='Pay after this date'
    )
    department_account_number = models.CharField(
        verbose_name='Department account number',
        max_length=30,
        null=True, blank=True
    )
    grant_pay = models.CharField(
        "Grant pay",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    # NOTE: if Grant pay 'Yes' to grant account number
    grant_number = models.CharField(
        "What is the grant account number?",
        max_length=25,
        null=True, blank=True
    )
    program_types = models.CharField(
        "Program types",
        max_length=16,
        choices=PROGRAM_CHOICES,
    )
    leaving_types = models.CharField(
        "Reason for leaving",
        max_length=16,
        choices=LEAVING_REASONS_CHOICES,
    )
    sabbatical_types = models.CharField(
        "Reason for sabbatical",
        max_length=16,
        choices=SABBATICAL_TERM_CHOICES,
    )
    academic_year = models.CharField(
        "Academic year",
        max_length=4,
        null=True, blank=True
    )
    teaching_appointment = models.CharField(
        "Teaching appointment",
        max_length=6,
        choices=BINARY_CHOICES,
        null=True, blank=True
    )
    teaching_appointment_arrangements = models.TextField(
        null=True, blank=True,
        help_text='Teaching arrangements'
    )
    old_position = models.CharField(
        verbose_name='Old position/title',
        max_length=55,
        null=True, blank=True
    )
    new_position = models.CharField(
        verbose_name='New position/title',
        max_length=55,
        null=True, blank=True
    )
    additional_supervisor_role = models.CharField(
        "Additional supervisory role?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    # NOTE: if Addition Supervisory role 'Yes'
    direct_reports = models.CharField(
        verbose_name='Direct report',
        max_length=100,
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

    def get_slug(self):
        return 'files/transaction/'

    @models.permalink
    def get_absolute_url(self):
        return ('transaction_detail', [str(self.id)])

    def permissions(self, user):

        return get_permissions(self, user)
