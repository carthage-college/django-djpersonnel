#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
# env
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/data2/django_1.11/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djpersonnel.settings.shell')

import django
django.setup()

from django.conf import settings

from djpersonnel.transaction.models import Operation as Transaction
from djpersonnel.requisition.models import Operation as Requisition

import argparse

'''
Various reports on database activity
'''

# set up command-line options
desc = """
Accepts as input...
"""

# RawTextHelpFormatter method allows for new lines in help text
parser = argparse.ArgumentParser(
    description=desc, formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument(
    '-m', '--model',
    required=True,
    help="Transaction or Requisition",
    dest='model'
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test'
)

def main():
    '''
    main function
    '''

    if test:
        print("Model = {}".format(model))

    if model == 'transaction':
        objects = Transaction.objects.all()
    elif model == 'requisition':
        objects = Requisition.objects.all()
    count = objects.count()
    print(count)

######################
# shell command line
######################

if __name__ == '__main__':
    args = parser.parse_args()
    model = args.model.lower()
    test = args.test

    if test:
        print(args)

    sys.exit(main())

