from urllib.request import urlopen

import requests
from django.contrib.auth.models import User
from django.db.models import Avg
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import login, logout
from bs4 import BeautifulSoup
from PizzaSearch.models import Pizza, Mark


def index(request):
    piz = Pizza.objects.all
    return render(request, 'index.html', {'piz': piz})


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
    url = 'https://www.pizzatempo.by/menu/pizza.html'
    r = requests.get(url)
    with open('test.html', 'w', encoding='utf-8') as output_file:
        output_file.write(r.text)
    html = open('test.html', "r", encoding='utf-8').read()
    name_piz = []
    img_piz = []
    descr_piz = []
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find_all('div', class_=[
        'item group1 novinka_1', 'item group1 novinka_', 'item group2 novinka_',
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
    result = []
    while index < len(img_piz):
        # with open(
        #         'C:\\Users\Dmitry\PycharmProjects\\untitled2\PizzaSearch\static\media\items\\tempo{}.jpg'.format(
        #             index), 'wb') as img:
        #     img.write(urlopen(img_piz[index]).read())
        img_piz1.append('items/tempo{}.jpg'.format(index))
        img_piz2.append('tempo{}.jpg'.format(index))
        descr_piz1.append(descr_piz[index][6:-5])
        array = []
        array.append(name_piz[index])
        array.append(img_piz1[index])
        array.append(descr_piz1[index])
        result.append(array)

        # Pizza.objects.create(
        #     name = array[0], description = array[2], image = array[1],
        # shop_id=1)
        index += 1
    # image = urlopen(img_piz[0])
    # Pizza.objects.get(id=1).image.save(
    #     '{}'.format(img_piz2[0]), image)
    return render(request, 'autamatic_search_data.html', {'res':result})

def pizzas(request):
    piz = Pizza.objects.all
    return render(request, 'pizzas.html', {'piz':piz})

def pizza(request, pizza_id):
    if request.method == 'GET':
        piza = Pizza.objects.filter(id=int(pizza_id)).all
        average_mark = Mark.objects.filter(
            pizza_id=pizza_id).aggregate(Avg('mark'))
        number = [value for key, value in average_mark.items()]
        if number[0] is not None:
            rating = round(number[0],2)
        else:
            rating = 0
        return render(request, 'pizza.html', {
            'piz':piza,  'num': rating})
    elif request.method == 'POST':
        Mark.objects.create(
            mark=request.POST.get('rating'),
            user_id=request.user.id,
            pizza_id=pizza_id )
        return redirect('pizza', pizza_id)