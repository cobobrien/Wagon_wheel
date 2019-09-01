from collections import defaultdict

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import SignUpForm
from .models import Category, Type, Price, Extra, Topping


# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    menu = {}
    toppings_dict = {}
    extras_dict = {}
    types = Type.objects.all()
    categories = Category.objects.all()
    extras = Extra.objects.all()
    toppings = Topping.objects.all()

    for cat in categories:
            for type in types:
                if type.category == cat:
                    menu.setdefault(cat.name, {}).setdefault(type.name, {})["id"] = type.id
                    try:
                        menu[cat.name][type.name]["large_price"] = float(type.price.get(size="Large").price)
                    except:
                        print("no price for large")
                    try:
                        menu[cat.name][type.name]["small_price"] = float(type.price.get(size="Small").price)
                    except:
                        print("no price for small")
                    try:
                        menu[cat.name][type.name]["one_price"] = float(type.price.get(size="N/A").price)
                    except:
                        print("no price for n/a")

    for extra in extras:
        extras_dict.setdefault(extra.name, {})["id"] = extra.id
        extras_dict[extra.name]["price"] = float(extra.price)

    for topping in toppings:
        toppings_dict[topping.name] = topping.id

    context = {
        "menu": menu,
        "extras": extras_dict,
        "toppings": toppings_dict
    }
    return render(request, "orders/menu.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out."})

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'users/register.html', {'form': form})
