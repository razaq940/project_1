from django.urls import path
from .views import (
    HomeView,
    add_to_cart,
    remove_from_cart,
    CheckoutView,
    StatusOrderedView,
    S,
    SF,
    SO,
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
    path('S1/', S.as_view(), name='S'),
    path('S2/', SO.as_view(), name='SO'),
    path('S3/', SF.as_view(), name='SF'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product')
   
]