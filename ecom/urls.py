
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from. import views
from.views import HomeView,ProductListView,ProductDetailView,ShoppingCart
urlpatterns = [
   #path('',HomeView.as_view(),name='index'),
   path('',views.search,name='index'),
   #path('shop/', ProductListView.as_view(), name='shop'),
   path('shop/', views.productList, name='shop'),
   #path('shop/<slug>',ProductDetailView.as_view(),name='shop-detail')
   path('shop/<slug>',views.ProductDeatilFBView,name='shop-detail'),
   path('add_to_cart/<slug>',views.add_to_cart,name='add_to_cart'),
   path('remove_from_cart/<slug>',views.remove_from_cart,name='remove_from_cart'),
   path('add_to_cart_with_number/<slug>',views.add_to_cart_with_number,name='add_to_cart_with_number'),

   #path('cart/',ShoppingCart.as_view(),name='cart')
   path('cart/',views.shoppingCart,name='cart'),

   # Favourites
   path('add_to_fav/<slug>',views.add_to_fav,name='add_to_fav'),
   path('remove_from_fav/<slug>',views.remove_from_fav,name='remove_from_fav'),
   path('favlist/',views.favList,name='favlist'),

   # add/remove single product
   path('add_single_item_to_cart/<slug>', views.add_single_item_to_cart, name='add_single_to_cart'),
   path('remove_single_item_from_cart/<slug>', views.remove_single_item_from_cart, name='remove_single_from_cart'),

   # category
   path('cat/<slug>',views.category_detail,name='category_detail'),

   # checkout
   path('checkout/',views.checkoutPage,name='checkout'),



]