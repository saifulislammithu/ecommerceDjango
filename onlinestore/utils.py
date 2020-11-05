import json
from .models import *
from users.models import NewUser

def cookieCart(request):
    try:
        cart=json.loads(request.COOKIES['cart'])
    except:
        cart={}
    print('Cart:',cart)
    items=[]
    order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
    cartItem=order['get_cart_items']
    for i in cart:
        try:
            cartItem+=cart[i]["quantity"]
            product=Product.objects.get(id=i)
            total=(product.price*cart[i]["quantity"])
            order['get_cart_total']+=total
            order['get_cart_items'] +=cart[i]["quantity"]
            item={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                    },
                'quantity':cart[i]["quantity"],
                'get_total':total
                }
            items.append(item)
            if product.digital==False:
                order['shipping']=True
        except:
            pass
    return {'cartItem':cartItem,'order':order,'items':items}
def cartData(request):
    if request.user.is_authenticated:
        user=request.user
        print('UserName:',user)
        customer=Customer.objects.get_or_create(user=user)
        
        
        
        #customer=Customer.objects.get_or_create(name=name)
        #customer.save()
        #customer=request.user.customer
        #customer.name=request.user.username
        #customer.email=request.user.email
        #newCustomer=customer.save()
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItem=order.get_cart_items
    else:
        cookieData=cookieCart(request)
        cartItem=cookieData['cartItem']
        order=cookieData['order']
        items=cookieData['items']
    return {'cartItem':cartItem,'order':order,'items':items}

def guestOrder(request,data):
    print('User not logged in')
    print('COOKIES:',request.COOKIES)
    name=data['form']['name']
    email=data['form']['email']
    cookieData=cookieCart(request)
    items=cookieData['items']
    customer,created=Customer.objects.get_or_create(email=email)
    customer.name=name
    customer.save()
    order=Order.objects.create(customer=customer,complete=False)
    for item in items:
        product=Product.objects.get(id=item['product']['id'])
        print('Product:',product)
        OrderItem.objects.create(
        product=product,
        order=order,
        quantity=item['quantity'],
        )
    print('Order_Customer',order.customer)
    print('Order_Complete',order.complete)
    print('Order_Tran_ID',order.transaction_id)
    return customer,order
