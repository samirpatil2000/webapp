
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from. import views
from.views import HomeView,ProductList,ProductDetailView
urlpatterns = [
   path('',HomeView.as_view(),name='index'),
   path('shop/',ProductList.as_view(),name='shop'),
   #path('shop/<slug>',ProductDetailView.as_view(),name='shop-detail')
   path('shop/<slug>',views.ProductDeatilFBView,name='shop-detail'),
   path('add_to_cart/<slug>',views.add_to_cart,name='add_to_cart'),
   path('remove_from_cart/<slug>',views.remove_from_cart,name='remove_from_cart'),
   path('add_to_cart_with_number/<slug>',views.add_to_cart_with_number,name='add_to_cart_with_number'),

]