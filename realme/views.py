from django.http import HttpResponse
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from . models import Mobile, Product, Cart, CartItem, OrderItems 
from . forms import OrderCreateForm, SearchForm
from django.contrib.auth.decorators import login_required
from . forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from decimal import Decimal, InvalidOperation
from decimal import *

def mobile_list(request):
    form = SearchForm(request.GET or None)
    mobiles = Mobile.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']
        mobiles = mobiles.filter(name__icontains=query)

    return render(request, 'realme/mobile_list.html', {'mobiles': mobiles, 'form': form})

def mobile_detail(request, pk):
    mobile = get_object_or_404(Mobile, pk=pk)
    return render(request, 'realme/mobile_detail.html', {'mobile': mobile})


def product_list(request):
    form = SearchForm(request.GET or None)
    products = Product.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']
        products = products.filter(name__icontains=query)

    return render(request, 'realme/product_list.html', {'products': products, 'form': form})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'realme/product_detail.html', {'product': product})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'realme/register.html', {'form':form})    
    
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('mobile_list')
            else : 
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'realme/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')



@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user_id=request.user.id)
    cart_items = CartItem.objects.filter(cart=cart)

    total = Decimal(0)

    for item in cart_items:
        try:
            item_total = Decimal(item.quantity) * (Decimal(item.mobile.price) if item.mobile else Decimal(item.product.price))
            total += item_total
        except InvalidOperation:
            # Handle the case where item.total is not a valid Decimal
            # You may want to log this or handle it based on your requirements
            pass
    
    return render(request, 'realme/cart_detail.html', {'cart_items': cart_items, 'total': total})



@login_required
def add_to_cart(request, item_type, item_id):
    user_cart, created = Cart.objects.get_or_create(user_id=request.user.id)
    if item_type == 'mobile':
        item = get_object_or_404(Mobile, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, mobile=item)
    else:
        item = get_object_or_404(Product, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=item)

    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

def increase_qunatity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')

@login_required
def order_create(request):
    #cart = Cart.objects.get(id=1)
    cart, created = Cart.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart.items.all():
                OrderItems.objects.create(
                    order = order,
                    product = item.product,
                    mobile = item.mobile,
                    price = item.product.price if item.product else item.mobile.price,
                    quantity = item.quantity
                )
            cart.items.all().delete()

            client = razorpay.Client(auth=(settings.RAZORPAY_TEST_KEY_ID, settings.RAZORPAY_TEST_KEY_SECRET))
            payment_data = {
                'amount': int(order.total_cost * 100),
                'currency': 'INR',
                'receipt': f'order_{order.id}', 
            }
            print(payment_data)
            payment = client.order.create(data=payment_data)
             
            return render(request, 'realme/order_created.html', {'order': order, 'payment': payment, 'razorpay_key_id': settings.RAZORPAY_TEST_KEY_ID})
    else : 
        form = OrderCreateForm()
    return render(request, 'realme/order_create.html', {'cart': cart, 'form': form})

@login_required
@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        return HttpResponse("Payment Successful")
    return HttpResponse(status=400)
