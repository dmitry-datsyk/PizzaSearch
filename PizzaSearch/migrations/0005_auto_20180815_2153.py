# Generated by Django 2.1 on 2018-08-15 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PizzaSearch', '0004_remove_pizza_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(verbose_name='Комментарий'),
        ),
    ]
