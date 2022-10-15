from django.shortcuts import render
from .serializers import ProductSerializer , CategorySerializer , ReviewSerializer ,ProductWriteSerializer
from .models import Category , Product , Review
from rest_framework import generics , permissions , viewsets ,views


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return ProductWriteSerializer
        return ProductSerializer

    def get_permissions(self):
        if self.action in ("create", 'update', 'partial_update', 'destroy'):
            self.permission_classes = (permissions.IsAuthenticated, )
        else:
            self.permission_classes = (permissions.AllowAny, )
        return super().get_permissions()


class RelatedProductView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id, *args, **kwargs):
        product_id = id 
        print(id)
        if not product_id:
            return Response({"error": "Product Id Not Found"}, status=400)
        product = get_object_or_404(Product, id=product_id)
        products_serialized = ProductSerializer(
            product.get_related_products(), many=True, context={'request': request})
        return Response(products_serialized.data)

    @classmethod
    def get_extra_actions(cls):
        return []