#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

import django


django.setup()

from djimix.people.departments import department as dept_name
from djpersonnel.core.utils import get_department
from djpersonnel.requisition.models import Operation as Requisition
from djpersonnel.transaction.models import Operation as Transaction

# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djpersonnel.settings.shell')


# set up command-line options
desc = """
    Accepts as input Transaction or Requistion.
"""

# RawTextHelpFormatter method allows for new lines in help text
parser = argparse.ArgumentParser(
    description=desc, formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    '-m',
    '--model',
    required=True,
    help="Transaction or Requisition",
    dest='model',
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test',
)


def main():
    """Various reports on database activity."""
    if test:
        print("Model = {0}".format(model))

    if model == 'transaction':
        actions = Transaction.objects.all().order_by('department_name')
    elif model == 'requisition':
        actions = Requisition.objects.all().order_by('department_name')
    else:
        print('model argument must be "transaction" or "requisition"')
        sys.exit(-1)

    for obj in actions:
        code = obj.department_name.strip()
        dept = get_department(code)
        if dept:
            if test:
                print(dept['code'], dept['name'], dept['id'])
            else:
                obj.department_name = dept['id']
                obj.save()
        else:
            if test:
                name = dept_name(code)
                print(
                    'fail: {0}|{1}|{2}|{3}|{4}'.format(
                        code, name, obj.created_by, obj.created_at, obj.id,
                    ),
                )
            else:
                obj.department_name = ''
                obj.save()


if __name__ == '__main__':
    args = parser.parse_args()
    model = args.model.lower()
    test = args.test

    if test:
        print(args)

    sys.exit(main())
