from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

def home(request):
    context = {}
    return render(request, 'store/home.html', context)

def products(request):
    products = Product.objects.all
    context =  {'products':products}
    return render(request, 'store/products.html', context)

def product_details(request):
    context = {}
    return render(request, 'store/product_details.html', context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_subtotal':0, 'get_cart_gst':0, 'get_cart_total':0}
        
    context = {'items':items, 'order':order}
    return render(request, 'store/cart.html', context)


def updateItem(request):
    data = json.loads(request.data)
    productId = data['productId']
    action = data['action']
    print('Action: ', action)
    print('productId: ', productId)
    return JsonResponse('Item was added', safe=False)