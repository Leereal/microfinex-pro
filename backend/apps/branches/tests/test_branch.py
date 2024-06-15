import pytest
from apps import branch_assets
from apps.branches.factory import BranchFactory

from apps.branches.models import Branch
from apps.users.forms import User
# @pytest.mark.django_db
# def test_create_branch():
#     Branch.objects.create(name='test', address='test', email='leereal08@gmail.com', phone='1234567890', is_active=True, country='United States')
#     assert Branch.objects.count() == 1

# @pytest.mark.django_db
# def test_total_branches():
#     count = User.objects.all().count()
#     print(count)
#     assert count == 0

# @pytest.fixture(scope="session")
# def branch(db):
#     return Branch.objects.create(name='test', address='test', email='leereal08@gmail.com', phone='1234567890', is_active=True, country='United States')

# # @pytest.mark.django_db
# # def test_set_branch_address(branch):
# #     branch.address = 'new address'
# #     branch.save()
# #     assert branch.address == 'new address'
# @pytest.mark.django_db
# def test_new_branch(db,branch_factory):
#     branch = branch_factory.create()
#     branch.save()
#     print(branch_factory.name)
#     assert True

# @pytest.mark.django_db
# def test_branch_asset(db, branch_assets_factory):
#     branch_asset = branch_assets_factory.create()
#     branch_asset.save()
#     print(branch_assets_factory.item)
#     assert True

@pytest.fixture
def populate_branches():
    # Create instances using the BranchFactory
    branches = BranchFactory.create_batch(5)  # Create 5 fake branches

    # Save instances to the database
    for branch in branches:
        branch.save()

    # You can return the created instances if needed
    return branches

@pytest.mark.django_db
def test_branches(populate_branches):
    # You can access the created instances from populate_branches fixture
    branches = populate_branches
    assert len(branches) == 5  # Assert that 5 branches were created
    for branch in branches:
        assert branch.id is not None  # Assert that each branch has an ID assigned