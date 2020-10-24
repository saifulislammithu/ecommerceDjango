from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
# Create your views here.
def index(request):
    user=request.user
    context={'user':user}
    return render(request,'onlinestore/home.html',context)
def store(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItem=order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
    products=Product.objects.all()
    context={'products':products,'items':items,'order':order,'cartItem':cartItem}
    return render(request,'onlinestore/store.html',context)
def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
    context={'items':items,'order':order}
    return render(request,'onlinestore/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
    context={'items':items,'order':order}
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
    return JsonResponse('data was updated.....',safe=False)

    
def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.filter(customer=customer,complete=False)
        total=float(data['form']['total'])
        order.transaction_id=transaction_id

        if total==float(order.get_cart_total):
            order.complete=True
        order.save
        if order.shipping==True:
            ShippingAddress.objects.create(customer=customer,order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User not logged in.........')
    return JsonResponse('Payment completed',safe=False)


