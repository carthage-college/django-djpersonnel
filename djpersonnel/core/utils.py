from djzbar.core.sql import VEEPS
from djzbar.utils.informix import do_sql

from djzbar.utils.hr import get_position

LEVEL2 = get_position(settings.LEVEL2_TPOS)


def _level3_choices():

    level3 = do_sql(VEEPS)
    choices = [('','---select---')]

    for l in level3:
        name = '{}, {}'.format(v.lastname, v.firstname)
        choices.append((str(v.id), name))
    return choices

