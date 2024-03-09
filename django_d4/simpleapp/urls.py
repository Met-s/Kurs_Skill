# from allauth.mfa.views import IndexView   # авто импорт
from django.urls import path
from .views import (
    ProductsList, ProductDetail, ProductsForm, ProductCreate,
    ProductUpdate, ProductDelete, subscriptions, IndexView,
    Index,
)


urlpatterns = [
    # path - означает ПУТЬ
    # В данном случае путь ко всем товарам останется пустым
    # Т.к. объявленное представление является классом, а Django ожидает
    # функцию, надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', ProductsList.as_view(), name='product_list'),
    # pk - это первичный ключ товара, который будет выводиться у нас в шаблон
    # int - указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('products_form/', ProductsForm.as_view()),
    path('create/', ProductCreate.as_view(), name='product_create'),
    path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('index/', IndexView.as_view()),
    path('indexleng/', Index.as_view(), name='indexleng'),  # /products/indexleng
]
