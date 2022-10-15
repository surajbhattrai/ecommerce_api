from django.db import models
from account.models import User
from django.urls import reverse
from django.db.models import Avg, Count
from os import path
from random import randint
from django.db.models.signals import pre_save

from ecommerce_api.utils import unique_slug_generator
from ecommerce_api.settings import MEDIA_URL



def get_filename_ext(filename):
    filepath = path.basename(filename)
    name, ext = path.splitext(filepath)
    return name, ext

def upload_name_path(instance, filename):
    folderName = randint(1, 40000000)
    filenam = randint(1, folderName)
    ext = get_filename_ext(filename)[1]
    return f'products/{folderName}/{filenam}.{ext}'



class Category(models.Model):
    name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])    

    class Meta:
        verbose_name = 'catgory'
        verbose_name_plural = 'categories'  




class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def filter_products(self, keyword, sort, min_price, max_price):
        qs = self.get_queryset()
        if keyword:
            qs = qs.filter(product_name__icontains=keyword).distinct()
        if sort:
            sort = int(sort)
            if sort == 2:
                qs = qs.order_by('-price')
            elif sort == 1:
                qs = qs.order_by('price')
        if max_price:
            max_price = int(max_price)
            qs = qs.filter(price__lt=max_price)
        if min_price:
            min_price = int(min_price)
            qs = qs.filter(price__gt=min_price)
        return qs

    def get_products(self):
        return self.get_queryset()




class Product(models.Model):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=2000,blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to=upload_name_path, blank=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date  = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    objects = ProductManager()
    
    class Meta:
        ordering = ('-created_date',)


    def get_related_products(self):
        product_name_split = self.product_name.split(' ')
        lookups = Q(product_name__icontains=product_name_split[0])
        for i in product_name_split[1:]:
            lookups |= Q(product_name__icontains=i)
        related_products = Product.objects.filter(lookups).distinct().exclude(id=self.id)
        return related_products

    
    def avarageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(avarage=Avg('rating'))
        avg = 0
        if reviews['avarage'] is not None:
            avg = float(reviews['avarage'])
        return avg

    def countReview(self):
         reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
         count = 0
         if reviews['count'] is not None:
             count = int(reviews['count'])
         return count

    def get_image_url(self):
        return f'{MEDIA_URL}{self.image}'

    def __str__(self):
        return self.product_name

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(product_pre_save_receiver, sender=Product)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user
     

    
