from django.contrib import admin

from .models import City, Customer, Product, Marketplace, Courier, Transaction, Purchase


class PurchasesInLine(admin.StackedInline):
    model = Purchase
    extra = 1


class TransactionAdmin(admin.ModelAdmin):
    inlines = [PurchasesInLine]


admin.site.register(City)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Marketplace)
admin.site.register(Courier)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Purchase)
