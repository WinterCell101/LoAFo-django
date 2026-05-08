from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Item, ItemImage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.conf import settings


# --- AUTHENTICATION VIEWS ---

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        identifier = request.POST.get('username')
        password = request.POST.get('password')

        if '@' in identifier:
            try:
                user_obj = User.objects.get(email=identifier)
                username = user_obj.username
            except User.DoesNotExist:
                username = identifier
        else:
            username = identifier

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
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        chosen_username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'account/signup.html')

        if User.objects.filter(username=chosen_username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'account/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return render(request, 'account/signup.html')

        user = User.objects.create_user(
            username=chosen_username, email=email, password=password,
            first_name=fname, last_name=lname
        )
        # After signup, redirect to login (not home)
        messages.success(request, f"Account created! Please log in.")
        return redirect('login')

    return render(request, 'account/signup.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                f'/reset-password/{uid}/{token}/'
            )
            # In production, send email. For dev, show the link via message.
            messages.success(
                request,
                f"Password reset link generated. If email is configured, it was sent. "
                f"Dev link: {reset_url}"
            )
        except User.DoesNotExist:
            # Don't reveal if email exists
            messages.success(request, "If that email is registered, a reset link has been sent.")
        return redirect('login')
    return render(request, 'account/forgot_password.html')


def reset_password_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, 'account/reset_password.html', {'valid': True, 'uid': uidb64, 'token': token})
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password updated successfully! Please log in.")
            return redirect('login')
        return render(request, 'account/reset_password.html', {'valid': True, 'uid': uidb64, 'token': token})
    else:
        messages.error(request, "Invalid or expired reset link.")
        return redirect('login')


# --- CORE APP VIEWS ---

@login_required
def home(request):
    selected_location = request.GET.get('location')
    active_tab = request.GET.get('tab', 'lost')  # default to lost items

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
        'active_tab': active_tab,
    }
    return render(request, 'homepage.html', context)


@login_required
def report_item(request):
    if request.method == 'POST':
        color = request.POST.get('color')
        if color == 'other':
            color = request.POST.get('custom_color', '').strip()[:50] or 'other'

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
        'active_tab': 'lost',
    }
    return render(request, 'homepage.html', context)
