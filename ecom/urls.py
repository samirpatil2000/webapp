
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
   path('shop/<slug>',views.ProductDeatilFBView,name='shop-detail')
]