from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet , RelatedProductView , ProductViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path("related/<id>/", RelatedProductView.as_view())
]


 