from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product, CartItem, Category, Order, OrderItem

def home(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    
    if not categories.exists():
        # Seed some initial categories
        categories = [
            Category.objects.create(name="Electronics", description="Gadgets and devices"),
            Category.objects.create(name="Fashion", description="Clothing and accessories"),
            Category.objects.create(name="Home & Living", description="Furniture and decor"),
        ]
        # Add some sample products
        Product.objects.get_or_create(name="Smart Watch", price=199.99, category=categories[0], stock=10, description="A premium smartwatch")
        Product.objects.get_or_create(name="Wireless Headphones", price=149.99, category=categories[0], stock=15, description="Noise cancelling headphones")
        Product.objects.get_or_create(name="Designer Hoodie", price=59.99, category=categories[1], stock=20, description="Ultra-comfortable hoodie")
        Product.objects.get_or_create(name="Coffee Table", price=89.99, category=categories[2], stock=5, description="Modern wooden coffee table")
        categories = Category.objects.all()

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
        
    return render(request, 'home.html', {
        'products': products, 
        'categories': categories,
        'selected_category': int(category_id) if category_id else None
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'st_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')

@login_required
def data_input(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'insert.html', {'form': form})

@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return redirect('cart_view')
    
    total = sum(item.total_price() for item in cart_items)
    
    # Simple order creation - in a real app, you'd collect address info
    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        address="Default Address (Set in Profile)"
    )
    
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price_at_order=item.product.price
        )
        # Reduce stock
        item.product.stock -= item.quantity
        item.product.save()
    
    # Clear cart
    cart_items.delete()
    
    return redirect('order_list')

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})
    