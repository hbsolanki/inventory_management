import  django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    sku=django_filters.CharFilter(field_name='sku',lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['sku']