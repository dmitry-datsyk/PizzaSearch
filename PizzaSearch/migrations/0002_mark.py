# Generated by Django 2.1 on 2018-08-08 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PizzaSearch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(verbose_name='Оценка')),
                ('user_id', models.IntegerField(verbose_name='ID пользователя')),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='PizzaSearch.Shop', verbose_name='ID пиццы')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценки',
            },
        ),
    ]
