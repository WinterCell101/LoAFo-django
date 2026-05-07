from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Item, ItemImage
from django.contrib.auth import authenticate, login, logout



# --- AUTHENTICATION VIEWS ---

def login_view(request):
    if request.method == 'POST':
        # identifier gets the value from the "Username or Email" field in your HTML
        identifier = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the user entered an email address
        if '@' in identifier:
            try:
                # Find the user object that has this email
                user_obj = User.objects.get(email=identifier)
                # Use that user's actual username for authentication
                username = user_obj.username
            except User.DoesNotExist:
                # If no email is found, fallback to the raw input
                username = identifier
        else:
            username = identifier

        # Authenticate using the username (which might be an email if you registered that way)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back!")
            return redirect('home')
        else:
            messages.error(request, "Invalid email/username or password.")
            return render(request, 'account/login.html')

    return render(request, 'account/login.html')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'account/signup.html')

        # Use the email as the username to ensure 'admin' isn't the display name
        if User.objects.filter(username=email).exists():
            messages.error(request, "A user with this email already exists.")
            return render(request, 'account/signup.html')

        # Create user with email as the username
        user = User.objects.create_user(username=email, email=email, password=password)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, f"Welcome, {email}!")
        return redirect('home')

    return render(request, 'account/signup.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# --- CORE APP VIEWS ---

@login_required
def home(request):
    selected_location = request.GET.get('location')

    all_locations = Item.objects.exclude(location__isnull=True).exclude(location='') \
        .values_list('location', flat=True).distinct().order_by('location')

    found_items = Item.objects.filter(item_status='FOUND').order_by('-item_id')
    lost_items = Item.objects.filter(item_status='LOST').order_by('-item_id')
    claimed_items = Item.objects.filter(item_status='CLAIMED').order_by('-item_id')

    if selected_location:
        found_items = found_items.filter(location=selected_location)
        lost_items = lost_items.filter(location=selected_location)
        claimed_items = claimed_items.filter(location=selected_location)

    context = {
        'found_items': found_items,
        'found_count': found_items.count(),
        'lost_items': lost_items,
        'lost_count': lost_items.count(),
        'claimed_items': claimed_items,
        'claimed_count': claimed_items.count(),
        'locations': all_locations,
    }
    return render(request, 'homepage.html', context)


def report_item(request):
    if request.method == 'POST':
        color = request.POST.get('color')
        if color == 'other':
            color = request.POST.get('custom_color')

        new_item = Item.objects.create(
            item_status=request.POST.get('report_type'),
            item_name=request.POST.get('name'),
            category=request.POST.get('category'),
            sub_category=request.POST.get('sub_category'),
            color=color,
            location=request.POST.get('location'),
            exact_location=request.POST.get('Trademark'),
            additional_location=request.POST.get('additional_info'),
            owner_name=request.POST.get('owner_name'),
            contact_info=request.POST.get('contact_info')
        )

        images = request.FILES.getlist('images')
        for img in images[:5]:
            ItemImage.objects.create(item=new_item, image=img)

        messages.success(request, "Successfully Submitted!!")
        return redirect('home')

    return redirect('home')


def search_items(request):
    query = request.GET.get('q', '').strip()
    results = Item.objects.all()

    locations_list = Item.objects.exclude(location__isnull=True).exclude(location='') \
        .values_list('location', flat=True).distinct().order_by('location')

    if query:
        search_filter = (
                Q(item_name__icontains=query) |
                Q(category__icontains=query) |
                Q(sub_category__icontains=query) |
                Q(location__icontains=query) |
                Q(exact_location__icontains=query)
        )
        if query.isdigit():
            search_filter |= Q(item_id=query)

        results = results.filter(search_filter)

    found_items = results.filter(item_status='FOUND').order_by('-item_id')
    lost_items = results.filter(item_status='LOST').order_by('-item_id')
    claimed_items = results.filter(item_status='CLAIMED').order_by('-item_id')

    context = {
        'found_items': found_items,
        'lost_items': lost_items,
        'claimed_items': claimed_items,
        'locations': locations_list,
        'query': query,
        'found_count': found_items.count(),
        'lost_count': lost_items.count(),
        'claimed_count': claimed_items.count(),
    }
    return render(request, 'homepage.html', context)