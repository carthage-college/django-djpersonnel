# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.test import TestCase
from django.apps import apps
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from djpersonnel.transaction.models import Operation as Transaction
from djpersonnel.requisition.models import Operation as Requisition
from djpersonnel.core.forms import DateCreatedForm
from djpersonnel.core.utils import LEVEL2

from djtools.utils.test import create_test_user
from djtools.utils.users import in_group


class CoreViewsTestCase(TestCase):

    fixtures = [
        'fixtures/group.json',
        'fixtures/user.json',
        'fixtures/requisition_operation.json',
        #'fixtures/transaction_operation.json'
    ]

    def setUp(self):
        self.user = create_test_user()
        self.level3_approver = User.objects.get(
            pk=settings.TEST_LEVEL3_APPROVER_ID
        )
        self.oid = 7
        self.created_at_date = settings.TEST_CREATED_AT_DATE

    def test_home(self):

        user = self.user

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
        #self.assertGreaterEqual(transactions.count(), 1)

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

        #self.assertGreaterEqual(transactions.count(), 1)

    def test_operation_status(self):

        user = self.level3_approver
        app = 'requisition'
        model = apps.get_model(app_label=app, model_name='Operation')
        status = 'approved'
        obj = get_object_or_404(model, pk=self.oid)
        perms = obj.permissions(user)
        print("permissions:\n")
        print(perms)
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
                print("obj title: {}".format(obj.position_title))
                print(obj.__dict__)

                bcc = settings.MANAGERS
                frum = user.email
                to_creator = [obj.created_by.email,]
                subject = "[PRF] {}: '{}'".format(status, obj.position_title)
                template = 'requisition/email/{}_{}.html'.format(level, status)
                if settings.DEBUG:
                    obj.to_creator = to_creator
                    to_creator = [settings.MANAGERS[0][1],]
                    if to_approver:
                        to_approver = [settings.MANAGERS[0][1],]
                        obj.to_approver = to_approver

                print("bcc = {}".format(bcc))
                print("from = {}".format(frum))
                print("to_creator = {}".format(to_creator))
                print("to_approver = {}".format(to_approver))
                print("subject = {}".format(subject))
                print("template = {}".format(template))

                '''
                # notify the creator of current status
                send_mail(
                    request, to_creator, subject, frum, template, obj, bcc
                )
                '''

                '''
                # notify the next approver
                if to_approver and status == 'approved':
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

        print("Message:\n")
        print(message)
