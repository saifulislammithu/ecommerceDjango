from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
import datetime
from .utils import cookieCart,cartData,guestOrder
# Create your views here.
def index(request):
    user=request.user
    context={'user':user}
    return render(request,'onlinestore/home.html',context)
def store(request):
    data=cartData(request)
    cartItem=data['cartItem']
    products=Product.objects.all()
    context={'products':products,'cartItem':cartItem}
    return render(request,'onlinestore/store.html',context)
def cart(request):
    data=cartData(request)
    order=data['order']
    items=data['items']
    cartItem=data['cartItem']

    context={'items':items,'order':order,'cartItem':cartItem}
    return render(request,'onlinestore/cart.html',context)

def checkout(request):
    data=cartData(request)
    order=data['order']
    items=data['items']
    cartItem=data['cartItem']
    context={'items':items,'order':order,'cartItem':cartItem}
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
    if action=='add':
        orderItem.quantity=(orderItem.quantity+1)
    elif action=='remove':
        orderItem.quantity=(orderItem.quantity-1)
    print(orderItem.quantity)
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse('data was updated.....',safe=False)

#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt   
def processOrder(request):
    transaction_id=datetime.datetime.now()
    data=json.loads(request.body)
    print('Data:',data)
    if request.user.is_authenticated:
        customer=request.user.customer
        customer.name=request.user.username
        customer.save()
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
    else:
        customer,order=guestOrder(request,data)
    total=float(data['form']['total'])
    order.transaction_id=transaction_id
    print('Transection_ID:',transaction_id)
    if total==float(order.get_cart_total):
        print('Total:',order.get_cart_total)
        order.complete=True
    order.save()

    if order.shipping==True:
        ShippingAddress.objects.create(customer=customer,order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse('Payment completed',safe=False)


