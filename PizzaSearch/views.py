import random
import re
import shutil
import threading
from multiprocessing import Process

from django.db import connection
from urllib.request import urlopen

import datetime
import requests
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Max
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import login, logout
from bs4 import BeautifulSoup
from selenium import webdriver

from PizzaSearch.models import Pizza, Mark, Comment, PizzaCheck, Shop, News


def index(request):
    shop = Shop.objects.all
    news = News.objects.order_by('-date_news')[:2]
    pizza = Pizza.objects.all()
    # id = []
    id = [(i.id) for i in pizza]
    # for  piz in pizza:
    #     id.append(piz.id)
    rand_id = random.choice(id)
    pizza1 = Pizza.objects.filter(id=rand_id).all
    return render(request, 'index.html', {
        'shop': shop, 'news': news, 'pizza': pizza1
    })


def shop(request, shop_id):
    pizza = Pizza.objects.filter(shop_id=shop_id).select_related('shop').all
    return render(request, 'shop.html', {'pizza': pizza})

def rating(request):
    rating = Mark.objects.select_related('pizza').select_related(
        'pizza__shop').all
    average_mark = Mark.objects.select_related('pizza').values(
        'pizza__name', 'pizza__shop__name', 'pizza__id','pizza__shop__id'
                ).annotate(
        avg_mark=Avg('mark'), cnt_user=Count('user_id')).order_by('-avg_mark')
    place = []
    position = 0
    for id in average_mark:
        position += 1
        place.append(position)
    return  render(request, 'rating.html', {
        'rating': rating, 'place': place,
           'average_mark':average_mark })


def news(request):
    news = News.objects.all
    return render(request, 'news.html', {'news': news})

def new(request, news_id):
    if request.method == 'GET':
        new = News.objects.filter(id=news_id).all
    return render(request, 'new.html'.format(news_id), {'new': new})
        # redirect('new', news_id, {'new':new})
    #render(request, 'news/{}'.format(news_id), {'news': news})




class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


def autamatic_search_data(request):
    # url = 'https://www.pizzatempo.by/menu/pizza.html'
    # r = requests.get(url)
    # with open('test.html', 'w', encoding='utf-8') as output_file:
    #     output_file.write(r.text)
    # html = open('test.html', "r", encoding='utf-8').read()
    # name_piz = []
    # img_piz = []
    # descr_piz = []
    # soup = BeautifulSoup(html, 'lxml')
    # div = soup.find_all('div', class_=[
    #     'item group1 novinka_1', 'item group1 novinka_', 'item group2 novinka_',
    #     'item group3 novinka_'
    # ])
    # for pizza in div:
    #     name = pizza.find('h3').find('span').next_element
    #     name_piz.append(name)
    #     image = pizza.find('div', class_='info').find(
    #         'div', class_='photo').find('img')
    #     link = image.get('src')
    #     img_piz.append(link)
    #     description = pizza.find('div', class_='info').find(
    #         'div', class_='photo').find(
    #         'div', class_='composition_holder').find(
    #         'div', class_='composition').next_element
    #     descr_piz.append(description)
    # index = 0
    # img_piz1 = []
    # img_piz2 = []
    # descr_piz1 = []
    # result = []
    # while index < len(img_piz):
    #     with open(
    #             'C:\\Users\Dmitry\PycharmProjects\\untitled2\PizzaSearch\static\media\items\\tempo{}.jpg'.format(
    #                 index), 'wb') as img:
    #         img.write(urlopen(img_piz[index]).read())
    #     img_piz1.append('items/tempo{}.jpg'.format(index))
    #     img_piz2.append('tempo{}.jpg'.format(index))
    #     descr_piz1.append(descr_piz[index][6:-5])
    #     array = []
    #     array.append(name_piz[index])
    #     array.append(img_piz1[index])
    #     array.append(descr_piz1[index])
    #     result.append(array)
        # print(result)
        # Pizza.objects.create(
        #     name = array[0], description = array[2], image = array[1],
        # shop_id=1)
        # index += 1
    # image = urlopen(img_piz[0])
    # Pizza.objects.get(id=1).image.save(
    #     '{}'.format(img_piz2[0]), image)

    # DOMINOS
    # url = 'https://dominos.by/ru/Pizza/'
    # r = requests.get(url)
    # with open('test1.html', 'w', encoding='utf-8') as output_file:
    #     output_file.write(r.text)
    # html = open('test1.html', "r", encoding='utf-8').read()
    # name_piz = []
    # img_piz = []
    # descr_piz = []
    # soup = BeautifulSoup(html, 'lxml')
    # div = soup.find_all('div', class_='product_item')
    # for pizza in div:
    #     name = pizza.find('p').find('a')
    #     if name is not None:
    #         name = name.next_element.lstrip()
    #         name_piz.append(name)
    #     image = pizza.find('div', class_='product_img_holder')
    #     if image is not None:
    #         image = image.find('a').find('img')
    #         link = image.get('src')
    #         img_piz.append(link)
    #     description = pizza.find('div', class_='product_mix')
    #     if description is not None:
    #         description = description.find('p').next_element
    #         descr_piz.append(description)
    # index = 0
    # img_piz1 = []
    # img_piz2 = []
    # descr_piz1 = []
    # result = []
    # while index < len(img_piz):
    #     with open(
    #             'C:\\Users\Dmitry\PycharmProjects\\untitled2\PizzaSearch\static\media\items\\dominos{}.jpg'.format(
    #                 index), 'wb') as img:
    #         img.write(urlopen('https://dominos.by/' + img_piz[index]).read())
    #     img_piz1.append('items/dominos{}.jpg'.format(index))
    #     img_piz2.append('dominos{}.jpg'.format(index))
    #     descr = ' '.join(descr_piz[index].split()).lower()
    #     descr_piz1.append(descr)
    #     array = []
    #     array.append(name_piz[index][0:-9])
    #     array.append(img_piz1[index])
    #     array.append(descr_piz1[index])
    #     result.append(array)
    #     Pizza.objects.create(
    #         name = array[0], description = array[2], image = array[1],
    #     shop_id=3)
    #     index += 1
    #
    #pzz
    # driver = webdriver.Chrome(
    #     executable_path='C:\\Users\Dmitry\PycharmProjects\\'
    #                     'untitled2\PizzaSearch\chromedriver.exe')
    # driver.get('https://pzz.by/pizzas')
    # result = driver.find_elements_by_class_name('pizzas-block')
    # name = [
    #     res.text for result in result for res in
    #     result.find_elements_by_tag_name('a') if res.text != '']
    # image = [
    #     res.get_attribute('src') for result in result for res in
    #     result.find_elements_by_tag_name('img')]
    # description = [
    #     res.text for result in result for result1 in
    #     result.find_elements_by_class_name('goods__list__text') for res in
    #     result1.find_elements_by_tag_name('p')]
    # if len(name) == len(image) and len(description) == len(description):
    #     index = 0
    #     img_piz1 = []
    #     img_piz2 = []
    #     result = []
    #     while index < len(name):
    #         with open(
    #                 'C:\\Users\Dmitry\PycharmProjects\\untitled2'
    #                 '\PizzaSearch\static\media\items\pzz{}.jpg'.format(
    #                     index), 'wb') as img:
    #             img.write(urlopen(image[index]).read())
    #         img_piz1.append('items/pzz{}.jpg'.format(index))
    #         img_piz2.append('pzz{}.jpg'.format(index))
    #         array = []
    #         array.append(name[index])
    #         array.append(img_piz1[index])
    #         array.append(description[index])
    #         result.append(array)
    #         Pizza.objects.create(
    #             name=array[0], description=array[2], image=array[1],
    #             shop_id=2)
    #         index += 1

    url = 'http://presto-pizza.by/group/1/1/'
    r = requests.get(url)
    with open('presto.html', 'w', encoding='utf-8') as output_file:
        output_file.write(r.text)
    html = open('presto.html', "r", encoding='utf-8').read()
    name_piz = []
    img_piz = []
    descr_piz = []
    soup = BeautifulSoup(html, 'lxml')
    h3 = soup.find_all('h3')
    for pizza in h3:
        name_piz.append(pizza.next_element)
    span = soup.find_all('div', class_='views-field views-field-php-1')
    for span in span:
        span1 = span.find_all('span', class_='field-content')
        for descr in span1:
            descr_piz.append(descr.next_element[0:-26].lower())
    span = soup.find_all('div', class_='views-field views-field-php')
    for span in span:
        image = span.find('span', class_='field-content').find('img')
        if image is not None:
            link = image.get('img')
            img_piz.append(link)
    index = 0
    img_piz1 = []
    img_piz2 = []
    descr_piz1 = []
    result = []
    while index < len(img_piz):
        with open(
                'C:\\Users\Dmitry\PycharmProjects\\untitled2\PizzaSearch\static\media\items\\presto{}.jpg'.format(
                    index), 'wb') as img:
            img.write(urlopen(img_piz[index]).read())
        img_piz1.append('items/presto{}.jpg'.format(index))
        img_piz2.append('presto{}.jpg'.format(index))
        descr = ' '.join(descr_piz[index].split()).lower()
        descr_piz1.append(descr)
        array = []
        array.append(name_piz[index])
        array.append(img_piz1[index])
        array.append(descr_piz1[index])
        result.append(array)
        Pizza.objects.create(
            name=array[0], description=array[2], image=array[1],
            shop_id=6)
        index += 1
    return render(request, 'autamatic_search_data.html', {'res': result})


def pizzas(request):
    piz = Pizza.objects.all
    return render(request, 'pizzas.html', {'piz': piz})


def pizza(request, pizza_id):
    if request.method == 'GET':
        piza = Pizza.objects.filter(
            id=int(pizza_id)).select_related('shop').all
        average_mark = Mark.objects.filter(pizza_id=pizza_id).aggregate(
            avg_mark=Avg('mark'), cnt_user=Count('user_id'))
        number = [value for key, value in average_mark.items()]
        if Mark.objects.filter(user_id=request.user.id, pizza_id=pizza_id):
            mark_user = Mark.objects.get(
                user_id=request.user.id, pizza_id=pizza_id).mark
        else:
            mark_user = 0
        if number[0] is not None:
            rating = round(number[0], 1)
            count = number[1]
        else:
            rating = 0
            count = 0
        comments = Comment.objects.filter(
            pizza_id=pizza_id).select_related('user').order_by('-date_comment')
        return render(request, 'pizza.html', {
            'piz': piza, 'num': rating,
            'count': count, 'comments': comments,
            'mark_user': mark_user})
    elif request.method == 'POST' and 'comment' in request.POST:
        Comment.objects.create(
            comment=request.POST.get('comment'),
            date_comment=datetime.datetime.now(),
            pizza_id=pizza_id,
            user_id=request.user.id
        )
        return redirect('pizza', pizza_id)
    else:

        if Mark.objects.filter(user_id=request.user.id, pizza_id=pizza_id):
            id_mark = Mark.objects.get(
                user_id=request.user.id, pizza_id=pizza_id).id
            Mark.objects.filter(id=id_mark).update(
                mark=request.POST.get('rating'),
                user_id=request.user.id,
                pizza_id=pizza_id
            )
        else:
            Mark.objects.create(
                mark=request.POST.get('rating'),
                user_id=request.user.id,
                pizza_id=pizza_id)
        return redirect('pizza', pizza_id)


def autamatic_check(request):
    if request.method == 'POST' and 'check' in request.POST:
        PizzaCheck.objects.all().delete()

        # url = 'https://www.pizzatempo.by/menu/pizza.html'
        # r = requests.get(url)
        # with open('tempo.html', 'w', encoding='utf-8') as output_file:
        #     output_file.write(r.text)
        # html = open('tempo.html', "r", encoding='utf-8').read()
        # name_piz = []
        # img_piz = []
        # descr_piz = []
        # soup = BeautifulSoup(html, 'lxml')
        # div = soup.find_all('div', class_=[
        #     'item group1 novinka_1', 'item group1 novinka_',
        #     'item group2 novinka_',
        #     'item group3 novinka_'
        # ])
        # for pizza in div:
        #     name = pizza.find('h3').find('span').next_element
        #     name_piz.append(name)
        #     image = pizza.find('div', class_='info').find(
        #         'div', class_='photo').find('img')
        #     link = image.get('src')
        #     img_piz.append(link)
        #     description = pizza.find('div', class_='info').find(
        #         'div', class_='photo').find(
        #         'div', class_='composition_holder').find(
        #         'div', class_='composition').next_element
        #     descr_piz.append(description)
        # index = 0
        # img_piz1 = []
        # img_piz2 = []
        # descr_piz1 = []
        # result = []
        # while index < len(img_piz):
        #     with open(
        #             'C:\\Users\Dmitry\PycharmProjects\\untitled2\PizzaSearch\static\media\check\\tempo{}.jpg'.format(
        #                 index), 'wb') as img:
        #         img.write(urlopen(img_piz[index]).read())
        #     img_piz1.append('check/tempo{}.jpg'.format(index))
        #     img_piz2.append('tempo{}.jpg'.format(index))
        #     descr_piz1.append(descr_piz[index][6:-5])
        #     array = []
        #     array.append(name_piz[index])
        #     array.append(img_piz1[index])
        #     array.append(descr_piz1[index])
        #     result.append(array)
        #     PizzaCheck.objects.create(
        #         name=array[0], description=array[2], image=array[1],
        #         shop_id=1)
        #     index += 1
        #
        # url = 'https://dominos.by/ru/Pizza/'
        # r = requests.get(url)
        # with open('dominos.html', 'w', encoding='utf-8') as output_file:
        #     output_file.write(r.text)
        # html = open('dominos.html', "r", encoding='utf-8').read()
        # name_piz = []
        # img_piz = []
        # descr_piz = []
        # soup = BeautifulSoup(html, 'lxml')
        # div = soup.find_all('div', class_='product_item')
        # for pizza in div:
        #     name = pizza.find('p').find('a')
        #     if name is not None:
        #         name = name.next_element.lstrip()
        #         name_piz.append(name)
        #     image = pizza.find('div', class_='product_img_holder')
        #     if image is not None:
        #         image = image.find('a').find('img')
        #         link = image.get('src')
        #         img_piz.append(link)
        #     description = pizza.find('div', class_='product_mix')
        #     if description is not None:
        #         description = description.find('p').next_element
        #         descr_piz.append(description)
        # index = 0
        # img_piz1 = []
        # img_piz2 = []
        # descr_piz1 = []
        # while index < len(img_piz):
        #     with open(
        #             'C:\\Users\Dmitry\PycharmProjects\\untitled2\PizzaSearch'
        #             '\static\media\check\\dominos{}.jpg'.format(
        #                 index), 'wb') as img:
        #         img.write(
        #             urlopen('https://dominos.by/' + img_piz[index]).read())
        #     img_piz1.append('check/dominos{}.jpg'.format(index))
        #     img_piz2.append('dominos{}.jpg'.format(index))
        #     descr = ' '.join(descr_piz[index].split()).lower()
        #     descr_piz1.append(descr)
        #     array = []
        #     array.append(name_piz[index][0:-9])
        #     array.append(img_piz1[index])
        #     array.append(descr_piz1[index])
        #     PizzaCheck.objects.create(
        #         name=array[0], description=array[2], image=array[1],
        #         shop_id=3)
        #     index += 1
        #
        # driver = webdriver.Chrome(
        #     executable_path='C:\\Users\Dmitry\PycharmProjects\\'
        #                     'untitled2\PizzaSearch\chromedriver.exe')
        # driver.get('https://pzz.by/pizzas')
        # result = driver.find_elements_by_class_name('pizzas-block')
        # name = [
        #     res.text for result in result for res in
        #     result.find_elements_by_tag_name('a') if res.text != '']
        # image = [
        #     res.get_attribute('src') for result in result for res in
        #     result.find_elements_by_tag_name('img')]
        # description = [
        #     res.text for result in result for result1 in
        #     result.find_elements_by_class_name('goods__list__text') for res in
        #     result1.find_elements_by_tag_name('p')]
        # if len(name) == len(image) and len(description) == len(description):
        #     index = 0
        #     img_piz1 = []
        #     img_piz2 = []
        #     while index < len(name):
        #         with open(
        #                 'C:\\Users\Dmitry\PycharmProjects\\untitled2'
        #                 '\PizzaSearch\static\media\check\pzz{}.jpg'.format(
        #                     index), 'wb') as img:
        #             img.write(urlopen(image[index]).read())
        #         img_piz1.append('check/pzz{}.jpg'.format(index))
        #         img_piz2.append('pzz{}.jpg'.format(index))
        #         array = []
        #         array.append(name[index])
        #         array.append(img_piz1[index])
        #         array.append(description[index])
        #         PizzaCheck.objects.create(
        #             name=array[0], description=array[2], image=array[1],
        #             shop_id=2)
        #         index += 1

        dict = {}
        url = 'https://www.pizzatempo.by/menu/pizza.html'
        r = requests.get(url)
        with open('tempo.html', 'w', encoding='utf-8') as output_file:
            output_file.write(r.text)
        html = open('tempo.html', "r", encoding='utf-8').read()
        name_piz = []
        img_piz = []
        descr_piz = []
        soup = BeautifulSoup(html, 'lxml')
        div = soup.find_all('div', class_=[
            'item group1 novinka_1', 'item group1 novinka_',
            'item group2 novinka_',
            'item group3 novinka_'
        ])
        for pizza in div:
            name = pizza.find('h3').find('span').next_element
            name_piz.append(name)
            image = pizza.find('div', class_='info').find(
                'div', class_='photo').find('img')
            link = image.get('src')
            img_piz.append(link)
            description = pizza.find('div', class_='info').find(
                'div', class_='photo').find(
                'div', class_='composition_holder').find(
                'div', class_='composition').next_element
            descr_piz.append(description)
        index = 0
        img_piz1 = []
        img_piz2 = []
        descr_piz1 = []
        result_list = []
        while index < len(img_piz):
            img_piz1.append('check/tempo{}.jpg'.format(index))
            img_piz2.append('tempo{}.jpg'.format(index))
            descr_piz1.append(descr_piz[index][6:-5])
            array = []
            array.append(name_piz[index])
            array.append(img_piz1[index])
            array.append(descr_piz1[index])
            array.append(img_piz[index])
            array.append('tempo')
            dict1 = {'number': index, 'name': name_piz[index],
                     'image': img_piz1[index]
                , 'description': descr_piz1[index], 'img_url': img_piz[index]
                , 'shop': 'tempo', 'shop_id': 1}
            result_list.append(dict1)
            index += 1

        url = 'https://dominos.by/ru/Pizza/'
        r = requests.get(url)
        with open('dominos.html', 'w', encoding='utf-8') as output_file:
            output_file.write(r.text)
        html = open('dominos.html', "r", encoding='utf-8').read()
        name_piz = []
        img_piz = []
        descr_piz = []
        soup = BeautifulSoup(html, 'lxml')
        div = soup.find_all('div', class_='product_item')
        for pizza in div:
            name = pizza.find('p').find('a')
            if name is not None:
                name = name.next_element.lstrip()
                name_piz.append(name)
            image = pizza.find('div', class_='product_img_holder')
            if image is not None:
                image = image.find('a').find('img')
                link = image.get('src')
                img_piz.append(link)
            description = pizza.find('div', class_='product_mix')
            if description is not None:
                description = description.find('p').next_element
                descr_piz.append(description)
        index = 0
        img_piz1 = []
        img_piz2 = []
        descr_piz1 = []
        while index < len(img_piz):
            img_piz1.append('check/dominos{}.jpg'.format(index))
            img_piz2.append('dominos{}.jpg'.format(index))
            descr = ' '.join(descr_piz[index].split()).lower()
            descr_piz1.append(descr)
            array = []
            array.append(name_piz[index][0:-9])
            array.append(img_piz1[index])
            array.append(descr_piz1[index])
            array.append('https://dominos.by/' + img_piz[index])
            array.append('dominos')
            dict1 = {'number': index, 'name': name_piz[index][0:-9],
                     'image': img_piz1[index]
                , 'description': descr_piz1[index],
                     'img_url': 'https://dominos.by/' + img_piz[index]
                , 'shop': 'dominos', 'shop_id': 3}
            result_list.append(dict1)
            index += 1

        driver = webdriver.Chrome(
            executable_path='C:\\Users\Dmitry\PycharmProjects\\'
                            'untitled2\PizzaSearch\chromedriver.exe')
        driver.get('https://pzz.by/pizzas')
        result = driver.find_elements_by_class_name('pizzas-block')
        name = [
            res.text for result in result for res in
            result.find_elements_by_tag_name('a') if res.text != '']
        image = [
            res.get_attribute('src') for result in result for res in
            result.find_elements_by_tag_name('img')]
        description = [
            res.text for result in result for result1 in
            result.find_elements_by_class_name('goods__list__text') for res in
            result1.find_elements_by_tag_name('p')]
        if len(name) == len(image) and len(description) == len(description):
            index = 0
            img_piz1 = []
            img_piz2 = []
            while index < len(name):
                img_piz1.append('check/pzz{}.jpg'.format(index))
                img_piz2.append('pzz{}.jpg'.format(index))
                array = []
                array.append(name[index])
                array.append(img_piz1[index])
                array.append(description[index])
                array.append(image[index])
                array.append('pzz')
                dict1 = {'number': index,
                         'name': name[index], 'image': img_piz1[index]
                    , 'description': description[index], 'img_url': image[index]
                    , 'shop': 'pzz', 'shop_id': 2}
                result_list.append(dict1)
                index += 1

        url = 'http://presto-pizza.by/group/1/1/'
        r = requests.get(url)
        with open('presto.html', 'w', encoding='utf-8') as output_file:
            output_file.write(r.text)
        html = open('presto.html', "r", encoding='utf-8').read()
        name_piz = []
        img_piz = []
        descr_piz = []
        soup = BeautifulSoup(html, 'lxml')
        h3 = soup.find_all('h3')
        for pizza in h3:
            name_piz.append(pizza.next_element)
        span = soup.find_all('div', class_='views-field views-field-php-1')
        for span in span:
            span1 = span.find_all('span', class_='field-content')
            for descr in span1:
                descr_piz.append(descr.next_element[0:-26].lower())
        span = soup.find_all('div', class_='views-field views-field-php')
        for span in span:
            image = span.find('span', class_='field-content').find('img')
            if image is not None:
                link = image.get('img')
                img_piz.append(link)
        index = 0
        img_piz1 = []
        img_piz2 = []
        descr_piz1 = []
        while index < len(img_piz):
            img_piz1.append('check/presto{}.jpg'.format(index))
            img_piz2.append('presto{}.jpg'.format(index))
            descr = ' '.join(descr_piz[index].split()).lower()
            descr_piz1.append(descr)
            array = []
            array.append(name_piz[index])
            array.append(img_piz1[index])
            array.append(descr_piz1[index])
            array.append(img_piz[index])
            array.append('presto')
            dict1 = {'number': index, 'name': name_piz[index],
                     'image': img_piz1[index]
                , 'description': descr_piz1[index],
                     'img_url': img_piz[index]
                , 'shop': 'presto', 'shop_id': 6}
            result_list.append(dict1)
            index += 1


        def download(**kwargs):
            with open(
                    'C:\\Users\Dmitry\PycharmProjects\\untitled2'
                    '\PizzaSearch\static\media\check\{}{}.jpg'.format(
                        kwargs['shop'], kwargs['number']), 'wb') as img:
                img.write(urlopen(kwargs['img_url']).read())
                PizzaCheck.objects.create(
                    name=kwargs['name'], description=kwargs['description'],
                    image=kwargs['image'], shop_id=kwargs['shop_id'])

        threads = []
        for dicts in result_list:
            t = threading.Thread(target=download, kwargs=dicts)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()


        cursor = connection.cursor()
        cursor.execute('''select p.id, p.name, p.shop_id, s.website,s.name
                from public."PizzaSearch_pizza" p 
                left join public."PizzaSearch_pizzacheck" p1 on p.name = p1.name
                          and p.shop_id = p1.shop_id
                join public."PizzaSearch_shop" s on s.id = p.shop_id                 
                where p1.name is null and p.on_sale=TRUE ''')
        row = cursor.fetchall()
        cursor.execute('''select p1.id, p1.name, p1.shop_id, s.website,s.name
                        from public."PizzaSearch_pizza" p 
                        right join public."PizzaSearch_pizzacheck" p1 on p.name = p1.name
                                  and p.shop_id = p1.shop_id
                        join public."PizzaSearch_shop" s on s.id = p1.shop_id                 
                        where p.name is null ''')
        row_add = cursor.fetchall()
        cursor.execute('''select p.id, p.name, p.shop_id, s.website,s.name
                                from public."PizzaSearch_pizza" p 
                                join public."PizzaSearch_pizzacheck" p1 on p.name = p1.name
                                          and p.shop_id = p1.shop_id
                                join public."PizzaSearch_shop" s on s.id = p.shop_id                 
                                where p.on_sale=FALSE ''')
        row_sale = cursor.fetchall()
        return render(request, 'autamatic_check.html', {
            'row': row, 'row_add': row_add, 'row_sale': row_sale
        })
    # делает пиццу неактивной
    elif request.method == 'POST' and 'delete' in request.POST:
        Pizza.objects.filter(id=request.POST.get('delete')).update(
            on_sale=False
        )
        cursor = connection.cursor()

        cursor.execute('''select p.id, p.name, p.shop_id, s.website
            from public."PizzaSearch_pizza" p 
            left join public."PizzaSearch_pizzacheck" p1 on p.name = p1.name
                      and p.shop_id = p1.shop_id
            join public."PizzaSearch_shop" s on s.id = p.shop_id                 
            where p1.name is null and p.on_sale=TRUE ''')
        row = cursor.fetchall()
        cursor.execute('''select p1.id, p1.name, p1.shop_id, s.website,s.name
            from public."PizzaSearch_pizza" p 
            right join public."PizzaSearch_pizzacheck" p1 on p.name = p1.name
                      and p.shop_id = p1.shop_id
            join public."PizzaSearch_shop" s on s.id = p1.shop_id                 
            where p.name is null ''')
        row_add = cursor.fetchall()
        cursor.execute('''select p.id, p.name, p.shop_id, s.website,s.name
                from public."PizzaSearch_pizza" p 
                join public."PizzaSearch_pizzacheck" p1 on p.name = p1.name
                          and p.shop_id = p1.shop_id
                join public."PizzaSearch_shop" s on s.id = p.shop_id                 
                where p.on_sale=FALSE ''')
        row_sale = cursor.fetchall()
        return render(request, 'autamatic_check.html', {
            'row': row, 'row_add': row_add, 'row_sale': row_sale})
    # добавляет новую пиццу
    elif request.method == 'POST' and 'add' in request.POST:

        pizza = PizzaCheck.objects.get(id=request.POST.get('add'))
        if pizza.shop_id == 1:
            new_img = 'tempo'
        elif pizza.shop_id == 2:
            new_img = 'dominos'
        elif pizza.shop_id == 3:
            new_img = 'pzz'

        max_id = Pizza.objects.aggregate(max_id=Max('id')).get('max_id')
        new_id = max_id + 1
        shutil.copy2('C:\\Users\Dmitry\PycharmProjects\\untitled2\PizzaSearch'
                     '\static\media\{}'.format(pizza.image),
                     'C:\\Users\Dmitry\PycharmProjects\\untitled2\PizzaSearch'
                     '\static\media\items/{}{}.jpg'.format(new_img, new_id))
        new_image = 'items/{}{}.jpg'.format(new_img, new_id)
        Pizza.objects.create(
            name=pizza.name,
            description=pizza.description,
            image=new_image,
            shop_id=pizza.shop_id,
            on_sale=True
        )
        cursor = connection.cursor()
        cursor.execute('''select p.id, p.name, p.shop_id, s.website
            from public."PizzaSearch_pizza" p 
            left join public."PizzaSearch_pizzacheck" p1 on p.name = p1.name
                      and p.shop_id = p1.shop_id
            join public."PizzaSearch_shop" s on s.id = p.shop_id                 
            where p1.name is null and p.on_sale=TRUE ''')
        row = cursor.fetchall()
        cursor.execute('''select p1.id, p1.name, p1.shop_id, s.website,s.name
            from public."PizzaSearch_pizza" p 
            right join public."PizzaSearch_pizzacheck" p1 on p.name = p1.name
                      and p.shop_id = p1.shop_id
            join public."PizzaSearch_shop" s on s.id = p1.shop_id                 
            where p.name is null ''')
        row_add = cursor.fetchall()
        cursor.execute('''select p.id, p.name, p.shop_id, s.website,s.name
                from public."PizzaSearch_pizza" p 
                join public."PizzaSearch_pizzacheck" p1 on p.name = p1.name
                          and p.shop_id = p1.shop_id
                join public."PizzaSearch_shop" s on s.id = p.shop_id                 
                where p.on_sale=FALSE ''')
        row_sale = cursor.fetchall()
        return render(request, 'autamatic_check.html', {
            'row': row, 'row_add': row_add, 'row_sale': row_sale})
    # делает пиццу вновь активной
    elif request.method == 'POST' and 'on_sale' in request.POST:
        Pizza.objects.filter(id=request.POST.get('on_sale')).update(
            on_sale=True
        )
        cursor = connection.cursor()
        cursor.execute('''select p.id, p.name, p.shop_id, s.website
            from public."PizzaSearch_pizza" p 
            left join public."PizzaSearch_pizzacheck" p1 on p.name = p1.name
                      and p.shop_id = p1.shop_id
            join public."PizzaSearch_shop" s on s.id = p.shop_id                 
            where p1.name is null and p.on_sale=TRUE ''')
        row = cursor.fetchall()
        cursor.execute('''select p1.id, p1.name, p1.shop_id, s.website,s.name
            from public."PizzaSearch_pizza" p 
            right join public."PizzaSearch_pizzacheck" p1 on p.name = p1.name
                      and p.shop_id = p1.shop_id
            join public."PizzaSearch_shop" s on s.id = p1.shop_id                 
            where p.name is null ''')
        row_add = cursor.fetchall()
        cursor.execute('''select p.id, p.name, p.shop_id, s.website,s.name
                from public."PizzaSearch_pizza" p 
                join public."PizzaSearch_pizzacheck" p1 on p.name = p1.name
                          and p.shop_id = p1.shop_id
                join public."PizzaSearch_shop" s on s.id = p.shop_id                 
                where p.on_sale=FALSE ''')
        row_sale = cursor.fetchall()
        return render(request, 'autamatic_check.html', {
            'row': row, 'row_add': row_add, 'row_sale': row_sale})
    return render(request, 'autamatic_check.html')
