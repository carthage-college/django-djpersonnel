from factory.django import DjangoModelFactory
from faker import Factory

faker = Factory.create()


class RequisitionFactory(DjangoModelFactory):
    class Meta:
        model = 'requisition.Operation'

