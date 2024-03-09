# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
from .models import Product, Subscriptions, Category
# -----------------
from django.http import HttpResponse
from .filters import ProductFilter
from django.urls import reverse_lazy
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
# -----------------
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from pprint import pprint
# ------------------------------------------------------
from django.http.response import HttpResponse
from django.views import View
from .tasks import hello, printer
from datetime import datetime, timedelta
from django.utils import timezone
# -----------------------------------------------------
# from django.views.decorators.cache import cache_page
# -----------------------------------------------------
from django.core.cache import cache
# ------------------------------D_13_Логирование-------
import logging
# ---------------D_14_Перевод---------
from django.utils.translation import gettext as _
# импортируем функцию для перевода
# from django.utils.translation import (activate,
#                                       get_supported_language_variant,
#                                       LANGUAGE_SESSION_KEY)
from django.utils import timezone
from django.shortcuts import redirect
import pytz
# ---------------D_15------------
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from simpleapp.serializers import *


from simpleapp.models import *





logger = logging.getLogger(__name__)


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

    template_name = 'products.html'  # шаблон, который будет использоваться

    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.

    context_object_name = 'products'  # Переменная в шаблоне в которую
    # передаётся вся информация из модели

    # Метод get_context_data позволяет изменить набор данных,
    # который будет передан в шаблон
    paginate_by = 5  # вот так можно указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # получаем обычный запрос
        queryset = super().get_queryset()
        # используем наш класс фильтрации
        # self.request.GET содержит объект QueryDict, который рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса, чтобы потом добавить в
        # контекст и использовать в шаблоне
        self.filterset = ProductFilter(self.request.GET, queryset)
        # возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        # С помощью super() обращаемся к родительским классам и вызываем у них
        # метод get_context_data с теми же аргументами.
        # В ответе должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'
        # context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['filterset'] = self.filterset

        # context['next_sale'] = "Распродажа в среду!"

        return context


def multiply(request):
    number = request.GET.get('number')
    multiplier = request.GET.get('multiplier')

    try:
        result = int(number) * int(multiplier)
        html = f"<html><body><h1>{number}*{multiplier}={result}</h1></body></html>"
    except (ValueError, TypeError):
        html = f"<html><body><h1>Invalid input.</h1></body></html>"

    return HttpResponse(html)


class ProductDetail(DetailView):
    # Модель всё та же, но мы хотим получить информацию по отдельному товару
    model = Product
    # Используем другой шаблон product.html
    template_name = 'product.html'
    # Название в котором будет выбранный пользователем продукт
    context_object_name = 'product'
    queryset = Product.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения
        # объекта, как ни странно
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)  # # кэш очень
        # Похож на словарь, и метод get действует так же. Он забирает значение
        # по ключу, если его нет, то забирает None.
        # Если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)
        return obj


class ProductsForm(LoginRequiredMixin, ListView):
    raise_exception = True
    model = Product
    ordering = 'name'
    template_name = 'products_form.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# Добавляем новое представление для создания товаров.
class ProductCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_product',)
    # raise_exception = True
    # Указываем нашу разработанную форму
    form_class = ProductForm
    # модель товаров
    model = Product
    # и новый шаблон, в котором используется форма
    template_name = 'product_edit.html'


# Добавляем представление для изменения товара.
class ProductUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.add_product',)
    # raise_exception = True
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'


# Представление удаляющее товар.
class ProductDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.add_product',)
    # raise_exception = True
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')


@login_required
@csrf_protect
# @cache_page(60 * 15)
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        pprint(f'CATEGORY_ID = {category_id}')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')
        pprint(category)

        if action == 'subscribe':
            Subscriptions.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriptions.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriptions.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


# @login_required
# def show_protected_page(request):
#     // do something protected

# class IndexView(View):
#     def get(self, request):
#         printer.apply_async([10], eta=datetime.now() + timedelta(seconds=5))
#         # printer.apply_async([10], eta=datetime.now()+timedelta(seconds=5))
#         # printer.apply_async([10], countdown=5)
#         # printer.delay(10)
#         hello.delay()
#         return HttpResponse('Hello!!!!')


class IndexView(View):
    def get(self, request):
        # printer.apply_async([10], countdown=5)
        # printer.apply_async([10], eta=timezone.now() + timedelta(seconds=5))
        hello.delay()
        return HttpResponse('Hello!!!!')


class Index(View):
    """
    Пример перевода.
    Простая view-функция, которая переводит только одну строку.
    Эта функция просто вернёт нам строку 'Hello world' в наш браузер,
    """

    def get(self, request):
        models = Product.objects.all()

        context = {'models': models,
                   'current_time': timezone.localtime(timezone.now()),
                   'timezones': pytz.common_timezones
                   }
        return HttpResponse(render(request,
                                   'translation.html', context))

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']

        return redirect('indexleng')

        # return redirect(request.Meta.get('HTTP_REFERER'))
        # . Translators: This message appears on the home page only
        # string = _('Hello world')
        #
        # # return HttpResponse(string)
        # context = {'string': string}
        # return HttpResponse(render(request,
        #                            'translation.html', context))


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# class SubscriptionsViewset(viewsets.ReadOnlyModelViewSet):
#     queryset = SubscriptionsSerializer
