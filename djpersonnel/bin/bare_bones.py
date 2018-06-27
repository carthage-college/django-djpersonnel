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
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djequis.settings")

from django.conf import settings


# set up command-line options

def main():
    """
    """

    try:
        # do something
    except Exception, e:
        print "does not exist"
        print "Exception: {}".format(str(e))
        sys.exit(1)


######################
# shell command line
######################

if __name__ == "__main__":

    sys.exit(main())
