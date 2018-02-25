from crmify.models import Lead
from factory import faker
import factory


class LeadFactory(factory.DjangoModelFactory):
    email = faker.Faker('email')
    first_name = faker.Faker('name')
    last_name = faker.Faker('name')

    class Meta:
        model = Lead