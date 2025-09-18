from .forms import ModernRegisterForm, CheckoutForm
from .utils import send_activation_email
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem, ShippingAddress
from .forms_profile import ProfileForm
from django.contrib.auth.decorators import login_required
# View simplu pentru înregistrare (placeholder)

def home(request):
    featured_product = Product.objects.first()
    top_products = Product.objects.all()[:3]  # primele 3 produse
    return render(request, 'store/home.html', {
        'featured_product': featured_product,
        'top_products': top_products
    })

def register(request):
    message = ''
    if request.method == 'POST':
        form = ModernRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_activation_email(user, request)
            message = 'Cont creat! Verifică emailul pentru activare.'
            return render(request, 'store/login_register.html', {'register_form': ModernRegisterForm(), 'register_success': True, 'register_message': message})
        else:
            message = 'Corectează erorile de mai jos.'
            return render(request, 'store/login_register.html', {'register_form': form, 'register_success': False, 'register_message': message})
    else:
        form = ModernRegisterForm()
    return render(request, 'store/login_register.html', {'register_form': form})

def activate_account(request, uid, token):
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return HttpResponse('Link invalid sau expirat.', status=400)
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'store/login_register.html', {'register_success': True, 'register_message': 'Cont activat! Te poți autentifica.'})
    else:
        return HttpResponse('Link invalid sau expirat.', status=400)

# View pentru pagina de login/înregistrare combinată
def register_login(request):
    message = ''
    show_login = True
    show_register = False
    if request.method == 'POST':
        form = ModernRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_activation_email(user, request)
            message = 'Cont creat! Verifică emailul pentru activare.'
            show_login = True
            show_register = False
            return render(request, 'store/login_register.html', {
                'register_form': ModernRegisterForm(),
                'register_success': True,
                'register_message': message,
                'show_login': show_login,
                'show_register': show_register
            })
        else:
            message = 'Corectează erorile de mai jos.'
            show_login = False
            show_register = True
            return render(request, 'store/login_register.html', {
                'register_form': form,
                'register_success': False,
                'register_message': message,
                'show_login': show_login,
                'show_register': show_register
            })
    else:
        form = ModernRegisterForm()
        show_login = True
        show_register = False
    return render(request, 'store/login_register.html', {
        'register_form': form,
        'show_login': show_login,
        'show_register': show_register
    })

# The following code block was misplaced and is now removed, as activate_account is already defined above.
def checkout(request):
    if not request.user.is_authenticated:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.get_full_path())
    cart = request.session.get('cart', {})
    if not cart:
        from django.shortcuts import redirect
        return redirect('cart_detail')
    if request.method == 'POST' and request.POST.get('paypal_order_id'):
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # (Opțional: verifică validitatea plății cu PayPal API folosind paypal_order_id)
            user = request.user if request.user.is_authenticated else None
            shipping_address = None
            if user:
                shipping_address, _ = ShippingAddress.objects.get_or_create(user=user)
                shipping_address.full_name = form.cleaned_data['full_name']
                shipping_address.country = form.cleaned_data['country']
                shipping_address.region = form.cleaned_data['region']
                shipping_address.city = form.cleaned_data['city']
                shipping_address.zip_code = form.cleaned_data['zip_code']
                shipping_address.address = form.cleaned_data['address']
                shipping_address.apartment = form.cleaned_data['apartment']
                shipping_address.house_number = form.cleaned_data['house_number']
                shipping_address.phone = form.cleaned_data['phone']
                shipping_address.email = form.cleaned_data['email']
                shipping_address.save()
            order = Order.objects.create(
                user=user,
                shipping_address=shipping_address,
                paid=True,  # Marchează comanda ca plătită
            )
            for product_id, item in cart.items():
                product_obj = Product.objects.get(id=product_id)
                selected_color = item.get('selected_color', None)
                OrderItem.objects.create(
                    order=order,
                    product=product_obj,
                    quantity=item['quantity'],
                    # Poți adăuga un câmp 'color' în OrderItem dacă vrei să salvezi permanent
                )
            del request.session['cart']
            return render(request, 'store/checkout.html', {'order': order, 'payment_status': 'success'})
        # Dacă formularul nu e valid, reafișează cu erori
        return render(request, 'store/checkout.html', {'form': form, 'payment_status': 'error'})
    else:
        initial = {}
        if request.user.is_authenticated:
            try:
                addr = request.user.shipping_address
                initial = {
                    'full_name': addr.full_name,
                    'country': addr.country,
                    'region': addr.region,
                    'city': addr.city,
                    'zip_code': addr.zip_code,
                    'address': addr.address,
                    'apartment': addr.apartment,
                    'house_number': addr.house_number,
                    'phone': addr.phone,
                    'email': addr.email,
                }
            except ShippingAddress.DoesNotExist:
                pass
        form = CheckoutForm(initial=initial)
        # Construiește lista de produse pentru afișare și PayPal
        cart_items = []
        total = 0
        for product_id, item in cart.items():
            prod = Product.objects.get(id=product_id)
            quantity = item['quantity']
            price = float(prod.price)
            total_price = price * quantity
            color_id = item.get('selected_color', None)
            color_obj = None
            color_name = ''
            if color_id:
                try:
                    color_obj = prod.colors.get(id=color_id)
                    color_name = color_obj.name
                except Exception:
                    color_name = ''
            cart_items.append({
                'product': prod,
                'quantity': quantity,
                'price': price,
                'total_price': total_price,
                'color': color_name,
            })
            total += total_price
        class CartObj:
            def __init__(self, items, total):
                self.items = items
                self.get_total_price = total
            def __iter__(self):
                return iter(self.items)
        cart_obj = CartObj(cart_items, total)
        return render(request, 'store/checkout.html', {'form': form, 'cart': cart_obj})

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
    return redirect('cart_detail')

def product_list(request):
    from .models import Category, Brand
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()

    category_slug = request.GET.get('category')
    brand_slug = request.GET.get('brand')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'brands': brands,
        'selected_category': category_slug,
        'selected_brand': brand_slug,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # Creează o listă de imagini cu culoare asociată (dacă există logică pentru imagini pe culoare)
    images_with_color = []
    for img in product.images.all():
        images_with_color.append({
            'url': img.image.url,
            'color': getattr(img, 'color', '').strip().lower() if hasattr(img, 'color') and img.color else '',
        })
    main_image = {'url': product.image.url if product.image else '', 'color': ''}
    return render(request, 'store/product_detail.html', {
        'product': product,
        'images_with_color': images_with_color,
        'main_image': main_image,
    })

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        quantity = item['quantity']
        price = float(product.price)
        total_price = price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'price': price,
            'total_price': total_price,
        })
        total += total_price
    class CartObj:
        def __init__(self, items, total):
            self.items = items
            self.get_total_price = total
        def __iter__(self):
            return iter(self.items)
    cart_obj = CartObj(cart_items, total)
    context = {'cart': cart_obj if cart_items else None}
    return render(request, 'store/cart.html', context)

# Dummy view for adding to cart (to resolve NoReverseMatch)
def cart_add(request, product_id):
    # Adaugă produsul în coșul din sesiune
    from django.shortcuts import redirect
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    quantity = int(request.POST.get('quantity', 1))
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += quantity
    else:
        cart[product_id_str] = {'quantity': quantity}
    request.session['cart'] = cart
    return redirect('cart_detail')


@login_required
def profile_view(request):
    user = request.user
    shipping_address, _ = ShippingAddress.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=shipping_address)
        if form.is_valid():
            form.save()
            return render(request, 'store/profile.html', {
                'form': form,
                'success': True
            })
    else:
        form = ProfileForm(instance=shipping_address)
    return render(request, 'store/profile.html', {
        'form': form
    })


# View pentru pagina de suport (contact admin/detinator)
def suport(request):
    return render(request, 'store/suport.html')