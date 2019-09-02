from django.contrib import admin

from django.contrib import admin

from .models import Category, Type, Price, Topping, Extra, Order, CartItem


# class PizzaToppingInline(admin.StackedInline):
#     model = Pizza_topping.items.through
#     extra = 1
#
# class SubtoppingInline(admin.StackedInline):
#     model = Sub_topping.items.through
#     extra = 1
#
#
# class SubAdmin(admin.ModelAdmin):
#     inlines = [PizzaToppingInline, SubtoppingInline]
#
#


admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Price)
admin.site.register(Topping)
admin.site.register(Extra)
admin.site.register(Order)
admin.site.register(CartItem)

