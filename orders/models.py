from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

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

class Topping(models.Model):
    name = models.CharField(max_length=100)
    pizza = models.ManyToManyField(Type, through='P_Membership', related_name='toppings')


    def __str__(self):
        return f"{self.name}"


class Extra(models.Model):
    name = models.CharField(max_length=100)
    sub = models.ManyToManyField(Type, blank=True,through='S_Membership')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}"

class P_Membership(models.Model):
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Type, on_delete=models.CASCADE)
    main = models.ForeignKey(Category, on_delete=models.CASCADE)

class S_Membership(models.Model):
    topping = models.ForeignKey(Extra, on_delete=models.CASCADE)
    sub_item = models.ForeignKey(Type, on_delete=models.CASCADE)
    main = models.ForeignKey(Category, on_delete=models.CASCADE)