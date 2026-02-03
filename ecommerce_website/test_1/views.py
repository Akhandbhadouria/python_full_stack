from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count, F
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
        Product.objects.get_or_create(name="Smart Watch", price=199.99, category=categories[0], stock=10, description="A premium smartwatch", image="https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500")
        Product.objects.get_or_create(name="Wireless Headphones", price=149.99, category=categories[0], stock=15, description="Noise cancelling headphones", image="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500")
        Product.objects.get_or_create(name="Designer Hoodie", price=59.99, category=categories[1], stock=20, description="Ultra-comfortable hoodie", image="https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500")
        Product.objects.get_or_create(name="Coffee Table", price=89.99, category=categories[2], stock=5, description="Modern wooden coffee table", image="https://images.unsplash.com/photo-1533090161767-e6ffed986c88?w=500")
        categories = Category.objects.all()

    query = request.GET.get('q')
    
    products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)
    
    if query:
        products = products.filter(name__icontains=query)
        
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
            product = form.save(commit=False)
            product.added_by = request.user
            product.save()
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

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    # Filter products by the current admin
    my_products = Product.objects.filter(added_by=request.user)
    
    total_products = my_products.count()
    out_of_stock = my_products.filter(stock__lte=0).count()
    
    # Get OrderItems for my products
    my_order_items = OrderItem.objects.filter(product__in=my_products)
    
    # Calculate revenue specifically from my products
    total_revenue = my_order_items.aggregate(
        rev=Sum(F('price_at_order') * F('quantity'))
    )['rev'] or 0
    
    # Get unique orders that contain my products
    my_orders = Order.objects.filter(items__product__in=my_products).distinct()
    total_orders = my_orders.count()
    
    recent_orders = my_orders.order_by('-created_at')[:10]
    low_stock_products = my_products.filter(stock__lt=10).order_by('stock')[:5]
    
    # Product statistics (number of users per product)
    product_stats = my_products.annotate(
        user_count=Count('orderitem__order__user', distinct=True),
        sales_count=Sum('orderitem__quantity')
    ).order_by('-user_count')
    
    # Customer tracking (users who bought my products)
    customer_purchases = my_order_items.select_related('order', 'order__user').order_by('-order__created_at')[:20]
    
    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'out_of_stock': out_of_stock,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'product_stats': product_stats,
        'customer_purchases': customer_purchases,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def all_orders(request):
    # Get products added by this admin
    my_products = Product.objects.filter(added_by=request.user)
    # Get orders that contain at least one of these products
    orders = Order.objects.filter(items__product__in=my_products).distinct().order_by('-created_at')
    return render(request, 'all_orders.html', {'orders': orders})

@login_required
@user_passes_test(lambda u: u.is_staff)
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
    return redirect('all_orders')
    