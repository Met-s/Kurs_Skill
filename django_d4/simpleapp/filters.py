from django_filters import FilterSet
from .models import Product


# Создаём набор фильтров для модели Product
# FilterSet, который наследуем очень похож на Django дженерики

class ProductFilter(FilterSet):
    class Meta:
        # В Meta классе нужно указать Django модель, в которой будем
        # фильтровать записи.
        model = Product
        # В fields описываем по каким полям модели будет
        # производиться фильтрация
        fields = {
            # Поиск по названию
            'name': ['icontains'],
            # Количество товаров должно быть больше или раво
            'quantity': ['gt'],
            'price': [
                'lt',  # цена меньше или равна указанной
                'gt',  # цена больше или равна указанной
            ],
        }
