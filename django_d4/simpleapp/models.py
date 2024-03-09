from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils.translation import gettext as _, pgettext_lazy
# from django.utils.translation import
# импортируем «ленивый» геттекст с подсказкой


# Товар для витрины
class Product(models.Model):
    """
    Класс Product, отображает товары и имеет обязательные поля name,
    description, quantity,
    category, price.
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    quantity = models.IntegerField(
        validators=[MinValueValidator(0,
                                      'Quantity should be >= 0')])
    # Поле которое будет ссылаться на модель категории
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE,
                                 related_name='products',
                                 verbose_name=pgettext_lazy(
                                     'help text for Product model',
                                     'This is the help text'))
    # все продукты в категории будут доступны через поле products
    price = models.FloatField(
        validators=[MinValueValidator(0.0,
                                      'Price should be >= 0')])

    @property
    def on_stock(self):
        """
         Отображает есть ли товар на складе есть=True, нет=False
        """
        return self.quantity > 0

    def __str__(self):
        return (f'{self.category} : {self.name} : {self.quantity} :'
                f' {self.description[:20]}')

    # Добавим absolute_urls
    def get_absolute_url(self):
        return f'/products/{self.id}'  # products
        # return reverse('product_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')


# Категория, к которой будет привязываться товар
class Category(models.Model):
    """
    Класс Category отображает категорию товара, name с максимальной
    длиной 100 символов.
    """
    name = models.CharField(max_length=100, unique=True,
                            help_text=_('category name'))  # добавим
    # переводящийся текст подсказку к полю

    def __str__(self):
        return f'{self.name.title()}'


class Subscriptions(models.Model):
    """
    Класс Подписчиков имеет два поля
    user = models.ForeignKey to=User,
    category = models.ForeignKey to=Category.
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             related_name='subscriptions')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE,
                                 related_name='subscriptions')
