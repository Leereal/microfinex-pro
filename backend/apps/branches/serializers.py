from os import read
from rest_framework import serializers
from .models import Branch

class BranchSerializer(serializers.ModelSerializer):
    #No need to specify this if we can get the country using depth 1
    #using depth also helps eliminate taking relationships for relationship

    #We use PrimaryKeyRelatedField if we just want to see primary key like 1,2,3 

    #We use StringRelatedField if we want to see the value in model __str__ method like name etc and it's read only
    # users = serializers.StringRelatedField(many=True, read_only=True)
     
    #We can also use hyperlinked relationships that is HyperlinkedRelatedField
    # We can use SlugRelatedField if we want to use a slug field such as username
    #We can use HyperlinkedIdentityField if we want to use a hyperlink to the object
    # average_loan = serializers.ReadOnlyField()

    # def get_average_loan(self, obj):
    #     return obj.average_loan()

    class Meta:
        model = Branch
        fields = [
            "id",
            "name",
            "address",
            "email",
            "phone",
            "is_active",
            # "average_loan",
            # "total_clients",
            # "total_loans",
            # "total_disbursements",
            # "total_repayments",
            # "this_month_disbursements",
            # "this_month_repayments",
            # "percentage_target"
            # "users" #bad idea since it exposes the password. Use serializer instead       
        ]
        # depth = 2
        #You can specify the fields you don't want to be added or updated it's values
