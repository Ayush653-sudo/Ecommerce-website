from django.contrib import admin
from django.urls import path,include
from .views import index,signup,login,logout,cart,checkout,ordered

urlpatterns = [
path('',index ,name='jjh'),
path('signup' , signup),
path('login',login),
path('logout',logout),
path('cart',cart),
path('checkout',checkout),
path('ordered',ordered),

]