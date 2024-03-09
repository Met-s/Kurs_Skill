# Generated by Django 4.2.6 on 2023-12-02 14:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simpleapp', '0002_subscriptions'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category_en_us',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='simpleapp.category', verbose_name='This is the help text'),
        ),
        migrations.AddField(
            model_name='product',
            name='category_ru',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='simpleapp.category', verbose_name='This is the help text'),
        ),
        migrations.AddField(
            model_name='product',
            name='description_en_us',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name_en_us',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name_ru',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='category name', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='simpleapp.category', verbose_name='This is the help text'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0, 'Price should be >= 0')]),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0, 'Quantity should be >= 0')]),
        ),
    ]
