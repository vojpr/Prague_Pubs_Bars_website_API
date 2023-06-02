from django_filters import FilterSet, ChoiceFilter, RangeFilter, CharFilter, ModelMultipleChoiceFilter, OrderingFilter, BooleanFilter
from django_filters.widgets import RangeWidget
from .models import PubsBars
from django.forms import CheckboxInput, CheckboxSelectMultiple


class CustomOrderingFilter(OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "Sort by"
        self.extra['choices'] += [
            ('name', 'Name (A-Z)'),
            ('-name', 'Name (Z-A)'),
            ('-beer_rating', 'Beer rating (High to low)'),
            ('beer_rating', 'Beer rating (Low to high)'),
            ('-overall_rating', 'Overall rating (High to low)'),
            ('overall_rating', 'Overall rating (Low to high)'),
        ]
    

class PubsBarsFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')
    outside_tables = BooleanFilter(widget=CheckboxInput, method="filter_true_method")
    foosball = BooleanFilter(widget=CheckboxInput, method="filter_true_method")
    beer_rating = RangeFilter(label="Beer rating (min-max)", widget=RangeWidget(attrs={'type':'number', 'min': '1', 'max': '5'}))
    overall_rating = RangeFilter(label="Overall rating (min-max)", widget=RangeWidget(attrs={'type':'number', 'min': '1', 'max': '5'}))
    order_by = CustomOrderingFilter()

    def filter_true_method(self, queryset, name, value):
        if value:
            queryset = queryset.filter(**{f'{name}': True})
        return queryset

    class Meta:
        model = PubsBars
        fields = ['name', 'outside_tables', 'foosball', 'beer_rating', 'overall_rating']