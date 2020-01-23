#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

import django


django.setup()

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
        actions = Transaction.objects.all()
    elif model == 'requisition':
        actions = Requisition.objects.all()
    count = actions.count()
    print(count)


if __name__ == '__main__':
    args = parser.parse_args()
    model = args.model.lower()
    test = args.test

    if test:
        print(args)

    sys.exit(main())
