from django.urls import path
from .views import (
    HomeView,
    add_to_cart,
    remove_from_cart,
    CheckoutView,
    StatusOrderedView,
    K,
    KT,
    Search,
    remove_single_item_from_cart,
    OrderSummaryView,
    ItemDetailView
)
app_name = 'store'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('StatusOrderedView/', StatusOrderedView.as_view(), name='StatusOrderedView'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('search/', Search.as_view(), name='Search'),
    path('S1/', K.as_view(), name='K'),
    path('S2/', KT.as_view(), name='KT'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product')
   
]