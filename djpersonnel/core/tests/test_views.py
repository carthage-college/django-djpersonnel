# -*- coding: utf-8 -*-

from django.conf import settings
from django.test import TestCase
from django.apps import apps
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from djpersonnel.transaction.models import Operation as Transaction
from djpersonnel.requisition.models import Operation as Requisition
from djpersonnel.core.forms import DateCreatedForm
from djpersonnel.core.utils import get_deans, LEVEL2
from djtools.utils.users import in_group


def _operation_status(user, app, status, oid):
    model = apps.get_model(app_label=app, model_name='Operation')
    obj = get_object_or_404(model, pk=oid)
    perms = obj.permissions(user)
    if not obj.declined:
        if perms['approver'] and status in ['approved','declined']:

            from djtools.fields import NOW

            to_approver = []
            if perms['level1']:
                level = 'level1'
            elif perms['level2']:
                level = 'level2'
                users = User.objects.filter(groups__name=settings.HR_GROUP)
                for u in users:
                    to_approver.append(u.email)
            elif perms['level3']:
                level = 'level3'
                to_approver = [LEVEL2.email,]

            if status == 'approved':
                setattr(obj, level, True)
                setattr(obj, '{}_date'.format(level), NOW)

            if status == 'declined':
                obj.declined = True

            obj.save()

            bcc = settings.MANAGERS
            frum = user.email
            to_creator = [obj.created_by.email,]
            subject = "[PRF] {}: '{}'".format(status, obj.position_title)
            template = 'requisition/email/{}_{}.html'.format(level, status)

            if settings.DEBUG:
                print("DEBUG")
                obj.to_creator = to_creator
                to_creator = [settings.MANAGERS[0][1],]
                if to_approver:
                    to_approver = [settings.MANAGERS[0][1],]
                    obj.to_approver = to_approver

            '''
            # notify the creator of current status
            send_mail(
                request, to_creator, subject, frum, template, obj, bcc
            )
            '''

            # notify the next approver
            if to_approver and status == 'approved':
                print("to_approver = {}".format(to_approver))
                '''
                send_mail(
                    request, to_approver, subject, frum,
                    'requisition/email/approver.html', obj, bcc
                )
                '''

            message = "Personnel {} has been {}".format(app, status)
        else:
            message = "Access Denied"
    else:
        message = "Personnel {} has already been declined".format(app)


class CoreViewsTestCase(TestCase):

    fixtures = [
        'fixtures/group.json',
        'fixtures/user.json',
        'fixtures/requisition_operation.json',
        'fixtures/transaction_operation.json'
    ]

    def setUp(self):

        global user

        user = User.objects.get(
            pk=settings.TEST_USER_ID
        )
        self.level3_approver = User.objects.get(
            pk=settings.TEST_LEVEL3_APPROVER_ID
        )
        self.level2_approver = User.objects.get(
            pk=settings.TEST_LEVEL2_APPROVER_ID
        )
        self.level1_approver = User.objects.get(
            pk=settings.TEST_LEVEL1_APPROVER_ID
        )
        self.oid = 7
        self.created_at_date = settings.TEST_CREATED_AT_DATE

    def test_get_deans(self):
        deans = get_deans()
        print("deans = {}".format(deans))

    def test_home(self):

        hr = in_group(user, settings.HR_GROUP)

        # HR or VPFA can access all objects
        if hr or user.id == LEVEL2.id:
            requisitions = Requisition.objects.all()
            transactions = Transaction.objects.all()
        else:
            requisitions = Requisition.objects.filter(
                Q(created_by=user) | Q(level3_approver=user)
            )
            transactions = Transaction.objects.filter(
                Q(created_by=user) | Q(level3_approver=user)
            )

        self.assertGreaterEqual(requisitions.count(), 1)
        self.assertGreaterEqual(transactions.count(), 1)

    def test_requisition_search(self):

        form = DateCreatedForm()

        requisitions = Requisition.objects.filter(
            created_at__gte = self.created_at_date
        )

        self.assertGreaterEqual(requisitions.count(), 1)

    def test_transaction_search(self):

        transactions = Transaction.objects.filter(
            created_at__gte = self.created_at_date
        ).all()

        self.assertGreaterEqual(transactions.count(), 1)

    def test_requisition_status_level3_approved(self):

        _operation_status(
            self.level3_approver, 'requisition', 'approved', self.oid
        )

    def test_requisition_status_level3_declined(self):

        _operation_status(
            self.level3_approver, 'requisition', 'declined', self.oid
        )

    def test_requisition_status_level2_approved(self):

        _operation_status(
            self.level2_approver, 'requisition', 'approved', self.oid
        )

    def test_requisition_status_level2_declined(self):

        _operation_status(
            self.level2_approver, 'requisition', 'declined', self.oid
        )

    def test_requisition_status_level1_approved(self):

        _operation_status(
            self.level1_approver, 'requisition', 'approved', self.oid
        )

    def test_requisition_status_level1_declined(self):

        _operation_status(
            self.level1_approver, 'requisition', 'declined', self.oid
        )

