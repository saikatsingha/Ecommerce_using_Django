from django.db.models.deletion import Collector
from django.conf import settings
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime 
from . utils import cookieCart, cartData, guestOrder
import stripe


# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY

def store(request):

    data = cartData(request)
    cartItems = data['cartItems']
    
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)    

def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    

    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    #print(request.method)
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    key = settings.STRIPE_PUBLISHABLE_KEY

    context = {'items':items, 'order':order, 'cartItems': cartItems, 'key': key}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer = customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        # print(action)
        orderItem.quantity = (orderItem.quantity + 1)
        
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
           
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def thankYou(request):
    if request.method == 'POST':
        print(request.POST)
        charge = stripe.Charge.create(
            amount =  500,
            currency = 'INR',
            description = 'Cart Value in Stripe',
            source = request.POST['stripeToken']
        )
    return render(request, 'store/thankyou.html')   

# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
def processOrder(request):
    # print('Data:',request.body)
    # return JsonResponse('payment complete')
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # items = Order.objects.get_or_create(customer = customer, complete=False)
        
        

    else:
        # print('User is not logged in')
        # print('COOKIES:', request.COOKIES)
        customer, order = guestOrder(request, data)



    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )

    return JsonResponse('Payment Complete',safe=False)