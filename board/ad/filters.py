from django_filters import FilterSet
from .models import UserResponse


class ResponseFilter(FilterSet):
    # qw = UserResponse.ad

    class Meta:
        model = UserResponse
        fields = {
            'ad': ['exact'],

        }
