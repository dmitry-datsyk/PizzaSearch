# Generated by Django 2.1 on 2018-08-19 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PizzaSearch', '0007_auto_20180818_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('news', models.TextField(verbose_name='Новость')),
                ('date_news', models.DateField(verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
            },
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(verbose_name='Отзыв'),
        ),
        migrations.AlterField(
            model_name='pizzacheck',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='check/', verbose_name='Изображение'),
        ),
    ]
