# -*- coding: utf-8 -*-

from django.conf import settings
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from djpersonnel.core.utils import get_permissions
from djtools.fields.helpers import upload_to_path


VARY_CHOICES = (
    ('Increase', 'Increase'),
    ('Decrease', 'Decrease'),
)


class Budget(models.Model):
    """Data model for the budget form."""

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
    # VP of Area
    approver = models.ForeignKey(
        User,
        related_name='budget_approver',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    approved = models.BooleanField(default=False)
    approved_date = models.DateField(
        null=True,
        blank=True,
    )
    # form fields
    version = models.CharField(max_length=128)
    cost_center = models.CharField(max_length=128)
    variation = models.CharField(
        max_length=16,
        choices=VARY_CHOICES,
    )
    amount = models.CharField(max_length=128)
    fund = models.CharField(max_length=128)
    program = models.CharField(max_length=128)
    gift = models.CharField(max_length=128)
    grant = models.CharField(max_length=128)
    project = models.CharField(max_length=128)
    phile = models.FileField(
        "Budget File",
        upload_to=upload_to_path,
        max_length=768,
        null=True,
        blank=True,
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

    def __unicode__(self):
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
