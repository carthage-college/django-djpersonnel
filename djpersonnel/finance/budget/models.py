# -*- coding: utf-8 -*-

from django.conf import settings
from django.dispatch import receiver
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from djtools.fields.helpers import upload_to_path
from djtools.utils.mail import send_mail
from djtools.utils.users import in_group
from djpersonnel.core.utils import LEVEL2


VARY_CHOICES = (
    ('Transfer to or from', 'Transfer to or from'),
    ('Increase to budget', 'Increase to budget'),
    ('Decrease to budget', 'Decrease to budget'),
)
CHANGE_TYPE = (
    ('Labor', 'Labor'),
    ('Non-labor', 'Non-labor'),
    ('Revenue', 'Revenue'),
    ('Capital', 'Capital'),
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


class Operation(models.Model):
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
    # cost center officer
    level1 = models.BooleanField(default=False)
    level1_date = models.DateField(null=True, blank=True)
    # CFO
    level2 = models.BooleanField(default=False)
    level2_date = models.DateField(null=True, blank=True)
    declined = models.BooleanField(default=False)
    declined_date = models.DateField(null=True, blank=True)
    # status of notification email
    status_email = models.BooleanField(default=False)
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
    change_type = models.CharField(
        "Type of Budget change",
        max_length=32,
        choices=CHANGE_TYPE,
        help_text="""
            If more than one type of budget request please submit a separate form
            for each change.
        """,
    )
    variation = models.CharField(
        max_length=128,
        choices=VARY_CHOICES,
        help_text='What sort of update is being requested?',
    )
    variation_change = models.ForeignKey(
        Account,
        verbose_name="Increase or decrease account",
        related_name='variation_change',
        on_delete=models.CASCADE,
        editable=settings.DEBUG,
        help_text="""
            If increasing budget please be certain to provide either an offsetting
            decrease to an existing budget expense/category or an increase to
            revenue/category and to note this information within the Allocation field.
        """,
        null=True,
        blank=True,
    )
    variation_to = models.ForeignKey(
        Account,
        verbose_name="Transfer to account",
        related_name='transfer_to',
        on_delete=models.CASCADE,
        editable=settings.DEBUG,
        null=True,
        blank=True,
    )
    variation_from = models.ForeignKey(
        Account,
        verbose_name="Transfer from account",
        related_name='transfer_from',
        on_delete=models.CASCADE,
        editable=settings.DEBUG,
        null=True,
        blank=True,
    )
    allocation =  models.TextField(
        max_length=32,
        help_text="""
            Please provide the following: expense and/or revenue by account,
            cost center and % in order to allocate the $ amount.
            If increasing budget please provide the % decrease by expense/category
            or % increase by revenue/category.
            If allocation includes movement from or to a Gift
            or Grant you should use the Gift and Grant fields below.
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
    useful_life = models.IntegerField(
        "Useful life of the item in years",
        null=True,
        blank=True,
        default=0,
        help_text="""
            Useful life is only utilized for Capital expenditures.
            Please contact Kathy Bretl with all Capital questions.
        """,
    )
    gift = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text="Provide the gift number AND % allocation OR $ amount.",
    )
    grant = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text="Provide the grant number AND % allocation OR $ amount.",
    )
    project = models.CharField(
        max_length=128,
        choices=PROJECT_CHOICES,
        help_text="""
            Provide the project number if known or to indicate that
            a new project number will be needed/requested.
        """,
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

        db_table = 'budget_operation'
        ordering  = ['-created_at']
        get_latest_by = 'created_at'
        verbose_name_plural = "Budget"

    def __str__(self):
        """Default data for display."""
        return "{0}: {1}, {2}".format(
            self.cost_center,
            self.created_by.last_name,
            self.created_by.first_name,
        )

    def approved(self):
        """Check if the submission is approved at all relevant levels."""
        status = False
        # level 3 and level 1 are minimum requirements for approval
        if self.level1 and self.level2:
            status = True
        return status

    def get_slug(self):
        """Slug for file uploads."""
        return 'files/budget/'

    def permissions(self, user):
        """Return user permissions for the object."""
        #perms = {'view': False, 'approver': False, 'level': []}
        group = in_group(user, settings.HR_GROUP)
        level = []
        approver = False
        view = False
        if user == self.created_by or group:
            view = True
        if user == self.cost_center.officer or group:
            level.append('level1')
            approver = True
        if user.id == LEVEL2.id or group:
            level.append('level2')
            approver = True
        perms = {'view': True, 'approver': approver, 'level': level}
        return perms

    def get_absolute_url(self):
        """Return the default URL of the detailed view."""
        return 'https://{0}{1}'.format(
            settings.SERVER_URL,
            reverse('budget_detail', args=(self.id,)),
        )


@receiver(models.signals.post_save, sender=Operation)
def send_mail_status(sender, instance, created, **kwargs):
    """Post-save signal function to notify folks of budget status."""
    if instance.declined:
        action = 'declined'
    elif instance.approved():
        action = 'approved'
    else:
        action = None
    if action and not instance.status_email:
        subject = '[Budget] modification {0}'.format(action)
        template = 'finance/budget/{0}.html'.format(action)
        to_list = settings.BUDGET_STATUS_LIST
        bcc = [settings.ADMINS[0][1]]
        bcc.append(instance.created_by.email)
        if settings.DEBUG:
            to_list = bcc
        send_mail(
            None,
            to_list,
            subject,
            instance.created_by.email,
            template,
            instance,
            bcc,
        )
        instance.status_email = True
        instance.save()
