import django_filters as filters
from .models import Client

class ClientFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name="first_name", lookup_expr="icontains")
    last_name = filters.CharFilter(field_name="last_name", lookup_expr="icontains")
    nationality = filters.CharFilter(field_name="nationality", lookup_expr="icontains")
    status = filters.CharFilter(field_name="status", lookup_expr="exact")
    created_at = filters.DateFromToRangeFilter(field_name="created_at")
    updated_at = filters.DateFromToRangeFilter(field_name="updated_at")
    national_id = filters.CharFilter(field_name="national_id", lookup_expr="icontains")
    passport_number = filters.CharFilter(field_name="passport_number", lookup_expr="icontains")
    gender = filters.ChoiceFilter(field_name="gender", choices=Client.Gender.choices)
    date_of_birth = filters.DateFromToRangeFilter(field_name="date_of_birth")
    suburb = filters.CharFilter(field_name="suburb", lookup_expr="icontains")
    city = filters.CharFilter(field_name="city", lookup_expr="icontains")
    branch = filters.CharFilter(field_name="branch__name", lookup_expr="icontains")
    is_guarantor = filters.BooleanFilter(field_name="is_guarantor")
    is_active = filters.BooleanFilter(field_name="is_active")

    class Meta:
        model = Client
        fields = [
            "first_name", "last_name", "nationality", "status", 
            "created_at", "updated_at", "national_id", "passport_number", 
            "gender", "date_of_birth", "suburb", "city", "branch", 
            "is_guarantor", "is_active"
        ]
