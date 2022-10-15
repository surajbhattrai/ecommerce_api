from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property

from products.models import Product
from account.models import User



class Order(models.Model):
    PENDING = 'P'
    COMPLETED = 'C'
    STATUS_CHOICES = ((PENDING, _('pending')), (COMPLETED, _('completed')))

    buyer = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.buyer.get_full_name()

    @cached_property
    def total_cost(self):
        return round(sum([order_item.cost for order_item in self.order_items.all()]), 2)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="product_orders", on_delete=models.CASCADE)
    quantity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.order.buyer.get_full_name()

    @cached_property
    def cost(self):
        return round(self.quantity * self.product.price, 2)