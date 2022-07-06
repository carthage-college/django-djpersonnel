# -*- coding: utf-8 -*-

from django.conf import settings
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from djpersonnel.core.utils import get_permissions
from djtools.fields.helpers import upload_to_path


VARY_CHOICES = (
    ('Transfer to or from', 'Transfer to or from'),
    ('Increase to budget', 'Increase to budget'),
    ('Decrease to budget', 'Decrease to budget'),
    ('Elimination', 'Elimination'),
    ('New budget request', 'New budget request'),
)
CHANGE_TYPE = (
    ('Labor', 'Labor'),
    ('Non-labor', 'Non-labor'),
    ('Revenue', 'Revenue'),
    ('Capital', 'Capital'),
)
GIFT_CHOICES = (
    ('Gift #', 'Gift #'),
    ('$ or %', '$ or %'),
)
GRANT_CHOICES = (
    ('Grant #', 'Grant #'),
    ('$ or %', '$ or %'),
)
PROJECT_CHOICES = (
    ('Capital', 'Capital'),
    ('Non-capital', 'Non-capital'),
    ('New', 'New'),
    ('Unknown', 'Unknown'),
)


class Account(models.Model):
    """Data model for the ledger accounts."""

    name = models.CharField(max_length=32)
    code = models.CharField(max_length=16)

    class Meta:
        """Sub-class for settings about the parent class."""

        db_table = 'finance_account'
        ordering  = ['name']
        verbose_name_plural = "Ledger Accounts"

    def __str__(self):
        """Default data for display."""
        return "{0} ({1})".format(self.name, self.code)

class CostCenter(models.Model):
    """Data model for the Cost Centers."""

    officer = models.ForeignKey(
        User,
        verbose_name="Budget Officer",
        related_name='budget_officer',
        on_delete=models.CASCADE,
        editable=settings.DEBUG,
    )
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=16)
    fund_name = models.CharField(max_length=32)
    fund_code = models.CharField(max_length=16)
    program_name = models.CharField(max_length=32)
    program_code = models.CharField(max_length=16)
    account = models.ForeignKey(
        Account,
        verbose_name="Ledger Account",
        related_name='ledger_account',
        on_delete=models.CASCADE,
        editable=settings.DEBUG,
    )

    class Meta:
        """Sub-class for settings about the parent class."""

        db_table = 'finance_cost_center'
        ordering  = ['name']
        verbose_name_plural = "Cost Centers"

    def __str__(self):
        """Default data for display."""
        return "{0} ({1}): {2}, {3}".format(
            self.name,
            self.code,
            self.officer.last_name,
            self.officer.first_name,
        )


class Budget(models.Model):
    """Data model for the budget form."""

    # meta
    created_by = models.ForeignKey(
        User,
        verbose_name="Created by",
        related_name='budget_created_by',
        on_delete=models.CASCADE,
        editable=settings.DEBUG,
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        related_name='budget_updated_by',
        on_delete=models.CASCADE,
        editable=settings.DEBUG,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField("Date Created", auto_now_add=True)
    updated_at = models.DateTimeField("Date Updated", auto_now=True)
    approved = models.BooleanField(default=False)
    approved_date = models.DateField(null=True, blank=True)
    # approver etc
    cost_center = models.ForeignKey(
        CostCenter,
        related_name='cost_center',
        on_delete=models.CASCADE,
    )
    # form fields
    version = models.CharField(
        max_length=128,
        help_text="""
            Proposed up until May 15th or Modified Budget up until July 1st,
            (versions in Adaptive will be 1.0 or 2.0)
        """,
    )
    variation = models.CharField(
        max_length=128,
        choices=VARY_CHOICES,
        help_text='What sort of update is being requested?',
    )
    # If transfer indicate % allocation by Account and
    # to/from Account
    #
    # if allocation includes movement from or to a Gift
    # or Grant use the Gift and Grant fields below.
    transfer_to = models.ForeignKey(
        Account,
        verbose_name="Transfer to account",
        related_name='transfer_to',
        on_delete=models.CASCADE,
        editable=settings.DEBUG,
    )
    transfer_to_percent = models.IntegerField(
        "Transfer to account percent",
        null=True,
        blank=True,
        default=0,
        help_text="A number from 1 to 99, do not include % symbol.",
    )
    transfer_from = models.ForeignKey(
        Account,
        verbose_name="Transfer from account",
        related_name='transfer_from',
        on_delete=models.CASCADE,
        editable=settings.DEBUG,
    )
    transfer_from_percent = models.IntegerField(
        "Transfer from account percent",
        null=True,
        blank=True,
        default=0,
        help_text="A number from 1 to 99, do not include % symbol.",
    )
    allocation =  models.CharField(
        max_length=32,
        help_text="""
            If allocation includes movement from or to a Gift
            or Grant you should use the Gift and Grant fields below.
        """,
    )
    change_type = models.CharField(
        "Type of Budget change",
        max_length=32,
        choices=CHANGE_TYPE,
        help_text="""
            If more than one type of budget request please submit a separate form
            for each change.
        """,
    )
    amount = models.IntegerField(
        help_text="""
            Note that a Project number may be needed if on-going
            related purchases are expected.
        """,
    )
    # If the request is for over 5000.00 please trigger the
    # following questions and automatically add Vince Ceja to approval.
    userful_life = models.IntegerField(
        "Useful life of the item in years",
        null=True,
        blank=True,
        default=0,
        help_text="What is the useful life of the item?",
    )
    nature_purchase = models.TextField(
        "What is the nature of the purchase?",
        help_text="""
            Is it new equipment, machinery, land, plant, buildings
            or warehouses, furniture and fixtures, business vehicles,
            software, or intangible assets such as a patent or license?
            NOTE: Only the 8XXX series accounts should be utilized
            for Capital updates. Please contact Kathy Bretl for all
            capital questions.
        """,
    )
    gift = models.CharField(
        max_length=128,
        choices=GIFT_CHOICES,
    )
    grant = models.CharField(
        max_length=128,
        choices=GRANT_CHOICES,
    )
    project = models.CharField(
        max_length=128,
        choices=PROJECT_CHOICES,
    )
    phile = models.FileField(
        "Attachments",
        upload_to=upload_to_path,
        max_length=768,
        null=True,
        blank=True,
    )
    comments = models.TextField(
        "Reasons for this request",
        help_text="Please provide any information that supports this request.",
    )

    class Meta:
        """Sub-class for settings about the parent class."""

        db_table = 'finance_budget'
        ordering  = ['-created_at']
        get_latest_by = 'created_at'
        verbose_name_plural = "Budget"

    def get_slug(self):
        """Slug for file uploads."""
        return 'files/budget/'

    def __str__(self):
        """Default data for display."""
        return "{0}: submitted by {1}, {2}".format(
            self.position_title,
            self.created_by.last_name,
            self.created_by.first_name,
        )

    def permissions(self, user):
        """Return user permissions for the object."""
        return get_permissions(self, user)

    def get_absolute_url(self):
        """Return the default URL of the detailed view."""
        return 'https://{0}{1}'.format(
            settings.SERVER_URL,
            reverse('budget_detail', args=(self.id,)),
        )
