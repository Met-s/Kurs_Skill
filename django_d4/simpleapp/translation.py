from .models import Product, Category
from modeltranslation.translator import register, TranslationOptions


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'category')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
