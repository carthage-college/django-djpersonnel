import django
django.setup()

from django.conf import settings
from django.core import serializers

from djpersonnel.transaction.models import Operation

import json


json_data = open(
    '{}/fixtures/transaction_operation.json'.format(settings.ROOT_DIR)
).read()
json_dict = json.loads(json_data)
print(json_dict[0]['fields'])

obj_generator = serializers.json.Deserializer(json_data)
for obj in obj_generator:
    obj.save()
    print(obj.object)

print("Faker")

from faker import Faker

fake = Faker()

print(fake.name())
print(fake.address())
print(fake.text())

fake = Faker('es_ES')
for _ in range(10):
    print(fake.name())
