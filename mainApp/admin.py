from django.contrib import admin
from .models import *
admin.site.register((Flavour,CakeType,Shape,Product,Buyer,Wishlist,Checkout,CheckoutProducts,Contact))
# Register your models here.
