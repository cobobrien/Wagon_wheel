from django.contrib import admin

from django.contrib import admin

from .models import Category, Type, Price, Topping, Extra, S_Membership, P_Membership


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
admin.site.register(P_Membership)
admin.site.register(S_Membership)
admin.site.register(Price)
admin.site.register(Topping)
admin.site.register(Extra)

