from django.shortcuts import render

# Create your views here.

def store(request):
    context = {}
    return render(request, 'stores/store.html', context)

def cart(request):
    context = {}
    return render(request, 'stores/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'stores/checkout.html', context)
