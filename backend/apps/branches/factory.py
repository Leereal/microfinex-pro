from apps.branch_assets.models import BranchAssets
from apps.branches.models import Branch
import factory
from faker import Faker

fake = Faker()


class BranchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Branch

    name = fake.city()
    address = fake.address()
    email = fake.email()
    phone = fake.phone_number()
    is_active = True
    country = fake.country()


class BranchAssetsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BranchAssets

    branch = factory.SubFactory(BranchFactory)
    item = fake.word()
    description = fake.text()
    brand = fake.company()
    color = fake.color_name()
    quantity = fake.random_number(digits=2)
    user = 1
    used_by = 1
    purchase_date = fake.date_this_decade()
    images = None