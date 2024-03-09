from django.shortcuts import render
from datetime import datetime
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
from .models import Product


class ProductsList(ListView):
    # Указываем модель объекты которой будем выводить

    model = Product

    # Поле, которое будет использоваться для сортировки объектов

    ordering = 'name'

    # queryset = Product.objects.filter(
    #     price__lt=900
    # ).order_by('-name')

    # Указываем имя шаблона, в котором будут все инструкции о том, как именно
    # пользователю должны быть показаны наши объекты

    template_name = 'products.html'  # шаблон, который будет ипользоваться

    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.

    context_object_name = 'products'  # Переменная в шаблоне в которую
    # передаётся вся информация из модели

    # Метод get_context_data позволяет изменить набор данных,
    # который будет передан в шаблон
    def get_context_data(self, **kwargs):
        # С помощью super() обращаемся к родительским классам и вызываем у них
        # метод get_context_data с теми же аргументами.
        # В ответе должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'
        # context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = "Распродажа в среду!"
        return context


class ProductDetail(DetailView):
    # Модель всё та же, но мы хотим получить информацию по отдельному товару
    model = Product
    # Используем другой шаблон product.html
    template_name = 'product.html'
    # Название в котором будет выбранный пользователем продукт
    context_object_name = 'product'
