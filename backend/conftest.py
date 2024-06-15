import pytest
from pytest_factoryboy import register

from apps.branches.factory import BranchFactory, BranchAssetsFactory

register(BranchFactory) 
register(BranchAssetsFactory)

@pytest.fixture
def new_branch(db, branch_factory):
    return branch_factory.create()

# @pytest.fixture
# def new_branch_asset(db, branch_assets_factory):
#     return branch_assets_factory.create()

# import pytest

# from apps.branches.models import Branch

# @pytest.fixture
# def new_branch_factory(db):
#     def create_branch(
#         name: str,
#         address: str = "123 Street",
#         email: str = "test@example.com",
#         phone: str = "+1234567890",
#         is_active: bool = True,
#         country: str = "US"
#     ):
#         branch = Branch.objects.create(
#             name=name,
#             address=address,
#             email=email,
#             phone=phone,
#             is_active=is_active,
#             country=country
#         )
#         return branch
#     return create_branch

# @pytest.fixture
# def new_branch(db, new_branch_factory):
#     return new_branch_factory("Test Branch")






# from django.contrib.auth.models import User
# import pytest

# @pytest.fixture
# def new_user_factory(db):
#     def create_app_user(
#         username:str,
#         password:str=None,
#         first_name:str="firstname",
#         last_name:str="lastname",
#         email:str="test@test.com",
#         is_staff:str=False,
#         is_superuser:bool=False,
#         is_active:bool=True
#     ):
#         user = User.objects.create_user(
#             username=username,
#             password=password,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             is_staff=is_staff,
#             is_superuser=is_superuser,
#             is_active=is_active
#         )
#         return user
#     return create_app_user

# @pytest.fixture
# def new_user(db, new_user_factory):
#     return new_user_factory(
#         "TestUser",
#         "TestUser",
#         "Test",
#     )
