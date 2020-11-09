
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

   #testing for mobile view
   path('mobile/',views.mobile_view,name='mobile_view'),

   # update/use address from list
   path('update_address/<id>',views.update_detail_address,name='update_detail_address'),
   path('use_address/<id>',views.use_address,name='use_address'),

   # delete address
   path('delete_address/<id>',views.delete_address,name='delete_address'),


   # Related to oder history
   path('order_history/',views.order_history,name='order_history'),
   path('order_history/<id>',views.order_history_detailview,name='order_history_detailview'),

   #all transactions
   path('transactions/',views.transactions,name='trans'),

   #ip address
   path('get_ip/',views.get_ip,name='ip_address'),

   #user address
   path('save_address/',views.user_address,name='save_address'),

   #create address
   path('create_address',views.create_address,name='create_address'),


   #payment option
   # path('payment_option/cash-on-delivery', views.confirmation_page_cod_order, name='confirmation_page_cod_order')

   #ordered placed
   # path('place_order/',views)




]