from django.urls import path
from .views import CartAPIView, UpdateCart ,AddToCart

urlpatterns = [
    path('cart/', CartAPIView.as_view()),
    # path('cart_create/', CartCreateAPIView.as_view()),
    path('cart/<int:pk>/', UpdateCart.as_view()),
    path('add_cart/<int:pk>/', AddToCart.as_view()),
]