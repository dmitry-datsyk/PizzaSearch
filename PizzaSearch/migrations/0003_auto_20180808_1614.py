# Generated by Django 2.1 on 2018-08-08 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PizzaSearch', '0002_mark'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(verbose_name='ID пользователя')),
                ('comment', models.TextField(max_length=1000, verbose_name='Комментарий')),
                ('date_comment', models.DateField(verbose_name='Дата создания')),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='PizzaSearch.Pizza', verbose_name='ID пиццы')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.AlterField(
            model_name='mark',
            name='pizza',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='PizzaSearch.Pizza', verbose_name='ID пиццы'),
        ),
    ]