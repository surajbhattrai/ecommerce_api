from django.shortcuts import get_object_or_404
from rest_framework import views , response, permissions , generics ,mixins
from products.models import Product
from .models import Cart, CartItem
from .serializers import CartSerializer , CartItemSerializer


class CartAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.get(user=user.id)



# class AddCartAPIView(generics.ListCreateAPIView):
#     serializer_class = CartItemSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         cart_obj, _ = Cart.objects.get_existing_or_new(request)
#         return CartItem.objects.get(cart=cart)



# class CartAPIView(generics.ListCreateAPIView):
#     serializer_class = CartSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         cart_obj, _ = Cart.objects.get_existing_or_new(request)
#         context = {'request': request}
#         serializer = CartSerializer(cart_obj, context=context)
#         return response.Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         product_id = request.data.get("id")
#         quantity = int(request.data.get("quantity", 1))

#         product_obj = get_object_or_404(Product, pk=product_id)
#         cart_obj, _ = Cart.objects.get_existing_or_new(request)

#         if quantity <= 0:
#             cart_item_qs = CartItem.objects.filter(cart=cart_obj, product=product_obj)
#             if cart_item_qs.count != 0:
#                 cart_item_qs.first().delete()
#         else:
#             cart_item_obj, created = CartItem.objects.get_or_create(
#                 product=product_obj, cart=cart_obj)
#             cart_item_obj.quantity = quantity
#             cart_item_obj.save()

#         serializer = CartSerializer(cart_obj, context={'request': request})
#         return response.Response(serializer.data)


# class CheckProductInCart(views.APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, *args, product_id, **kwargs):
#         product_obj = get_object_or_404(Product, pk=product_id)
#         cart_obj, created = Cart.objects.get_existing_or_new(request)
#         return Response(not created and CartItem.objects.filter(cart=cart_obj, product=product_obj).exists())

class UpdateCart(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    # def list(self, request, product_id):
    #     product_obj = get_object_or_404(Product, pk=product_id)
    #     cart_obj, created = Cart.objects.get_existing_or_new(request)
    #     queryset = CartItem.objects.filter(cart=cart_obj, product=product_obj)
    #     serializer = CartItemSerializer(queryset, many=True)
    #     return response.Response(serializer.data)

    # def get_queryset(self, product_id):
    #     product_obj = get_object_or_404(Product, pk=product_id)
    #     cart_obj, created = Cart.objects.get_existing_or_new(request)
    #     return 

    # def get(self, request, *args, product_id, **kwargs):
    #     product_obj = get_object_or_404(Product, pk=product_id)
    #     cart_obj, created = Cart.objects.get_existing_or_new(request)
    #     return response.Response(not created and CartItem.objects.filter(cart=cart_obj, product=product_obj).exists())



class AddToCart(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get(self, request, *args, pk, **kwargs):
        product_obj = get_object_or_404(Product, pk=pk)
        cart_obj, created = Cart.objects.get_existing_or_new(request)
        return response.Response(not created and CartItem.objects.filter(cart=cart_obj, product=product_obj).exists())