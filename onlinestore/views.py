from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
# Create your views here.
def store(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request,'onlinestore/store.html',context)
def cart(request):
    context={}
    return render(request,'onlinestore/cart.html',context)

def checkout(request):
    context={}
    return render(request,'onlinestore/checkout.html',context)
def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print(productId,action)
    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)
    return JsonResponse('Data was added',safe=False)

    