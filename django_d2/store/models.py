from django.db import models
from django.utils import timezone
from django.utils.datetime_safe import datetime


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey("Staff", on_delete=models.CASCADE)
# Поле модели products, реализующее связь с моделью Product через
# промежуточную таблицу ProductOrder
    products = models.ManyToManyField("Product", through='ProductOrder')

    def get_duration(self):
        if self.complete:  # если завершён возвращаем разность объектов
            return (self.time_out - self.time_in).total_seconds() // 60
        else:
            return ((datetime.now(timezone.utc) - self.time_in).total_seconds()
                    // 60)

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    composition = models.TextField(default="Состав не указан")
    slug = models.SlugField(max_length=255, unique=True)


class Staff(models.Model):
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'

    POSITIONS = [
        (director, 'Директор'),
        (admin, 'Администратор'),
        (cook, 'Повар'),
        (cashier, 'Кассир'),
        (cleaner, 'Уборщик')
    ]

    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=2,
                                choices=POSITIONS,
                                default=cashier)
    labor_contract = models.IntegerField()


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1, db_column='amount')

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()
