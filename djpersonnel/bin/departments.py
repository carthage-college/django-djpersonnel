import django
django.setup()

from djpersonnel.core.utils import get_department
from djpersonnel.core.utils import get_department_choices
from djpersonnel.requisition.models import Operation as Requisition
from djpersonnel.transaction.models import Operation as Transaction


#objects = Transaction.objects.all().order_by('department_name')
objects = Requisition.objects.all().order_by('department_name')
for obj in objects:
    code = obj.department_name.strip()
    dept = get_department(code)
    if dept:
        print(dept['code'], dept['name'])
    else:
        print(code)
