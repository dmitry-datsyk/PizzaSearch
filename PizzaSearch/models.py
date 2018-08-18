from django.contrib.auth.models import User
from django.db import models


class Shop(models.Model):
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return '{}'.format(self.name)

    name = models.CharField(max_length=100, null=True, blank=True,
                            verbose_name='Имя')
    website = models.URLField(max_length=100, null=True, blank=True,
                              verbose_name='Сайт')


class Pizza(models.Model):
    class Meta:
        verbose_name = 'Пицца'
        verbose_name_plural = 'Пиццы'

    def __str__(self):
        return '{}'.format(self.name)

    name = models.CharField(max_length=100, null=True, blank=True,
                            verbose_name='Название')
    description = models.TextField(max_length=300, null=True, blank=True,
                                   verbose_name='Состав')
    image = models.ImageField(upload_to='items/', verbose_name='Изображение',
                              null=True, blank=True)
    shop = models.ForeignKey(
        Shop, related_name='pizzas', on_delete=models.CASCADE,
        verbose_name='ID магазина')
    on_sale = models.BooleanField(verbose_name='В продаже', default=True)


class PizzaCheck(models.Model):
    class Meta:
        verbose_name = 'Пицца'
        verbose_name_plural = 'Пиццы'

    def __str__(self):
        return '{}'.format(self.name)

    name = models.CharField(max_length=100, null=True, blank=True,
                            verbose_name='Название')
    description = models.TextField(max_length=300, null=True, blank=True,
                                   verbose_name='Состав')
    image = models.ImageField(upload_to='check/', verbose_name='Изображение',
                              null=True, blank=True)
    shop = models.ForeignKey(
        Shop, related_name='pizzas_check', on_delete=models.CASCADE,
        verbose_name='ID магазина')



class Mark(models.Model):
    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    mark = models.IntegerField(verbose_name='Оценка')
    pizza = models.ForeignKey(
        Pizza, related_name='marks', on_delete=models.CASCADE,
        verbose_name='ID пиццы')
    user_id = models.IntegerField(verbose_name='ID пользователя')


class Comment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return '{}. {}'.format(self.id, self.sphere)

    # user_id = models.IntegerField(verbose_name='ID пользователя')
    comment = models.TextField(verbose_name='Комментарий')
    date_comment = models.DateField(verbose_name='Дата создания')
    pizza = models.ForeignKey(
        Pizza, related_name='comment', on_delete=models.CASCADE,
        verbose_name='ID пиццы')
    user = models.ForeignKey(
        User, related_name='comment_user', on_delete=models.CASCADE,
        verbose_name='ID user')
