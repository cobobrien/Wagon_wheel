from collections import defaultdict

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import SignUpForm
from .models import Category, Type, Price, Extra, Topping, CartItem, Order
from django.http import JsonResponse
import logging
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def index(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    menu = {}
    toppings_dict = {}
    order_cart_items = {}
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
                        menu[cat.name][type.name]["large_price"] = "{:.2f}".format(float(type.price.get(size="Large").price))
                    except:
                        pass
                    try:
                        menu[cat.name][type.name]["small_price"] = "{:.2f}".format(float(type.price.get(size="Small").price))
                    except:
                        pass
                    try:
                        menu[cat.name][type.name]["one_price"] = "{:.2f}".format(float(type.price.get(size="N/A").price))
                    except:
                        pass

    for extra in extras:
        extras_dict.setdefault(extra.name, {})["id"] = extra.id
        extras_dict[extra.name]["price"] = "{:.2f}".format(float(extra.price))

    for topping in toppings:
        toppings_dict[topping.name] = topping.id

    try:
        order = Order.objects.get(user=request.user, status="Pending")
    except:
        logger.info("No order on server")
    if(order):
        for cart in order.cart_items.all():
            order_cart_items.setdefault(cart.item.name, {})["price"] = cart.price
            if (cart.extras.all()):
                order_cart_items[cart.item.name]= []
                for extra in cart.extras.all():
                    order_cart_items[cart.item.name].append(extra.name)
            if (cart.toppings.all()):
                order_cart_items[cart.item.name] = []
                for topping in cart.toppings.all():
                    order_cart_items[cart.item.name].append(topping.name)


    context = {
        "menu": menu,
        "extras": extras_dict,
        "toppings": toppings_dict,
        "order": order_cart_items
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

def cart(request):
    logger.info("User: {}".format(request.user))

    item_size = request.POST.get("item_size")
    item_id = request.POST.get("item_id")
    try:
        item = Type.objects.get(id=item_id)
        main = item.category
        try:
            order = Order.objects.get(user=request.user, status="Pending")
        except:
            order = Order.objects.create(user=request.user)
        logger.info("Order: {}".format(order))
        cart = CartItem.objects.create(item=item, order=order, user=request.user, size=item_size, main=main)
    except:
        return JsonResponse({"success": False})
    return JsonResponse({"success": True, "cart_item": item.name, "price": cart.price, "order_items": order.cart_items.count(), "order_total": order.total})

