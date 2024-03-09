from django.core.management.base import BaseCommand, CommandError
from simpleapp.models import Product


class Command(BaseCommand):
    help = 'Удаление продуктов в выбранной категории'
    requires_migrations_checks = True

    def category(self, *args, **kwargs):
        product_category = Product.objects.category.all()
        self.stdout.readable()
        self.stdout.write(f'{product_category} Выберите категорию товары '
                          f'которой нужно удалить')
        answer = input()

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write(
            'Do you really want to delete all products? yes/no')
        answer = input()

        if answer == 'yes':
            Product.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Successfully wiped '
                                                 'products!'))
            return
        self.stdout.write(self.style.ERROR('Access denied'))
