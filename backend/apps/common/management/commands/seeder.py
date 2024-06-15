# myapp/management/commands/seeder.py

from decimal import Decimal
from django.core.management.base import BaseCommand
from apps.branch_assets.models import BranchAssets
from apps.branch_product_charge.models import BranchProductCharge
from apps.branch_products.models import BranchProduct
from apps.branches.models import Branch
from apps.charges.models import Charge
from apps.clients.models import Client, ClientLimit, Contact, NextOfKin
from apps.currencies.models import Currency
from apps.employers.models import Employer
from apps.finance.models import Finance
from apps.group_product.models import GroupProduct
from apps.group_product_charge.models import GroupProductCharge
from apps.groups.models import Group
from apps.loan_applications.models import LoanApplication, RejectionReason
from apps.loan_statuses.models import LoanStatus
from apps.payment_gateways.models import PaymentGateway
from apps.periods.models import Period
from apps.products.models import Product
from apps.users.models import User, UserBranch
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate Branch, BranchAssets, and User models with fake data'

    def handle(self, *args, **options):
        fake = Faker()

        # Generate Branches
        for _ in range(20):
            branch = Branch.objects.create(
                name=fake.city(),
                address=fake.address(),
                email=fake.email(),
                phone=fake.phone_number(),
                is_active=True,
                country=fake.country()
            )

        office_items = ['laptop', 'car', 'TV', 'chair', 'desk', 'printer', 'phone', 'monitor', 'keyboard', 'mouse']
        # Generate Users
        for _ in range(20):
            email = fake.unique.email()  # Ensure unique email addresses
            user = User.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=email,
                is_staff=fake.boolean(chance_of_getting_true=20),  # Example of a boolean field
                is_active=True,
                date_joined=fake.date_time_between(start_date="-1y", end_date="now"),
            )

            # Assign random branches to users
            branches = Branch.objects.order_by('?')[:random.randint(1, 3)]
            for branch in branches:
                UserBranch.objects.create(user=user, branch=branch, created_by_id=1)
        # Generate BranchAssets
        for branch in Branch.objects.all():
            item = random.choice(office_items)
            branch_asset = BranchAssets.objects.create(
                branch=branch,
                item=item,
                description=fake.text(),
                brand=fake.company(),
                color=fake.color_name(),
                quantity=fake.random_int(min=1, max=100),
                user_id=1,
                used_by_id=1,
                purchase_date=fake.date_between(start_date="-1y", end_date="today"),
                images=[]  # You may adjust this field based on your requirements
            )
               
        # Generate Periods
        # Customized names and their corresponding duration units
        period_details = [
            {"name": "Weekly", "units": ["weeks"]},
            {"name": "Monthly", "units": ["months"]},
            {"name": "Daily", "units": ["days"]},
            {"name": "Yearly", "units": ["years"]},
            {"name": "Quarterly", "units": ["months"]}
        ]

        for period_detail in period_details:
            # Select a name and its valid units
            name = period_detail["name"]
            valid_units = period_detail["units"]
            
            # Ensure the duration matches the unit for names with specific time frames
            if name == "Quarterly":
                # Assuming quarterly means 3 months duration
                duration = 3
                duration_unit = "months"
            elif name == "Yearly":
                duration = 1
                duration_unit = "years"
            else:
                # For other types, you can randomize within a sensible range if needed
                duration = fake.random_int(min=1, max=4)
                duration_unit = random.choice(valid_units)

            Period.objects.create(
                name=name,
                duration=str(duration),
                duration_unit=duration_unit,
                description=fake.text()
            )

        #Generate Products
        #Predefined product names
        product_names = ["SSB", "Paynet", "Loan Term", "Collateral Based"]

        #Generate Products with predefined names
        for name in product_names:
            Product.objects.create(
                name=name,
                is_active=fake.boolean(chance_of_getting_true=75)  # 75% chance to be active
            )
        

        #Generate Specific Currencies
        currencies = [
            {"name": "US Dollar", "code": "USD", "symbol": "$", "position": "before"},
            {"name": "Zim Dollar", "code": "ZWL", "symbol": "Z$", "position": "before"},
            {"name": "SA Rand", "code": "ZAR", "symbol": "R", "position": "before"},
            {"name": "Botswana Pula", "code": "BWP", "symbol": "P", "position": "before"},
        ]

        for currency in currencies:
            Currency.objects.create(
                name=currency["name"],
                code=currency["code"],
                symbol=currency["symbol"],
                position=currency["position"],
                is_active=True
            )
        
        # Generate BranchProducts
        branches = list(Branch.objects.all())
        products = list(Product.objects.all())
        periods = list(Period.objects.all())
        users = list(User.objects.all())

        for _ in range(10):  # Adjust the number of BranchProducts to generate as needed
            branch_product = BranchProduct.objects.create(
                branch=random.choice(branches),
                product=random.choice(products),
                interest=Decimal(fake.random_number(digits=2) + fake.random_number(digits=2) / 100),
                max_amount=Decimal(fake.random_number(digits=5)),
                min_amount=Decimal(fake.random_number(digits=3)),
                period=random.choice(periods),
                min_period=fake.random_int(min=1, max=12),
                max_period=fake.random_int(min=13, max=24),            
                created_by=random.choice(users)
            )
        
        #Generate Groups
        # Predefined group names
        group_names = [
            "Zesa", "ZNA", "Unki", "Mimosa", "Zim Teachers",
            "Bata", "Ok Supermarket", "TM Supermarket", "Chicken Feeder Crew"
        ]

        # Fetch all branches and a user to set as 'created_by'
        branches = list(Branch.objects.all())
        users = list(User.objects.all())

        for name in group_names:
            # Randomly assign a branch or None (to simulate groups without a branch)
            branch = random.choice(branches + [None])  # Adding None to the list

            group, created = Group.objects.get_or_create(
                name=name,
                defaults={
                    'description': fake.text(),
                    'leader': fake.name(),
                    'email': fake.email(),
                    'phone': fake.phone_number(),
                    'is_active': True,
                    'branch': branch,
                    'created_by': random.choice(users),
                    'status': Group.Status.ACTIVE if fake.boolean(chance_of_getting_true=75) else Group.Status.INACTIVE,
                }
            )
        
        #Generate group products
        groups = list(Group.objects.all())
        products = list(Product.objects.all())
        periods = list(Period.objects.all())
        users = list(User.objects.all())

        for _ in range(10):  # Adjust the number of GroupProducts to generate as needed
            group_product = GroupProduct.objects.create(
                group=random.choice(groups),
                product=random.choice(products),
                interest=Decimal(f"{random.randint(1, 15)}.{random.randint(0, 99)}"),
                max_amount=Decimal(fake.random_number(digits=5)),
                min_amount=Decimal(fake.random_number(digits=3)),
                period=random.choice(periods),
                min_period=fake.random_int(min=1, max=12),
                max_period=fake.random_int(min=13, max=24),
                created_by=random.choice(users)
            )

        # Generate Clients and Contacts
        users = list(User.objects.all())  # Assuming User model import is correct
        branches = list(Branch.objects.all())

        for _ in range(10):  # Adjust the number as needed
            client = Client.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                emails=[fake.email(), ],  # Assuming ArrayField expects a list
                national_id=fake.unique.ssn(),  # Or any appropriate method to generate a unique ID
                nationality=fake.country_code(representation="alpha-2"),
                # Fill in other fields as necessary...
                branch=random.choice(branches),  # Random branch or None
                created_by=random.choice(users),
                # Ensure to convert the date properly if your Django version does not auto-handle it
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=90),
                country=fake.country_code(representation="alpha-2"),
            )
            
            # Generate Contacts for the client
            for _ in range(random.randint(1, 3)):  # Each client will have 1 to 3 contacts
                Contact.objects.create(
                    client=client,
                    phone=fake.phone_number(),
                    type=random.choice([choice[0] for choice in Contact.ContactType.choices]),
                    is_primary=fake.boolean(),
                    is_active=fake.boolean(),
                    whatsapp=fake.boolean(),
                    # Fill in other fields as needed...
                )
            
            # Generate NextOfKin for the client
            NextOfKin.objects.create(
                client=client,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=fake.phone_number(),
                relationship=random.choice(['Sibling', 'Parent', 'Child', 'Friend', 'Spouse']),
                address=fake.address(),
                created_by=random.choice(users),
                is_active=True
            )

            # Generate an Employer for the client (assuming a client can have an employer)
            # Note: Adjust field values as necessary based on your model definitions
            if fake.boolean(chance_of_getting_true=100):  # 50% chance to have an employer
                Employer.objects.create(
                    client=client,
                    contact_person=fake.name(),
                    email=fake.email(),
                    phone=fake.phone_number(),
                    name=fake.company(),
                    address=fake.address(),
                    employment_date=fake.past_date(start_date="-5y", tzinfo=None),
                    job_title=fake.job(),
                    created_by=random.choice(users),
                    is_active=True
                )
                
            # Generate ClientLimits for the client
            currency = Currency.objects.order_by('?').first()
            ClientLimit.objects.create(
                client=client,
                max_loan=fake.random_number(digits=6, fix_len=True),  # Generate a random max loan value
                credit_score=fake.random_int(min=300, max=850),  # Example range for credit scores
                currency=currency
            )

        # Seed LoanStatuses with specific rules for auto calculations
        loan_status_names = ['Pending','Approved','Rejected','Active','Default','Completed','Overdue','Cancelled','Failed', 'Closed', 'Legal', 'Bad Debt']
        for name in loan_status_names:
            allow_auto_calculations = True if name in ['Active', 'Default'] else False
            LoanStatus.objects.get_or_create(
                name=name,
                defaults={
                    'description': fake.text(),
                    'allow_auto_calculations': allow_auto_calculations,
                    'is_active': True
                }
            )

        #Generate Specific Charges
        charge_details = [
            {"name": "Admin Fee Payment", "amount_type": "percentage", "charge_type": "credit", "charge_application": "principal", "mode": "auto"},
             {"name": "Admin Fee", "amount_type": "percentage", "charge_type": "debit", "charge_application": "principal", "mode": "auto"},
            {"name": "Processing Fee", "amount_type": "fixed", "charge_type": "debit", "charge_application": "principal", "mode": "auto"},
            {"name": "Interest", "amount_type": "percentage", "charge_type": "debit", "charge_application": "balance",  "mode": "auto"},
            {"name": "Late Payment Fee", "amount_type": "fixed", "charge_type": "debit", "charge_application": "other", "mode": "manual"},
            {"name": "Origination Fee", "amount_type": "percentage", "charge_type": "debit", "charge_application": "principal", "mode": "auto"},
            {"name": "Service Charge", "amount_type": "fixed", "charge_type": "debit", "charge_application": "principal",  "mode": "auto"},
            {"name": "Prepayment Penalty", "amount_type": "percentage", "charge_type": "debit", "charge_application": "balance","mode": "manual"},
            {"name": "Inspection Fee", "amount_type": "fixed", "charge_type": "debit", "charge_application": "other","mode": "manual"},
            {"name": "Legal Fee", "amount_type": "fixed", "charge_type": "debit", "charge_application": "other", "mode": "manual"},
            {"name": "Insurance", "amount_type": "fixed", "charge_type": "debit", "charge_application": "principal","mode": "auto"},
            {"name": "Annual Maintenance Fee", "amount_type": "fixed", "charge_type": "debit", "charge_application": "principal", "mode": "auto"},
        ]

        for charge_detail in charge_details:
            Charge.objects.get_or_create(
                name=charge_detail["name"],
                defaults={
                    "description": fake.text(),
                    "amount": fake.random_number(digits=3) if charge_detail["amount_type"] == "fixed" else fake.random_int(min=1, max=15),
                    "amount_type": charge_detail["amount_type"],
                    "charge_type": charge_detail["charge_type"],
                    "charge_application": charge_detail["charge_application"],
                    "loan_status": LoanStatus.objects.order_by('?').first(),
                    # "frequency": charge_detail["frequency"],
                    "mode": charge_detail["mode"],
                    "is_active": True
                }
            )
        
        # Generate Seed PaymentGateways with specific names and types
        payment_gateway_details = [
            {"name": "Cash", "type": "Offline"},
            {"name": "Paypal", "type": "Online"},
            {"name": "Ecocash", "type": "Online"},
            {"name": "RTGS", "type": "Offline"},
            {"name": "One Wallet", "type": "Online"},
            {"name": "Bank Transfer", "type": "Offline"},
        ]

        for gateway_detail in payment_gateway_details:
            PaymentGateway.objects.get_or_create(
                name=gateway_detail["name"],
                defaults={
                    "description": fake.text(),
                    "type": gateway_detail["type"],
                    "is_disbursement": fake.boolean(),
                    "is_repayment": fake.boolean(),
                    "is_active": True
                }
            )
        # Assuming you have some GroupProducts and BranchProducts already seeded
        # Seed GroupProductCharges and BranchProductCharges
        for group_product in GroupProduct.objects.all():
            GroupProductCharge.objects.create(
                group_product=group_product,
                charge=Charge.objects.order_by('?').first(),
                is_active=True
            )
        
        for branch_product in BranchProduct.objects.all():
            BranchProductCharge.objects.create(
                branch_product=branch_product,
                charge=Charge.objects.order_by('?').first(),
                is_active=True
            )
        
        # Seed Finances
        finance_types = ['Income', 'Expense', 'Investment', 'Withdrawal']
        for _ in range(20):
            Finance.objects.create(
                title=fake.company(),
                description=fake.text(),
                amount=fake.random_number(digits=5),
                received_from=fake.name() if fake.boolean() else '',
                paid_to=fake.name() if fake.boolean() else '',
                receipt_number=fake.bothify(text='???-#######'),
                type=random.choice(finance_types),
                created_by=User.objects.order_by('?').first(),
                branch=Branch.objects.order_by('?').first()
            )
        
        # Seed RejectionReasons
        users = list(User.objects.all())  # Assuming User model import is correct
        branches = list(Branch.objects.all())
        clients = list(Client.objects.all())

        rejection_titles = [
            'Incomplete Application',
            'Poor Credit Score',
            'Insufficient Income',
            'Unstable Employment History',
            'High Debt-to-Income Ratio',
            'Lack of Collateral',
            'Failed to Meet Loan Policy'
        ]

        for title in rejection_titles:
            RejectionReason.objects.get_or_create(
                title=title,
                defaults={
                    'description': fake.sentence(nb_words=10),
                    'user': random.choice(users),
                }
            )

        # Prepare rejection reasons for random assignment to rejected loan applications
        rejection_reasons = list(RejectionReason.objects.all())

        # Generate loan applications        
        for _ in range(100):  # Adjust the number of loan applications as needed
            loan_amount = Decimal(f"{random.randrange(100000, 5000000) / 100:.2f}")
            status = random.choice(["pending", "cancelled", "approved", "rejected"])

            loan_application_kwargs = {
                'client': random.choice(clients),
                'amount': loan_amount,
                'status': status,
                'user': random.choice(users),
                'branch': random.choice(branches)
            }

            if status == "rejected" and rejection_reasons:
                # Assign a random rejection reason for rejected loan applications
                loan_application_kwargs['rejection_reason'] = random.choice(rejection_reasons)

            # Note: You might need to handle the scenario where `rejection_reason` is expected to be null for non-rejected statuses
            # This simplistic approach assumes the LoanApplication model allows null for `rejection_reason` for non-rejected applications
            loan_application = LoanApplication.objects.create(**loan_application_kwargs)
        self.stdout.write(self.style.SUCCESS('Fake data populated successfully for Branch, BranchAssets, and User'))
