from unicodedata import decimal
from django.db.models.signals import m2m_changed
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        managed = True

class Type(models.Model):

    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    TOPPING_NUMBER = (
        (ZERO, 'Zero'),
        (ONE, 'One'),
        (TWO, 'Two'),
        (THREE, 'Three'),
        (FOUR, 'Four'),
    )

    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="type")
    topping_number_allowed = models.IntegerField(choices=TOPPING_NUMBER, default=ZERO)

    def __str__(self):
        return f"{self.category} - {self.name}. Allowed: {self.topping_number_allowed} toppings"

    class Meta:
        managed = True

class Price(models.Model):

    Not_applicable = "N/A"
    SMALL = "Small"
    LARGE = "Large"
    DISH_SIZE = (
        (Not_applicable, 'N/A'),
        (SMALL, 'Small'),
        (LARGE, 'Large'),
    )
    size = models.CharField(max_length=10, choices=DISH_SIZE, default=Not_applicable)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dish = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="price")

    def __str__(self):
        return f"{self.dish} - {self.size} costs {self.price}"

    class Meta:
        managed = True

class Order(models.Model):
    PENDING = "Pending"
    SUBMITTED = "Submitted"
    COMPLETE = "Complete"
    ORDER_STATUS = (
        (PENDING, 'Pending'),
        (SUBMITTED, 'Submitted'),
        (COMPLETE, 'Complete'),
    )
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default=PENDING)

    @property
    def total(self):
        return sum(item.price for item in self.cart_items.all())

    @property
    def total2(self):
        return self.cart_items.all().aggregate(Sum('total_price'))['total_price__sum'] or decimal(0.00)

    class Meta:
        managed = True

class Topping(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        managed = True

class Extra(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        managed = True


class CartItem(models.Model):
    item = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='orders')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='cart_items')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    main = models.ForeignKey(Category, on_delete=models.CASCADE)
    extras = models.ManyToManyField(Extra, blank=True, related_name='cart_items')
    toppings = models.ManyToManyField(Topping, blank=True, related_name='cart_items')

    Not_applicable = "N/A"
    SMALL = "Small"
    LARGE = "Large"
    DISH_SIZE = (
        (Not_applicable, 'N/A'),
        (SMALL, 'Small'),
        (LARGE, 'Large'),
    )
    size = models.CharField(max_length=10, choices=DISH_SIZE, default=Not_applicable)

    @property
    def price(self):
        item_price=Price.objects.get(size=self.size, dish=self.item).price
        try:
            extras = self.extras.all().aggregate(Sum('price'))['price__sum'] or decimal(0.00)
        except:
            return item_price
        else:
            return item_price + extras

        class Meta:
            managed = True

def set_total_price(sender, instance, **kwargs):
    item_price=Price.objects.get(size=instance.size, dish=instance.item).price
    try:
        extras = instance.extras.all().aggregate(Sum('price'))['price__sum'] or decimal(0.00)
    except:
        instance.total_price = item_price
    else:
        instance.total_price = item_price + extras

pre_save.connect(set_total_price, sender=CartItem)


def toppings_changed(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    if action == "pre_add":
        if "Pizza" not in instance.main.name:
            raise ValidationError(
                _('Toppings can only go on Pizzas'),
            )


m2m_changed.connect(toppings_changed, sender=CartItem.toppings.through)

def extras_changed(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    if action == "pre_add":
        if instance.main.name != "Sub":
            raise ValidationError(
                _('Extras can only be added to Subs'),
            )


m2m_changed.connect(extras_changed, sender=CartItem.extras.through)