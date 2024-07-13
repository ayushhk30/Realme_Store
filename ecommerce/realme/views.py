from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Mobile, Cart, CartItem
from .forms import SearchForm
from django.contrib.auth.decorators import login_required

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

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user_id=request.user.id)
    cart_items = CartItem.objects.filter(cart=cart) 
    total = sum(item.total for item in cart_items)
    print("total : ", total )
    return render(request, 'realme/cart_detail.html', {'cart_items': cart_items, 'total': total})

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