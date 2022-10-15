from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from orders.models import Order, OrderItem
from orders.permissions import IsOrderByBuyerOrAdmin, IsOrderItemByBuyerOrAdmin, IsOrderItemPending, IsOrderPending
from .serializers import OrderItemSerializer, OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsOrderItemByBuyerOrAdmin]

    def get_queryset(self):
        res = super().get_queryset()
        order_id = self.kwargs.get('order_id')
        return res.filter(order__id=order_id)

    def perform_create(self, serializer):
        order = get_object_or_404(Order, id=self.kwargs.get('order_id'))
        serializer.save(order=order)

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            self.permission_classes += [IsOrderItemPending]
        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsOrderByBuyerOrAdmin]
    serializer_class =  OrderSerializer

    # def get_serializer_class(self):
    #     if self.action in ('create', 'update', 'partial_update', 'destroy'):
    #         return OrderWriteSerializer
    #     return OrderReadSerializer

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(buyer=user)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes += [IsOrderPending]
        return super().get_permissions()